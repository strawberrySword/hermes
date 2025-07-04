import TinderCard from "react-tinder-card";
import "./index.css";
import {
  useHistoryCount,
  useRandomArticles,
  useRecordOpenedArticle,
} from "../../hooks/api";
import { useQueryClient } from "@tanstack/react-query";
import ArticleCard from "../Feed/Article";
import { ThumbDown, ThumbUp } from "@mui/icons-material";
import { Box, Button, Fab, Tooltip, withStyles } from "@mui/material";
import { useNavigate } from "react-router";

type Direction = "right" | "left" | "up" | "down";

function TinderCards() {
  const { data: article, isLoading } = useRandomArticles();
  const { data: likedCount } = useHistoryCount();
  // const [likedCount, setLikedCount] = useState(0);
  const queryClient = useQueryClient();
  const { mutate: recordOpened } = useRecordOpenedArticle(article?.id);
  const navigate = useNavigate();
  const swiped = (direction: Direction) => {
    if (direction === "right") {
      recordOpened();
    }
    queryClient.invalidateQueries();
  };

  if (isLoading) {
    return "Loading...";
  }
  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "space-around",
        alignItems: "center",
        height: "100vh",
      }}
    >
      <img
        src="/logo-new.png"
        alt="My Image"
        style={{ width: "200px", height: "auto" }}
      />

      <div className="tinderCard_container">
        <Fab sx={{ zIndex: "-1" }} color="error" aria-label="like">
          <ThumbDown />
        </Fab>
        <TinderCard
          className="swipe"
          preventSwipe={[`up`, `down`]}
          onSwipe={(dir) => swiped(dir)}
          swipeRequirementType="position"
          swipeThreshold={300}
        >
          <ArticleCard article={article} extremelyClickable={false} />
        </TinderCard>
        <Fab sx={{ zIndex: "-1" }} color="success" aria-label="like">
          <ThumbUp />
        </Fab>
      </div>
      <Tooltip
        title={
          likedCount < 5 ? "Like more then 5 articles to start exploring" : ""
        }
      >
        <span>
          <Button
            onClick={() => {
              queryClient.invalidateQueries();
              navigate("/feed");
            }}
            disabled={likedCount < 5}
            variant="contained"
            sx={{
              bgcolor: "action.hover",
              color: "text.primary",
              border: "1px solid",
              borderColor: "divider",
              "&:hover": {
                bgcolor: "background.paper",
              },
              root: {
                "&.Mui-disabled": {
                  pointerEvents: "auto",
                },
              },
            }}
          >
            Start Reading!
          </Button>
        </span>
      </Tooltip>
    </Box>
  );
}
export default TinderCards;
