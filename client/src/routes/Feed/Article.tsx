import {
  Card,
  CardContent,
  CardActions,
  Typography,
  IconButton,
  CardHeader,
  Avatar,
  Box,
} from "@mui/material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import ShareIcon from "@mui/icons-material/Share";
import CommentIcon from "@mui/icons-material/Comment";
import ArticleIcon from "@mui/icons-material/Article";
import OpenInNewIcon from "@mui/icons-material/OpenInNew";

export type Article = {
  article_id: string;
  genre: string;
  subtitle: string;
  title: string;
  topic: string;
  url: string;
};

export const ArticleCard = ({
  article,
  userId,
}: {
  article: Article;
  userId: string | undefined;
}) => {
  return (
    <Card
      sx={{ maxWidth: 800, margin: "1rem auto", boxShadow: 3, borderRadius: 3 }}
    >
      <CardHeader
        avatar={
          <Avatar sx={{ bgcolor: "primary.main" }}>
            <ArticleIcon />
          </Avatar>
        }
        title={article.title}
        subheader={article.subtitle}
      />
      <CardContent>
        <Box mt={2}>
          <a
            href={article.url}
            target="_blank"
            rel="noopener noreferrer"
            style={{
              textDecoration: "none",
              color: "#1976d2",
              fontWeight: "bold",
            }}
          >
            Read Full Article{" "}
            <OpenInNewIcon
              fontSize="small"
              style={{ verticalAlign: "middle" }}
            />
          </a>
        </Box>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          <strong>Genre:</strong> {article.genre} | <strong>Topic:</strong>{" "}
          {article.topic}
        </Typography>
      </CardContent>
      <CardActions disableSpacing>
        <IconButton aria-label="like">
          <FavoriteIcon />
        </IconButton>
        <IconButton aria-label="comment">
          <CommentIcon />
        </IconButton>
        <IconButton aria-label="share">
          <ShareIcon />
        </IconButton>
      </CardActions>
    </Card>
  );
};
