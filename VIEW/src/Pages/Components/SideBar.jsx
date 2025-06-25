import React, { useState } from 'react';
import { FaBook, FaComments } from 'react-icons/fa';
import { useNavigate } from 'react-router-dom';

export const Sidebar = () => {
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
      className={`d-flex flex-column border-end position-relative me-5`}
      style={{
        width: isExpanded ? '200px' : '90px',
        height: '782px',
        transition: 'width 0.3s ease',
        padding: '20px 0',
        backgroundColor: "var(--bg-color)",
        transition: "background 0.3s ease, color 0.3s ease"
      }}
    >
      <button 
        onClick={toggleSidebar}
        className="position-absolute bg-white border rounded-circle p-0"
        style={{
          top: '10px',
          right: '-15px',
          width: '30px',
          height: '30px',
          cursor: 'pointer',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          boxShadow: '0 0 5px rgba(0, 0, 0, 0)'
        }}
      >
        {isExpanded ? '◀' : '▶'}
      </button>
      
      <div 
        className="d-flex flex-column mt-5 gap-4"
        style={{
          alignItems: isExpanded ? 'flex-start' : 'center'
        }}
      >
        <button 
          onClick={goToLibrary}
          className="d-flex align-items-center bg-transparent border-0 p-2"
          style={{
            borderRadius: '4px',
            margin: '0 10px',
            transition: 'all 0.2s ease',
            color: "var(--text-color)"
          }}
        >
          <FaBook style={{ minWidth: '32px', minHeight: '32px' }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: '32px' }}>Library</span>
          )}
        </button>

        <button 
          onClick={goToChat}
          className="d-flex align-items-center bg-transparent border-0 p-2"
          style={{
            borderRadius: '4px',
            margin: '0 10px',
            transition: 'all 0.2s ease',
            color: "var(--text-color)"
          }}
        >
          <FaComments style={{ minWidth: '32px', minHeight: '32px' }} />
          {isExpanded && (
            <span className="ms-3" style={{ fontSize: '32px' }}>Chat</span>
          )}
        </button>
      </div>
    </div>
  );
};