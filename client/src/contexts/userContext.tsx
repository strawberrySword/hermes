// src/contexts/UserContext.ts
import { createContext } from "react";

export type User = {
  user_id: string;
};

export type UserContextType = {
  user: User | null;
  login: (username: string) => Promise<boolean>;
  logoff: () => void;
};

export const UserContext = createContext<UserContextType | undefined>(
  undefined
);
