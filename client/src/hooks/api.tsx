import { useAuth0 } from "@auth0/auth0-react";
import { useQuery } from "@tanstack/react-query";
import axios from "axios";

export type Article = {
  date: string;
  image: string;
  keyword: string;
  publisher: string;
  title: string;
  url: string;
};

export const useArticles = () => {
  const { getAccessTokenSilently, isAuthenticated } = useAuth0();

  return useQuery({
    queryKey: ["articles"],
    queryFn: async (): Promise<Array<Article>> => {
      const token = await getAccessTokenSilently({
        detailedResponse: true,
      });

      const response = await axios.get<Article[]>(
        "http://localhost:5000/api/articles",
        {
          headers: { Authorization: `Bearer ${token.id_token}` },
        }
      );

      return response.data;
    },
    enabled: isAuthenticated,
  });
};
