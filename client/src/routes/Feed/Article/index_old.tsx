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
import { useQueryClient } from "@tanstack/react-query";
import { useEffect, useState } from "react";
import { Article } from "../../../hooks/api";

const ArticleCard = ({ article }: { article: Article }) => {
  const [isLiked, setIsLiked] = useState(false);
  const queryClient = useQueryClient();

  useEffect(() => {
    const checkIfLiked = async () => {
      try {
        const response = await fetch(`/api/articles/like/${article}/${""}`);
        if (response.status === 404) {
          setIsLiked(false);
          return;
        }
        if (!response.ok) {
          throw new Error("Failed to fetch like status");
        }
        setIsLiked(true);
      } catch (error) {
        console.error("Error fetching like status:", error);
      }
    };

    checkIfLiked();
  }, [article]);

  const handleLike = async () => {
    try {
      const response = await fetch(`/api/articles/like/${article}/`, {
        method: isLiked ? "DELETE" : "POST",
      });
      if (!response.ok) {
        throw new Error("Failed to like the article");
      }
      setIsLiked((liked) => !liked);
      queryClient.invalidateQueries({ queryKey: ["articles"] });
    } catch (error) {
      console.error("Error liking the article:", error);
    }
  };

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
        <IconButton
          aria-label="like"
          onClick={handleLike}
          style={{ color: isLiked ? "red" : "grey" }}
        >
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

export default ArticleCard;
