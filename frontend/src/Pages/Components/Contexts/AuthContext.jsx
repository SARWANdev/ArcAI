import { createContext, useContext, useState } from "react";

const AuthContext = createContext();
/**
 * AuthContext provides a global authentication state using React Context API.
 * It stores user-related data such as authentication status, user ID (`sub`), profile picture, and name,
 * and makes them accessible throughout the component tree via the `useAuth` hook.
 * 
 * This is typically used in conjunction with protected routes and login/logout logic.
 *
 * @param {React.ReactNode} props.children - The child components that will have access to the AuthContext.
 * @returns {JSX.Element} AuthProvider wraps its children with authentication context.
 */
export const AuthProvider = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [sub, setSub] = useState(null);
  const [picture, setPicture] = useState(null);
  const [name, setName] = useState(null);
  return (
    <AuthContext.Provider value={{ isAuthenticated, setIsAuthenticated, sub, setSub, picture, setPicture, name, setName}}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);