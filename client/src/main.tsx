import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import Feed from "./routes/Feed";
import Login from "./routes/Login";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { routes } from "./routes/routes.ts";
import { Auth0Provider } from "@auth0/auth0-react";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import Tinder from "./routes/Tinder";
import CssBaseline from "@mui/material/CssBaseline";

const queryClient = new QueryClient();

const darkTheme = createTheme({
  palette: {
    mode: "dark",
  },
});

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={darkTheme}>
        <CssBaseline />
        <Auth0Provider
          domain="dev-sohzugdgs6sgqmey.us.auth0.com"
          clientId="vLUQG3rmLsx4mfR6rXV2jRYgfwqeKhTY"
          authorizationParams={{
            redirect_uri: `${window.location.origin}/feed`,
            audience: "https://dev-sohzugdgs6sgqmey.us.auth0.com/api/v2/",
          }}
        >
          <BrowserRouter>
            <Routes>
              <Route path={routes.FEED} element={<Feed />} />
              <Route path={routes.HISTORY} element={<Feed />} />
              <Route path={routes.LOGIN} element={<Login />} />
              <Route path={routes.PROFILE} element={<Login />} />
              <Route path={routes.TINDER} element={<Tinder />} />
            </Routes>
          </BrowserRouter>
        </Auth0Provider>
      </ThemeProvider>
    </QueryClientProvider>
  </StrictMode>
);
