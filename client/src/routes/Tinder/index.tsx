import React, { useState } from "react";
import TinderCard from "react-tinder-card";
import "./index.css";
import { useRandomArticles, useRecordOpenedArticle } from "../../hooks/api";
import { useQueryClient } from "@tanstack/react-query";
import ArticleCard from "../Feed/Article";
import { ThumbDown, ThumbUp } from "@mui/icons-material";
import FavoriteIcon from "@mui/icons-material/Favorite";
import { Box, Fab, IconButton } from "@mui/material";

function TinderCards() {
  const { data: article, isLoading } = useRandomArticles();
  const queryClient = useQueryClient();
  const { mutate: recordOpened } = useRecordOpenedArticle(article?.id);

  const swiped = (direction) => {
    if (direction === "right") {
      recordOpened();
    }
    queryClient.invalidateQueries(["articles", "random"]);
  };

  if (isLoading) {
    return "Loading...";
  }
  return (
    <Box
      sx={{
        display: "flex",
        
      }}
    >
      <div
        style={{
          position: "absolute",
          top: 0,
          left: "50%",
          transform: "translateX(-50%)",
          zIndex: 2,
          display: "flex",
          justifyContent: "center",
          width: "100%",
          marginTop: "16px",
        }}
      >
        <img
          src="/logo-new.png"
          alt="My Image"
          style={{ width: "200px", height: "auto" }}
        />
      </div>
      <div className="tinderCard_container">
        <Fab sx={{ zIndex: "-1" }} color="error" aria-label="like">
          <ThumbDown />
        </Fab>
        <TinderCard
          className="swipe"
          preventSwipe={[`up`, `down`]}
          onSwipe={(dir) => swiped(dir, article?.id)}
          swipeRequirementType="position"
          swipeThreshold={300}
        >
          <ArticleCard article={article} extremelyClickable={false} />
        </TinderCard>
        <Fab sx={{ zIndex: "-1" }} color="success" aria-label="like">
          <ThumbUp />
        </Fab>
      </div>
    </Box>
  );
}
export default TinderCards;
