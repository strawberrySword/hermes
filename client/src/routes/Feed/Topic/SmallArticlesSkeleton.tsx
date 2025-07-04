import { Box, Divider, Skeleton } from "@mui/material";

function SmallArticlesSkeleton() {
  return (
    <Box
      sx={{
        p: 2,
        borderRadius: 2,
        display: "grid",
        gap: 2,
        background: "#201c1c",
      }}
    >
      {[1, 2, 3, 4, 5].map(() => (
        <>
          <Skeleton height={100} width="100%" />
          <Divider />
        </>
      ))}
    </Box>
  );
}

export default SmallArticlesSkeleton;
