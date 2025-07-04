import { useArticles } from "../../../hooks/api";
import {
  Box,
  capitalize,
  Divider,
  Stack,
  Typography,
  IconButton,
} from "@mui/material";

import SmallArticle from "../SmallArticle";
import TopicSkeleton from "./TopicSkeleton";
import { ChevronLeft, ChevronRight } from "@mui/icons-material";
import { useState } from "react";
import SmallArticlesSkeleton from "./SmallArticlesSkeleton";

const Topic = ({ topic }: { topic: string }) => {
  const {
    data: articles,
    isLoading,
    fetchNextPage,
    isFetchingNextPage,
  } = useArticles(topic, 5);
  const [page, setPage] = useState(0);
  if (isLoading) {
    return <TopicSkeleton />;
  }

  return (
    <Stack>
      <Box
        sx={{
          p: 2,
          borderRadius: 2,
          display: "grid",
          gap: 2,
          background: "#201c1c",
        }}
      >
        <Box display="flex" justifyContent="space-between">
          <Typography variant="h5">{capitalize(topic)}</Typography>
          <Box>
            <IconButton>
              <ChevronLeft
                onClick={() => {
                  setPage(Math.max(page - 1, 0));
                }}
              />
            </IconButton>
            <IconButton
              onClick={() => {
                fetchNextPage();
                setPage(page + 1);
              }}
            >
              <ChevronRight />
            </IconButton>
          </Box>
        </Box>
        <Divider />
        {isFetchingNextPage ? (
          <SmallArticlesSkeleton />
        ) : (
          articles?.pages[page].map((item) => (
            <>
              <SmallArticle article={item} />
              <Divider />
            </>
          ))
        )}
      </Box>
    </Stack>
  );
};

export default Topic;
