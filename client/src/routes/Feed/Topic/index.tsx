import { useArticles } from "../../../hooks/api";
import { Box, capitalize, Divider, Stack, Typography } from "@mui/material";

import SmallArticle from "../SmallArticle";
import TopicSkeleton from "./TopicSkeleton";

const Topic = ({ topic }: { topic: string }) => {
  const { data: articles, isLoading } = useArticles(topic);
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
        <Typography variant="h5">{capitalize(topic)}</Typography>
        <Divider />
        {articles?.pages.map((page) =>
          page.slice(0, 5).map((item) => (
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
