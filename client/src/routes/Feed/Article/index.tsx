import { AccessTime, Launch } from "@mui/icons-material";
import {
  Box,
  CardActionArea,
  CardActions,
  CardContent,
  Stack,
  Tooltip,
  Typography,
} from "@mui/material";
import { Card, CardMedia } from "@mui/material";
import { Article, useRecordOpenedArticle } from "../../../hooks/api";

interface ArticleCardProps {
  article: Article;
  extremelyClickable?: boolean;
}

const ArticleCard = ({
  article,
  extremelyClickable = true,
}: ArticleCardProps) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const { mutate: recordOpened } = useRecordOpenedArticle(article.id);
  return (
    <Card
      onClick={() => {
        if (extremelyClickable) {
          recordOpened();
          window.open(article.url);
        }
      }}
      key={article.id}
      sx={{
        minWidth: 350,
        maxWidth: 350,
        height: 400,
        display: "flex",
        flexDirection: "column",
        transition: "all 0.3s ease",
        boxShadow:
          "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
        borderRadius: 2,
        overflow: "hidden",
        "&:hover": {
          transform: "translateY(-8px)",
          boxShadow:
            "0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)",
        },
      }}
    >
      <CardActionArea>
        <CardMedia
          component="img"
          height="140"
          src={`/api/proxy?url=${article.image}`}
          alt="green iguana"
          sx={{
            objectFit: "cover",
            userSelect: "none",
            WebkitUserSelect: "none",
            MozUserSelect: "none",
            msUserSelect: "none",
            WebkitUserDrag: "none",
            pointerEvents: "none",
          }}
        />
        <CardContent sx={{ flex: 1, overflow: "hidden" }}>
          <Typography
            gutterBottom
            variant="h5"
            component="div"
            sx={{
              overflow: "hidden",
              textOverflow: "ellipsis",
              display: "-webkit-box",
              WebkitLineClamp: 5,
              WebkitBoxOrient: "vertical",
            }}
          >
            {article.title}
          </Typography>
        </CardContent>
      </CardActionArea>
      <CardActions
        sx={{
          mt: "auto",
          display: "flex",
          flexDirection: "row",
          justifyContent: "space-between",
        }}
      >
        <Stack direction="row" spacing={2} alignItems="center">
          <Box>
            <Tooltip title={article.publisher}>
              <Typography
                variant="body2"
                sx={{
                  fontWeight: 600,
                  color: "#374151",
                  overflow: "hidden",
                  whiteSpace: "nowrap",
                  textOverflow: "ellipsis",
                  maxWidth: "200px",
                }}
              >
                {article.publisher}
              </Typography>
            </Tooltip>
            <Stack direction="row" spacing={1} alignItems="center">
              <AccessTime sx={{ fontSize: 14, color: "#9ca3af" }} />
              <Typography variant="caption" sx={{ color: "#6b7280" }}>
                {formatDate(article.date)}
              </Typography>
            </Stack>
          </Box>
        </Stack>
        <Typography
          fontWeight={600}
          sx={{
            color: "#3b82f6",
            display: "flex",
            alignItems: "center",
            gap: 0.5,
            userSelect: "none",
            cursor: "pointer",
          }}
          onClick={() => {
            recordOpened();
            window.open(article.url);
          }}
        >
          Read More
          <Launch sx={{ fontSize: 16 }} />
        </Typography>
      </CardActions>
    </Card>
  );
};

export default ArticleCard;
