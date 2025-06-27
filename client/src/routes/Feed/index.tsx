import Topnav from "./Topnav";
import Category from "./Category";

const Feed = () => {
  const categories = ["Action", "Comedy", "Drama", "Horror"];

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
      {categories.map((category) => (
        <Category key={category} category={category} />
      ))}
    </>
  );
};

export default Feed;
