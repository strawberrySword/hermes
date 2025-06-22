import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { Feed } from "./routes/Feed/index.tsx";
import Login from "./routes/Login";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UserProvider } from "./contexts/UserProvider.tsx";
import { routes } from "./routes/routes.ts";
import { Auth0Provider } from "@auth0/auth0-react";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <Auth0Provider
        domain="dev-sohzugdgs6sgqmey.us.auth0.com"
        clientId="vLUQG3rmLsx4mfR6rXV2jRYgfwqeKhTY"
        authorizationParams={{
          redirect_uri: window.location.origin,
          audience: "https://dev-sohzugdgs6sgqmey.us.auth0.com/api/v2/",
        }}
      >
        <UserProvider>
          <BrowserRouter>
            <Routes>
              <Route
                path={routes.MF}
                element={<Feed feedType="matrix-factorization" />}
              />
              <Route path={routes.NRMS} element={<Feed feedType="nrms" />} />
              <Route
                path={routes.HISTORY}
                element={<Feed feedType="history" />}
              />
              <Route path={routes.LOGIN} element={<Login />} />
              <Route path={routes.PROFILE} element={<Login />} />
            </Routes>
          </BrowserRouter>
        </UserProvider>
      </Auth0Provider>
    </QueryClientProvider>
  </StrictMode>
);
