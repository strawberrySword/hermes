import { useAuth0 } from "@auth0/auth0-react";
import { useMutation, useQuery } from "@tanstack/react-query";
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

export const useArticles = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  return useQuery({
    queryKey: ["articles"],
    queryFn: async (): Promise<Array<Article>> => {
      const token = await getAccessTokenSilently({
        detailedResponse: true,
      });

      const response = await axios.get<Article[]>("api/articles", {
        headers: { Authorization: `Bearer ${token.id_token}` },
      });

      return response.data;
    },
    enabled: isAuthenticated,
    staleTime: 5 * 60 * 1000,
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
