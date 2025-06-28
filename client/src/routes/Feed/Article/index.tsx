import { AccessTime, Launch } from "@mui/icons-material";
import { Box, CardContent, Stack, Typography } from "@mui/material";
import { Card, CardMedia, Chip, Avatar } from "@mui/material";
import { Article, useRecordOpenedArticle } from "../../../hooks/api";

interface ArticleCardProps {
  article: Article;
}

const ArticleCard = ({ article }: ArticleCardProps) => {
  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  const { mutate: recordOpened } = useRecordOpenedArticle(article.id);

  const getPublisherInitials = (publisher: string) => {
    return publisher
      .split(" ")
      .map((word) => word[0])
      .join("")
      .toUpperCase();
  };
  return (
    <Card
      key={article.url}
      onClick={() => {
        recordOpened();
        window.open(article.url);
      }}
      sx={{
        minWidth: 320,
        maxWidth: 320,
        bgcolor: "white",
        cursor: "pointer",
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
      <Box sx={{ position: "relative" }}>
        <CardMedia
          component="img"
          height="180"
          src={`/api/proxy?url=${article.image}`}
          alt={article.title}
          sx={{
            objectFit: "cover",
          }}
        />

        {/* Keyword Badge */}
        <Chip
          label={article.keyword}
          size="small"
          sx={{
            position: "absolute",
            top: 12,
            left: 12,
            bgcolor: "rgba(59, 130, 246, 0.9)",
            color: "white",
            fontWeight: 600,
            fontSize: "0.75rem",
            backdropFilter: "blur(4px)",
          }}
        />
      </Box>

      <CardContent sx={{ p: 3 }}>
        <Stack direction="row" spacing={2} alignItems="center" sx={{ mb: 2 }}>
          <Avatar
            sx={{
              width: 32,
              height: 32,
              bgcolor: "#3b82f6",
              fontSize: "0.75rem",
              fontWeight: 600,
            }}
          >
            {getPublisherInitials(article.publisher)}
          </Avatar>
          <Box>
            <Typography
              variant="body2"
              sx={{ fontWeight: 600, color: "#374151" }}
            >
              {article.publisher}
            </Typography>
            <Stack direction="row" spacing={1} alignItems="center">
              <AccessTime sx={{ fontSize: 14, color: "#9ca3af" }} />
              <Typography variant="caption" sx={{ color: "#6b7280" }}>
                {formatDate(article.date)}
              </Typography>
            </Stack>
          </Box>
        </Stack>

        <Typography
          variant="h6"
          component="h3"
          sx={{
            fontWeight: 600,
            color: "#111827",
            mb: 2,
            lineHeight: 1.4,
            display: "-webkit-box",
            WebkitLineClamp: 3,
            WebkitBoxOrient: "vertical",
            overflow: "hidden",
          }}
        >
          {article.title}
        </Typography>

        <Stack
          direction="row"
          justifyContent="space-between"
          alignItems="center"
        >
          <Typography
            variant="body2"
            sx={{
              color: "#3b82f6",
              fontWeight: 600,
              display: "flex",
              alignItems: "center",
              gap: 0.5,
            }}
          >
            Read More
            <Launch sx={{ fontSize: 16 }} />
          </Typography>
        </Stack>
      </CardContent>
    </Card>
  );
};

export default ArticleCard;
