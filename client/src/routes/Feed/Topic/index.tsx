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

const Topic = ({ topic }: { topic: string }) => {
  const { data: articles, isLoading } = useArticles(topic, 5);
  const [page, setPage] = useState()
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
              <ChevronLeft />
            </IconButton>
            <IconButton>
              <ChevronRight />
            </IconButton>
          </Box>
        </Box>
        <Divider />
        {articles?.pages.map((page) =>
          page.map((item) => (
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
