import {
  Box,
  CardContent,
  Typography,
  Card,
  CardMedia,
  CardActionArea,
} from "@mui/material";

import { Article, useRecordOpenedArticle } from "../../../hooks/api";

const SmallArticle = ({ article }: { article: Article }) => {
  const { mutate: recordOpened } = useRecordOpenedArticle(article.id);

  return (
    <Card
      onClick={() => {
        recordOpened();
        window.open(article.url);
      }}
    >
      <CardActionArea
        sx={{
          display: "flex",
          justifyContent: "space-between",
          height: "100px",
        }}
      >
        <Box sx={{ display: "flex", flexDirection: "column" }}>
          <CardContent sx={{ flex: "1 0 auto" }}>
            <Typography
              fontSize={20}
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
      </CardActionArea>
    </Card>
  );
};

export default SmallArticle;
