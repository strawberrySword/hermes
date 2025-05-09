import React, { useState, useEffect } from "react";
import { User, UserContext, UserContextType } from "./userContext";

export const UserProvider: React.FC<{ children: React.ReactNode }> = ({
  children,
}) => {
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const storedUser = localStorage.getItem("user");
    if (storedUser) setUser(JSON.parse(storedUser));
  }, []);

  const login = async (user_id: string) => {
    const res = await fetch(`/api/user/${user_id}`);
    if (res.ok) {
      const data = await res.json();
      const userObj = data as User;
      setUser(userObj);
      localStorage.setItem("user", JSON.stringify(userObj));
      return true;
    }
    return false;
  };

  const logoff = () => {
    setUser(null);
    localStorage.removeItem("user");
  };

  const contextValue: UserContextType = {
    user,
    login,
    logoff,
  };

  return (
    <UserContext.Provider value={contextValue}>{children}</UserContext.Provider>
  );
};
