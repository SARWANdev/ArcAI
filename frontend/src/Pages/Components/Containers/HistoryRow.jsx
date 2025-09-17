import React, { useState, useRef, useEffect } from "react";
import DeleteButton from "../Buttons/DeleteButton";
import RenameButton from "../Buttons/RenameButton";

export default function HistoryRow({ conversation, onRename, onDelete }) {
  // State to track whether the settings dropdown is open
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);

  // State to track whether the rename modal is open
  const [isRenameModalOpen, setIsRenameModalOpen] = useState(false);

  // Ref for the settings dropdown container element
  const settingsRef = useRef(null);

  // Ref for the settings button element
  const settingsBtnRef = useRef(null);

  /**
   * Helper to format how long ago a date string was from now.
   * Returns a human-readable string like "3 days ago".
   */
  function formatDaysAgo(dateString) {
    if (!dateString) return "";
    const utcDate = new Date(dateString);
    const now = new Date();
    const diffMs = now - utcDate;

    const seconds = Math.floor(diffMs / 1000);
    const minutes = Math.floor(diffMs / (1000 * 60));
    const hours = Math.floor(diffMs / (1000 * 60 * 60));
    const days = Math.floor(diffMs / (1000 * 60 * 60 * 24));

    if (seconds < 60) return `${seconds} second${seconds !== 1 ? "s" : ""} ago`;
    if (minutes < 60) return `${minutes} minute${minutes !== 1 ? "s" : ""} ago`;
    if (hours < 24) return `${hours} hour${hours !== 1 ? "s" : ""} ago`;
    return `${days} day${days !== 1 ? "s" : ""} ago`;
  }

  /**
   * Handler for clicking on the whole row.
   * Navigates to chat page only if settings or rename modal are not open.
   */
  const handleRowClick = () => {
    if (!isSettingsOpen && !isRenameModalOpen) {
      // Using window.location.href for navigation (could be replaced with react-router if desired)
      window.location.href = `http://localhost:5173/home/chat/${conversation.ConversationId}`;
    }
  };

  /**
   * Toggles the visibility of the settings dropdown.
   * Stops event propagation to prevent row click from triggering.
   */
  const toggleSettings = (e) => {
    e.stopPropagation();
    setIsSettingsOpen((prev) => !prev);
  };

  // Effect to handle closing settings dropdown when clicking outside of it
  useEffect(() => {
    const handleClickOutside = (e) => {
      // Don't close if rename modal is open
      if (isRenameModalOpen) return;

      // If click is outside both settings dropdown and settings button, close dropdown
      if (
        settingsRef.current &&
        !settingsRef.current.contains(e.target) &&
        settingsBtnRef.current &&
        !settingsBtnRef.current.contains(e.target)
      ) {
        setIsSettingsOpen(false);
      }
    };

    if (isSettingsOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isSettingsOpen, isRenameModalOpen]);

  return (
    <div
      className="border-top position-relative history-container"
      style={{ cursor: "pointer" }}
      onClick={handleRowClick}
    >
      {/* Main row content */}
      <div className="history-row align-items-center p-2" style={{ height: "70px" }}>
        {/* Conversation title with truncation and tooltip */}
        <div
          className="text-truncate fw-semibold"
          style={{position: "relative", left: "1%", width: "600px", marginRight: "80px" }}
          title={conversation.Title}
        >
          {conversation.Title}
        </div>

        {/* Created at timestamp formatted as relative time */}
        <div
          className="text-truncate"
          style={{
            flex: 1,
            minWidth: 0,
            fontSize: "1.00rem",
            color: "var(--text-secondary-color)",
          }}
        >
          {formatDaysAgo(conversation.CreatedAt)}
        </div>

        {/* Settings button aligned right */}
        <div style={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <button
            className="btn btn-sm btn-outline-secondary settings-button"
            ref={settingsBtnRef}
            onClick={toggleSettings}
            aria-expanded={isSettingsOpen}
            aria-label="Toggle settings"
          />
        </div>
      </div>

      {/* Settings dropdown, shown only when open */}
      {isSettingsOpen && (
        <div
          ref={settingsRef}
          className="card card-body mt-2 p-2"
          style={{
            position: "absolute",
            top: "60px",
            right: "20px",
            zIndex: 2000,
            backgroundColor: "var(--bg-color)",
            border: "1px solid var(--text-secondary-color)",
            borderRadius: "4px",
            minWidth: "150px",
          }}
          // Prevent clicks inside dropdown from closing it or triggering row click
          onClick={(e) => e.stopPropagation()}
        >
          <DeleteButton
            conversation_id={conversation.ConversationId}
            onCloseSettings={() => setIsSettingsOpen(false)}
            onDelete={onDelete}
          />
          <RenameButton
            conversation_id={conversation.ConversationId}
            conversation_title={conversation.Title}
            onOpenModal={() => setIsRenameModalOpen(true)}
            onCloseModal={() => setIsRenameModalOpen(false)}
            onRename={() => {
              // Close settings and trigger rename refresh callback
              setIsSettingsOpen(false);
              onRename();
            }}
          />
        </div>
      )}
    </div>
  );
}

