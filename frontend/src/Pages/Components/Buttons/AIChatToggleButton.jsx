import PropTypes from "prop-types";
import { Button } from "react-bootstrap";
import { useEffect, useState } from "react";
import AIChatContainer from "../Containers/AIChatContainer";

/**
 * AIChatToggleButton toggles the visibility of the AI chat sidebar for a document.
 */
export default function AIChatToggleButton({
  document_id,
  showAIChat,
  setShowAIChat,
  setShowNotepad,
  fetchNote, // Receive the function as a prop
}) {
  const [errorMessage, setErrorMessage] = useState(null);

  const handleToggleAIChat = () => {
    setShowAIChat((prev) => !prev);
  };

  const handleGoToNotes = async () => {
    setShowAIChat(false);
    setShowNotepad(true);
    await fetchNote(); // Use the passed-in fetchNote function
  };

  useEffect(() => {
    const handleEsc = (e) => {
      if (e.key === "Escape" && showAIChat) {
        setShowAIChat(false);
      }
    };
    window.addEventListener("keydown", handleEsc);
    return () => window.removeEventListener("keydown", handleEsc);
  }, [showAIChat, setShowAIChat]);

  return (
    <>
      <Button
        onClick={handleToggleAIChat}
        className="fw-bold"
        aria-label={showAIChat ? "Close AI chat" : "Open AI chat"}
        style={{
          position: "fixed",
          top: "24%",
          right: showAIChat ? "330px" : "10px",
          transform: "translateY(-50%)",
          zIndex: 1050,
          transition: "right 0.3s ease",
        }}
      >
        {showAIChat ? "→" : "🤖 AI"}
      </Button>

      <div
        style={{
          position: "fixed",
          top: 0,
          right: showAIChat ? 0 : "-340px",
          width: "340px",
          height: "100vh",
          backgroundColor: "var(--bg-color)",
          borderLeft: "1px solid #ccc",
          boxShadow: "0 0 10px rgba(0,0,0,0.1)",
          zIndex: 1060,
          transition: "right 0.3s ease",
          display: "flex",
          flexDirection: "column",
          padding: "1rem",
        }}
      >
        <h5 className="fw-bold mb-3" style={{ color: "var(--text-color)" }}>
          AI Assistant
        </h5>

        <AIChatContainer document_id={document_id} height={750} hideTitle={true} />

        <div className="mt-2 d-flex justify-content-start">
          <Button variant="primary" onClick={handleGoToNotes}>
            Go to Notes
          </Button>
        </div>
      </div>
    </>
  );
}

AIChatToggleButton.propTypes = {
  document_id: PropTypes.string,
  showAIChat: PropTypes.bool.isRequired,
  setShowAIChat: PropTypes.func.isRequired,
  setShowNotepad: PropTypes.func.isRequired,
  fetchNote: PropTypes.func.isRequired,
};