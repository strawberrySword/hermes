import { useAuth0 } from "@auth0/auth0-react";
import { useInfiniteQuery, useMutation, useQuery } from "@tanstack/react-query";
import axios from "axios";

export type Article = {
  date: string;
  image: string;
  keyword: string;
  publisher: string;
  title: string;
  url: string;
  id: string;
};

export const useArticles = (topic: string) => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  return useInfiniteQuery({
    queryKey: ["articles", topic],
    queryFn: async ({ pageParam = 0 }): Promise<Array<Article>> => {
      const token = await getAccessTokenSilently({
        detailedResponse: true,
      });

      const response = await axios.get<Article[]>(`api/articles/${topic}`, {
        headers: { Authorization: `Bearer ${token.id_token}` },
      });

      return response.data;
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
    initialPageParam: 0,
    getNextPageParam: (lastPage, pages) => pages.length,
  });
};

export const useRecordOpenedArticle = (articleId: string) => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  return useMutation({
    mutationFn: async () => {
      if (!isAuthenticated) return;

      const token = await getAccessTokenSilently({
        detailedResponse: true,
      });

      await axios.post(
        `api/interactions/${articleId}`,
        {},
        {
          headers: { Authorization: `Bearer ${token.id_token}` },
        }
      );
    },
  });
};

export const useTopics = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  return useQuery({
    queryKey: ["topics"],
    queryFn: async (): Promise<Array<string>> => {
      const token = await getAccessTokenSilently({
        detailedResponse: true,
      });

      const response = await axios.get<string[]>("api/articles/top-topics", {
        headers: { Authorization: `Bearer ${token.id_token}` },
      });

      return [...response.data.map((topic) => topic["topic"])];
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
  });
};

export const useRandomArticles = () => {
  return useQuery({
    queryKey: ["articles", "random"],

    queryFn: async (): Promise<Article> => {
      const response = await axios.get<Article>(`api/article`);

      return response.data;
    },
    staleTime: 5 * 60 * 1000,
  });
};
