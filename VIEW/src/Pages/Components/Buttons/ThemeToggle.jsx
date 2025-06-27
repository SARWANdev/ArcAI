import { useContext } from 'react';
import { Button } from 'react-bootstrap';
import { ThemeContext } from '../ThemeContext';
import "./ThemeToggle.css"

export default function ThemeToggle() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <Button className = "fw-bold wb-1 p-2" id = "theme-toggle-button" style = {{transition: "background 0.3s ease, color 0.3s ease"}} onClick={toggleTheme}>{theme === "dark" ? "Light mode☀️" : "Dark mode🌙"}</Button>
  );
}