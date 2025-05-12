import React, { useEffect } from "react";
import { useInView } from "react-intersection-observer";
import { useInfiniteQuery } from "@tanstack/react-query";
import { useUser } from "../../hooks/useUser";
import { Article, ArticleCard } from "./Article";

export const Feed = () => {
  const { user } = useUser();
  const { ref: loadMoreRef, inView } = useInView();
  console.log("yayyy");

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
    // please log in message and url to login
    return (
      <div>
        <h1>Please log in to view your feed</h1>
        <a href="/login">Login</a>
      </div>
    );
  }

  return status === "pending" ? (
    <p>Loading...</p>
  ) : status === "error" ? (
    <p>Error: {error.message}</p>
  ) : (
    <>
      {data.pages.map((group, i) => (
        <React.Fragment key={i}>
          {group.data.map((article) => (
            <ArticleCard
              key={article.article_id}
              article={article}
              userId={user.user_id}
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
