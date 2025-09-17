import React, { createContext, useState, useEffect } from "react";

// Create ThemeContext to provide theme state and toggle function
export const ThemeContext = createContext();

export const ThemeProvider = ({ children }) => {
  // State to hold the current theme, default to 'light'
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem("theme") || "light";
  });

  // Side effect to update the HTML attribute and localStorage when theme changes
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  /**
   * Toggles the theme between 'light' and 'dark'.
   * If forcedTheme param is provided and valid, sets theme explicitly.
   * Otherwise, toggles between 'light' and 'dark'.
   * @param {string} [forcedTheme] - optional forced theme ('light' or 'dark')
   */
  const toggleTheme = (forcedTheme) => {
    if (forcedTheme === "light" || forcedTheme === "dark") {
      setTheme(forcedTheme);
    } else {
      setTheme((prev) => (prev === "dark" ? "light" : "dark"));
    }
  };

  // Provide the current theme and toggle function to context consumers
  return (
    <ThemeContext.Provider value={{ theme, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};