import React, { useState } from 'react';
import { FaBook, FaComments } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';
import { useContext } from "react";
import { ThemeContext } from './ThemeContext';

export const Sidebar = () => {
  const { theme } = useContext(ThemeContext);
  const navigate = useNavigate();
  const [isExpanded, setIsExpanded] = useState(true);
  
  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };

  function goToLibrary(e) {
    if (e) e.preventDefault();
    navigate("/home/library", { replace: true });
  }

  function goToChat(e) {
    if (e) e.preventDefault();
    navigate("/home/chat-chatbot", { replace: true });
  }

  return (
    <div 
      className="d-flex flex-column border-end position-relative"
      style={{
        width: isExpanded ? '200px' : '90px',
        height: '100vh',
        transition: 'width 0.3s ease',
        padding: '20px 0',
        backgroundColor: "var(--bg-sidebar-color)",
        flexShrink: 0 // Prevents the sidebar from shrinking
      }}
    >
      <div 
        className="d-flex flex-column mt-5 gap-4"
        style={{
          alignItems: isExpanded ? 'flex-start' : 'center',
          paddingLeft: isExpanded ? '15px' : '0'
        }}
      >
        <button 
          onClick={toggleSidebar}
          className="d-flex align-items-center bg-transparent border-0 p-2"
          style={{
            borderRadius: '4px',
            transition: 'all 0.2s ease',
            color: "var(--text-color)",
            width: '100%',
            justifyContent: isExpanded ? 'flex-start' : 'center'
          }}
        >
          {isExpanded ? (
            <>
              <img 
                src={theme === "dark" ? '../../images/sidebar-left-dark-theme.png' : '../../images/sidebar-left-light-theme.png'} 
                alt="Collapse sidebar"
                style={{width: "35px", height: "35px"}}
              />
              <span className="ms-3" style={{ fontSize: '1rem' }}>Collapse</span>
            </>
          ) : (
            <img 
              src={theme === "dark" ? '../../images/sidebar-right-dark-theme.png' : '../../images/sidebar-right-light-theme.png'} 
              alt="Expand sidebar"
              style={{width: "35px", height: "35px"}}
            />
          )}
        </button>

        <button 
          onClick={goToLibrary}
          className="d-flex align-items-center bg-transparent border-0 p-2"
          style={{
            borderRadius: '4px',
            transition: 'all 0.2s ease',
            color: "var(--text-color)",
            width: '100%',
            justifyContent: isExpanded ? 'flex-start' : 'center'
          }}
        >
          <FaBook style={{ width: '32px', height: '32px' }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: '1rem' }}>Library</span>
          )}
        </button>

        <button 
          onClick={goToChat}
          className="d-flex align-items-center bg-transparent border-0 p-2"
          style={{
            borderRadius: '4px',
            transition: 'all 0.2s ease',
            color: "var(--text-color)",
            width: '100%',
            justifyContent: isExpanded ? 'flex-start' : 'center'
          }}
        >
          <FaComments style={{ width: '32px', height: '32px' }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: '1rem' }}>Chat</span>
          )}
        </button>
      </div>
    </div>
  );
};