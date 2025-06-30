import Topnav from "./Topnav";
import Category from "./Category";
import { useTopics } from "../../hooks/api";
import Topic from "./Topic";
import { Box } from "@mui/material";

const Feed = () => {
  const { data: topics } = useTopics();

  return (
    <>
      <Topnav />

      <Category key="all" topic="all" />
      <Box
        sx={{
          p: 4,
          borderRadius: 2,
          bgcolor: "background.default",
          display: "grid",
          gridTemplateColumns: { md: "1fr 1fr 1fr" },
          gap: 4,
        }}
      >
        {topics?.slice(0, 6).map((topic) => (
          <Topic topic={topic} />
        ))}
      </Box>
    </>
  );
};

export default Feed;
