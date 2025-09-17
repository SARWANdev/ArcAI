import PropTypes from "prop-types";
import { useAuth } from "../Contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { useState, useEffect } from "react";
import axios from "axios";
import "./SearchBar.css";

/**
 * SearchBar provides a search input field that allows users to search
 * for either documents or chat conversations with live suggestions.
 *
 * Props:
 * - ifDoc: boolean — if true, enables document search
 * - ifChat: boolean — if true, enables chat search
 */
export default function SearchBar({ ifDoc, ifChat }) {
  const { sub } = useAuth(); // Authenticated user ID
  const navigate = useNavigate(); // React Router navigation hook

  const [query, setQuery] = useState(""); // User input for the search bar
  const [suggestions, setSuggestions] = useState([]); // Suggestions from backend

  // Track search lifecycle to decide when to show "No matches found"
  const [isSearching, setIsSearching] = useState(false);
  const [hasSearched, setHasSearched] = useState(false);

  // Debounced effect to fetch suggestions based on query input
  useEffect(() => {
    const delayDebounce = setTimeout(() => {
      const q = query.trim();

      if (q.length > 0) {
        // Mark we are initiating a search (prevents premature "no matches" message)
        setIsSearching(true);
        setHasSearched(false);

        if (ifDoc) {
          fetchDocumentSuggestions(q); // Fetch document matches
        } else if (ifChat) {
          fetchChatSuggestions(q); // Fetch chat matches
        }
      } else {
        // Clear state when input is empty
        setSuggestions([]);
        setIsSearching(false);
        setHasSearched(false);
      }
    }, 300); // Delay of 300ms for debounce

    return () => clearTimeout(delayDebounce); // Cleanup on re-render
  }, [query, ifDoc, ifChat]);

  // Makes an API call to get document suggestions
  const fetchDocumentSuggestions = async (input) => {
    if (!input || input.trim().length === 0) return;
    try {
      const res = await axios.get("http://localhost:3000/library/search/document", {
        params: { user_id: sub, query: input },
        withCredentials: true,
      });
      setSuggestions(res.data.results || []); // Update suggestions
    } catch (err) {
      console.error("Error fetching document suggestions:", err);
      setSuggestions([]); // ensure empty on error
    } finally {
      // Mark search finished so UI can show "No matches found" if empty
      setIsSearching(false);
      setHasSearched(true);
    }
  };

  // Makes an API call to get chat suggestions
  const fetchChatSuggestions = async (input) => {
    if (!input || input.trim().length === 0) return;
    try {
      const res = await axios.get("http://localhost:3000/chat/search", {
        params: { user_id: sub, query: input },
        withCredentials: true,
      });
      setSuggestions(res.data.results || []); // Update suggestions
    } catch (err) {
      console.error("Error fetching chat suggestions:", err);
      setSuggestions([]); // ensure empty on error
    } finally {
      // Mark search finished so UI can show "No matches found" if empty
      setIsSearching(false);
      setHasSearched(true);
    }
  };

  // Navigates to the document or chat page when a suggestion is clicked
  const handleSelectSuggestion = (idObj) => {
    if (ifDoc) {
      navigate(`/home/library/document/${idObj.DocumentId}`);
    } else if (ifChat) {
      navigate(`/home/chat/${idObj.ConversationId}`);
    }
  };

  return (
    <div className="position-relative">
      {/* Search Icon - visually placed on the left side of input */}
      <span
        style={{
          position: "absolute",
          left: "14px",
          top: "50%",
          transform: "translateY(-50%)",
          color: "var(--text-secondary-color)",
          pointerEvents: "none",
          display: "flex",
          alignItems: "center",
        }}
        aria-hidden="true"
      >
        {/* Inline SVG icon for search (magnifying glass) */}
        <svg
          width="20"
          height="20"
          viewBox="0 0 488.4 488.4"
          fill="currentColor"
          xmlns="http://www.w3.org/2000/svg"
        >
          <g>
            <g>
              <path d="M0,203.25c0,112.1,91.2,203.2,203.2,203.2c51.6,0,98.8-19.4,134.7-51.2l129.5,129.5c2.4,2.4,5.5,3.6,8.7,3.6
                s6.3-1.2,8.7-3.6c4.8-4.8,4.8-12.5,0-17.3l-129.6-129.5c31.8-35.9,51.2-83,51.2-134.7c0-112.1-91.2-203.2-203.2-203.2
                S0,91.15,0,203.25z M381.9,203.25c0,98.5-80.2,178.7-178.7,178.7s-178.7-80.2-178.7-178.7s80.2-178.7,178.7-178.7
                S381.9,104.65,381.9,203.25z"/>
            </g>
          </g>
        </svg>
      </span>

      {/* Input box for typing search query */}
      <input
        id="input-text"
        className="form-control"
        type="text"
        placeholder={
          ifDoc ? "Search documents..." :
          ifChat ? "Search chats..." : "Search..."
        }
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{
          width: "400px",
          marginRight: "150px",
          backgroundColor: "var(--bg-color)",
          transition: "background 0.3s ease, color 0.3s ease, width 0.3s ease",
          paddingLeft: "40px", // space for icon
        }}
        aria-label={ifDoc ? "Search documents" : ifChat ? "Search chats" : "Search"}
      />

      {/* Suggestions dropdown, shown only when suggestions are available */}
      {suggestions.length > 0 && (
        <ul className="list-group position-absolute w-100" style={{ zIndex: 1000 }}>
          {suggestions.map((item) => (
            <li
              key={item.DocumentId || item.ProjectId || item.ChatId}
              className="list-group-item list-group-item-action"
              onClick={() => handleSelectSuggestion(item)}
              style={{ cursor: "pointer" }}
              tabIndex={0}
              aria-label={item.Title || item.ProjectName || item.ChatTitle}
            >
              <strong>{item.Title || item.ProjectName || item.ChatTitle}</strong>
            </li>
          ))}
        </ul>
      )}

      {/* "No matches found" dropdown item (only after a completed search with zero results) */}
      {hasSearched && !isSearching && query.trim().length > 0 && suggestions.length === 0 && (
        <ul className="list-group position-absolute w-100" style={{ zIndex: 1000 }}>
          <li
            className="list-group-item text-muted"
            aria-live="polite"
            aria-atomic="true"
          >
            No matches found
          </li>
        </ul>
      )}
    </div>
  );
}

// Define prop types for better validation
SearchBar.propTypes = {
  ifDoc: PropTypes.bool,
  ifChat: PropTypes.bool,
};
