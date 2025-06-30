import { ChevronLeft, ChevronRight } from "@mui/icons-material";
import {
  Box,
  CircularProgress,
  Container,
  IconButton,
  Typography,
} from "@mui/material";
import { useEffect, useRef } from "react";
import { useArticles } from "../../../hooks/api";
import SkeletonCategory from "./SkeletonCategory";
import ArticleCard from "../Article";

const Category = ({ topic }: { topic: string }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  const { data, isLoading, fetchNextPage, hasNextPage, isFetchingNextPage } =
    useArticles(topic);

  useEffect(() => {
    const handleScroll = () => {
      if (scrollRef.current) {
        const { scrollLeft, scrollWidth, clientWidth } = scrollRef.current;
        if (
          scrollLeft + clientWidth >= scrollWidth - 5 &&
          hasNextPage &&
          !isFetchingNextPage
        ) {
          fetchNextPage();
        }
      }
    };

    const scrollElement = scrollRef.current;
    scrollElement?.addEventListener("scroll", handleScroll);

    return () => {
      scrollElement?.removeEventListener("scroll", handleScroll);
    };
  }, [fetchNextPage, hasNextPage, isFetchingNextPage]);

  if (isLoading) {
    return <SkeletonCategory />;
  }

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const scrollAmount = 1000;
      scrollRef.current.scrollBy({
        left: direction === "left" ? -scrollAmount : scrollAmount,
        behavior: "smooth",
      });
    }
  };

  return (
    <Box
      sx={{
        py: 3,
      }}
    >
      <Container maxWidth="xl">
        <Typography
          variant="h5"
          component="h2"
          sx={{
            mb: 3,
            fontWeight: "bold",
            color: "white",
          }}
        >
          {topic !== "all" ? topic : "For You"}{" "}
        </Typography>

        <Box
          sx={{
            position: "relative",
            "&:hover .scroll-arrow": {
              opacity: 1,
            },
          }}
        >
          <IconButton
            className="scroll-arrow"
            onClick={() => scroll("left")}
            sx={{
              position: "absolute",
              left: -24,
              top: "50%",
              transform: "translateY(-50%)",
              zIndex: 2,
              bgcolor: "rgba(0,0,0,0.7)",
              color: "white",
              opacity: 0,
              transition: "opacity 0.3s ease",
              "&:hover": {
                bgcolor: "rgba(0,0,0,0.9)",
              },
            }}
          >
            <ChevronLeft fontSize="large" />
          </IconButton>

          <IconButton
            className="scroll-arrow"
            onClick={() => scroll("right")}
            sx={{
              position: "absolute",
              right: -16,
              top: "50%",
              transform: "translateY(-50%)",
              zIndex: 2,
              bgcolor: "rgba(0,0,0,0.7)",
              color: "white",
              opacity: 0,
              transition: "opacity 0.3s ease",
              "&:hover": {
                bgcolor: "rgba(0,0,0,0.9)",
              },
            }}
          >
            {isFetchingNextPage ? (
              <CircularProgress />
            ) : (
              <ChevronRight fontSize="large" />
            )}
          </IconButton>

          <Box
            ref={scrollRef}
            sx={{
              display: "flex",
              gap: 3,
              overflowX: "auto",
              scrollBehavior: "smooth",
              "&::-webkit-scrollbar": {
                display: "none",
              },
              msOverflowStyle: "none",
              pb: 1,
            }}
          >
            {data?.pages.map((page) =>
              page.map((item) => <ArticleCard key={item.url} article={item} />)
            )}
          </Box>
        </Box>
      </Container>
    </Box>
  );
};

export default Category;
