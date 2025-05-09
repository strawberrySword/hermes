import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Route, Routes } from 'react-router'
import { Feed } from './routes/Feed/index.tsx'
import { Login } from './routes/Login/index.tsx'
import './index.css'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient()

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Feed />} />
        <Route path="/login" element={<Login />} />
      </Routes>
    </BrowserRouter>
    </QueryClientProvider>
  </StrictMode>,
)
