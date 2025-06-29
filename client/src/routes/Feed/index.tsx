import Topnav from "./Topnav";
import Category from "./Category";
import { useTopics } from "../../hooks/api";

const Feed = () => {
  const { data: topics } = useTopics();

  // return (
  //   <>
  //     <Topnav />
  //     {isLoading ? (
  //       <Typography>Loading...</Typography>
  //     ) : (
  //       data?.map((article) => (
  //         <ArticleCard key={article.url} article={article} />
  //       ))
  //     )}
  //   </>
  // );
  return (
    <>
      <Topnav />
      {topics?.map((topic) => (
        <Category key={topic} topic={topic} />
      ))}
    </>
  );
};

export default Feed;
