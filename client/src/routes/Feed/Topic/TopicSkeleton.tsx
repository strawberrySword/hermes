import { Box, Divider, Skeleton, Stack } from "@mui/material";

function TopicSkeleton() {
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
        <Skeleton />
        <Divider />
        {[1, 2, 3, 4, 5].map(() => (
          <>
            <Skeleton height={100} width="100%" />
            <Divider />
          </>
        ))}
      </Box>
    </Stack>
  );
}

export default TopicSkeleton;
