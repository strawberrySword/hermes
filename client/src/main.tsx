import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Route, Routes } from "react-router";
import { Feed } from "./routes/Feed/index.tsx";
import { Login } from "./routes/Login/index.tsx";
import "./index.css";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UserProvider } from "./contexts/UserProvider.tsx";
import { routes } from "./routes/routes.ts";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
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
          </Routes>
        </BrowserRouter>
      </UserProvider>
    </QueryClientProvider>
  </StrictMode>
);
