import { Container, Skeleton } from "@mui/material";
import Box from "@mui/material/Box";

const SkeletonCategory = () => {
  return (
    <Box
      sx={{
        py: 3,
      }}
    >
      <Container maxWidth="xl">
        {/* <Skeleton height={32} width={100} /> */}
        <Box
          sx={{
            display: "flex",
            gap: 3,
            rowGap: 0,
          }}
        >
          {[1, 2, 3, 4, 5].map(() => (
            <Skeleton height={400} width={350} />
          ))}
        </Box>
      </Container>
    </Box>
  );
};

export default SkeletonCategory;
