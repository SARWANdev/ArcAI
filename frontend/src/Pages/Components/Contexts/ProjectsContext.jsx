import React, { createContext, useContext, useState } from "react";

/**
 * ProjectsContext provides state and setters for project and document counts
 * to be shared across the component tree.
 */
const ProjectsContext = createContext();

/**
 * ProjectsProvider component wraps children components to provide
 * access to project and document count state and their setters.
 *
 * @param {React.ReactNode} children - Components that consume this context.
 * @returns {JSX.Element} Context provider wrapping children.
 */
export function ProjectsProvider({ children }) {
  // State to track number of projects
  const [projectCount, setProjectCount] = useState(0);
  // State to track number of documents
  const [documentCount, setDocumentCount] = useState(0);

  // You may add additional updater functions here if needed

  return (
    <ProjectsContext.Provider
      value={{
        projectCount,
        setProjectCount,
        documentCount,
        setDocumentCount,
      }}
    >
      {children}
    </ProjectsContext.Provider>
  );
}

/**
 * Custom hook to access ProjectsContext values easily.
 *
 * @returns {{projectCount: number, setProjectCount: Function, documentCount: number, setDocumentCount: Function}}
 */
export function useProjects() {
  return useContext(ProjectsContext);
}