import React, { useState, useEffect } from "react";
import { createPortal } from "react-dom";
import axios from "axios";
import NotepadToggleButton from "../Buttons/NotepadToggleButton";
import AIChatToggleButton from "../Buttons/AIChatToggleButton";
import { useAuth } from "../AuthContext";

/**
 * Manages the state and logic for the document view, including
 * the notepad and AI chat sidebars.
 */
export default function DocumentPanel({ document_id }) {
  const { sub: user_id } = useAuth();
  const [showNotepad, setShowNotepad] = useState(false);
  const [showAIChat, setShowAIChat] = useState(false);
  const [noteText, setNoteText] = useState("");
  const [savedText, setSavedText] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchNote = async () => {
    try {
      if (!user_id || !document_id) return;
      const response = await axios.get("http://localhost:3000/document/note", {
        params: { user_id, document_id },
        withCredentials: true,
      });
      const note = response?.data?.note ?? "";
      setNoteText(note);
      setSavedText(note);
    } catch (err) {
      setErrorMessage(err.response?.data?.error || "Error fetching note");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  return (
    <div>
      {/* Error Popup - Rendered at document body level */}
      {errorMessage && createPortal(
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>,
        document.body
      )}
      <NotepadToggleButton
        document_id={document_id}
        showNotepad={showNotepad}
        setShowNotepad={setShowNotepad}
        setShowAIChat={setShowAIChat}
        noteText={noteText}
        setNoteText={setNoteText}
        savedText={savedText}
        setSavedText={setSavedText}
        fetchNote={fetchNote} // Pass the function down
      />
      <AIChatToggleButton
        document_id={document_id}
        showAIChat={showAIChat}
        setShowAIChat={setShowAIChat}
        setShowNotepad={setShowNotepad}
        fetchNote={fetchNote} // Pass the function down
      />
    </div>
  );
}