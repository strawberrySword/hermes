import React, { useEffect } from "react";
import { useInView } from "react-intersection-observer";
import { useInfiniteQuery } from "@tanstack/react-query";
import { useUser } from "../../hooks/useUser";
import { Article, ArticleCard } from "./Article";
import Topnav from "./Topnav";
import { routes } from "../routes";
import { useNavigate } from "react-router";

export const Feed = () => {
  const { user } = useUser();
  const { ref: loadMoreRef, inView } = useInView();
  const navigate = useNavigate();

  const fetchProjects = async ({
    pageParam,
  }: {
    pageParam: number;
  }): Promise<{
    data: Article[];
    previousPage: number;
    nextCursor: number;
  }> => {
    const res = await fetch(`/api/articles/${user?.user_id}/${pageParam}`);
    return res.json();
  };

  const {
    data,
    error,
    fetchNextPage,
    hasNextPage,
    isFetching,
    isFetchingNextPage,
    status,
  } = useInfiniteQuery({
    queryKey: ["articles", user?.user_id],
    queryFn: fetchProjects,
    initialPageParam: 0,
    getNextPageParam: (lastPage) => lastPage.nextCursor,
    enabled: !!user,
  });

  useEffect(() => {
    if (inView && hasNextPage) {
      fetchNextPage();
    }
  }, [inView, hasNextPage, fetchNextPage]);

  if (!user) {
    navigate(routes.LOGIN);
  }

  if (status === "pending") {
    return <p>Loading...</p>;
  }
  if (status === "error") {
    return <p>Error: {error.message}</p>;
  }
  return (
    <>
      <Topnav />
      <br />
      <br />
      <br />
      <br />
      {data.pages.map((group, i) => (
        <React.Fragment key={i}>
          {group.data.map((article) => (
            <ArticleCard
              key={article.article_id}
              article={article}
              userId={user?.user_id}
            />
          ))}
        </React.Fragment>
      ))}
      <div ref={loadMoreRef}>
        {isFetchingNextPage
          ? "Loading more..."
          : hasNextPage
          ? "Scroll down to load more"
          : "Nothing more to load"}
      </div>
      <div>{isFetching && !isFetchingNextPage ? "Fetching..." : null}</div>
    </>
  );
};
