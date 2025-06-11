import React, { useState } from 'react';
import { FaBook, FaComments } from 'react-icons/fa'; // Font Awesome for expanded state
import styled from 'styled-components';
import { useNavigate } from 'react-router-dom';
/**
 * SideBar is a trial component which I am experimenting it to make the code more compact
 * @returns 
 */
export const Sidebar = () => {
  const navigate = useNavigate()
  const [isExpanded, setIsExpanded] = useState(true);

  const toggleSidebar = () => {
    setIsExpanded(!isExpanded);
  };

  /**
     * goToLibrary is the function that is used to navigate to the library page.
     */
  function goToLibrary(e) {
    if (e) e.preventDefault();
    navigate("/home/library", { replace: true });   //TODO: Change to /library
  }

  /**
     * goToChat is the function that is used to navigate to the chat page.
     * @param {Event} e - The event that is used to prevent the default behavior of the button.
     */
  function goToChat(e) {
    if (e) e.preventDefault();
    navigate("/home/chat-chatbot", { replace: true });
  }

  return (
    <SidebarContainer isExpanded={isExpanded}>
      <ToggleButton onClick={toggleSidebar}>
        {isExpanded ? '◀' : '▶'}
      </ToggleButton>
      
      <ButtonGroup>
        <SidebarButton isExpanded={isExpanded} onClick={goToLibrary}>
          {isExpanded ? (
            <>
              <FaBook />
              <span>Library</span>
            </>
          ) : (
            <FaBook />
          )}
        </SidebarButton>

        <SidebarButton isExpanded={isExpanded} onClick={goToChat}>
          {isExpanded ? (
            <>
              <FaComments />
              <span>Chat</span>
            </>
          ) : (
            <FaComments />
          )}
        </SidebarButton>
      </ButtonGroup>
    </SidebarContainer>
  );
};

// Styled Components (unchanged from your previous version)
const SidebarContainer = styled.div`
  width: ${({ isExpanded }) => (isExpanded ? '200px' : '90px')};
  height: 725px;
  background-color: white;
  color: black;
  transition: width 0.3s ease;
  position: relative;
  padding: 20px 0;
  border-right: 1px solid #e0e0e0;
`;

const ToggleButton = styled.button`
  position: absolute;
  top: 10px;
  right: -15px;
  background: white;
  border: 1px solid #e0e0e0;
  color: black;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0);
`;

const ButtonGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-top: 40px;
  align-items: ${({ isExpanded }) => (isExpanded ? 'flex-start' : 'center')}; 
`;

const SidebarButton = styled.button`
  background: transparent;
  border: none;
  color: black;
  display: flex;
  align-items: center;
  padding: 10px 15px;
  cursor: pointer;
  transition: all 0.2s ease;
  border-radius: 4px;
  margin: 0 10px;
  &:hover {
    background: #f5f5f5;
  }

  span {
    margin-left: ${({ isExpanded }) => (isExpanded ? '10px' : '0')};
    display: ${({ isExpanded }) => (isExpanded ? 'block' : 'none')};
    transition: all 0.3s ease;
    font-size: 32px;
    color: black;
  }

  svg {
    min-width: ${({ isExpanded }) => (isExpanded ? '32px' : '32px')};
    min-height: ${({ isExpanded }) => (isExpanded ? '32px' : '32px')};
    color: black;
  }
`;