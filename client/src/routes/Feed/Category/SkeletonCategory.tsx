import { Skeleton } from "@mui/material";
import Box from "@mui/material/Box";

const SkeletonCategory = () => {
  return (
    <Box
      display="flex"
      gap={2}
      padding={2}
      border="1px solid #e0e0e0"
      borderRadius="8px"
      bgcolor="#f9f9f9"
    >
      {/* Image Placeholder */}
      <Skeleton variant="rectangular" width={80} height={80} />

      {/* Text Placeholders */}
      <Box flex={1}>
        <Skeleton variant="text" width="60%" height={24} />
        <Skeleton variant="text" width="90%" height={16} />
      </Box>
    </Box>
  );
};

export default SkeletonCategory;
