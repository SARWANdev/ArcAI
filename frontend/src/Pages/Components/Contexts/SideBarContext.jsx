import { createContext, useContext, useState } from "react";

// Create a Context for the sidebar state (expanded or collapsed)
const SideBarContext = createContext();

/**
 * SideBarProvider component that wraps children with SideBarContext.Provider.
 * Manages the sidebar's expanded/collapsed state and provides the state and setter function.
 *
 * @param {object} props
 * @param {React.ReactNode} props.children - React child components that consume the context
 * @returns {JSX.Element} Provider component for sidebar state
 */
export const SideBarProvider = ({ children }) => {
  // State to track whether sidebar is expanded (true) or collapsed (false)
  const [isExpanded, setIsExpanded] = useState(true);

  return (
    <SideBarContext.Provider value={{ isExpanded, setIsExpanded }}>
      {children}
    </SideBarContext.Provider>
  );
};

/**
 * Custom hook to consume the SideBarContext easily.
 * @returns {{ isExpanded: boolean, setIsExpanded: function }} - Sidebar state and setter
 */
export const useSideBar = () => {
  const context = useContext(SideBarContext);
  if (context === undefined) {
    throw new Error("useSideBar must be used within a SideBarProvider");
  }
  return context;
};