import { Box, CardContent, Typography, Card, CardMedia } from "@mui/material";

import { Article } from "../../../hooks/api";

const SmallArticle = ({ article }: { article: Article }) => {
  return (
    <Card
      sx={{ display: "flex", justifyContent: "space-between", height: "100px" }}
    >
      <Box sx={{ display: "flex", flexDirection: "column" }}>
        <CardContent sx={{ flex: "1 0 auto" }}>
          <Typography fontSize={20}
            sx={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              display: "-webkit-box",
              WebkitLineClamp: 3,
              WebkitBoxOrient: "vertical",
            }}
          >
            {article.title}
          </Typography>
        </CardContent>
      </Box>
      <CardMedia
        component="img"
        src={`/api/proxy?url=${article.image}`}
        alt="green iguana"
        sx={{
          width: "150px",
          height: "auto",
          objectFit: "cover",
          userSelect: "none",
          WebkitUserSelect: "none",
          MozUserSelect: "none",
          msUserSelect: "none",
          WebkitUserDrag: "none",
          pointerEvents: "none",
        }}
      />
    </Card>
  );
};

export default SmallArticle;
