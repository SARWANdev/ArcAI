import { useEffect, useState } from 'react';
import { Button } from 'react-bootstrap';
import "./ThemeToggle.css"

export default function ThemeToggle() {
  const [theme, setTheme] = useState(() => {
    return localStorage.getItem('theme') || 
      (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
  });

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme);
    localStorage.setItem('theme', theme);
  }, [theme]);

  const toggleTheme = () => {
    setTheme(prev => (prev === 'dark' ? 'light' : 'dark'));
  };

  return (
    <Button className = "fw-bold wb-1 p-2" id = "theme-toggle-button" onClick={toggleTheme}>Toggle</Button>
  );
}