import { Button, Spinner } from "react-bootstrap";
import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import HistoryRow from "../Containers/HistoryRow";
import ClearAllChatsButton from "../Buttons/ClearAllChatsButton";
import "./HistoryGrid.css";

export default function HistoryGrid() {
  const { sub } = useAuth(); // User identifier from auth context

  // State to hold the list of conversations
  const [conversations, setConversations] = useState([]);

  // Loading indicator state for fetching conversations
  const [loading, setLoading] = useState(true);

  // Current column sorted by ("Title" or "CreatedAt" or null)
  const [currentState, setCurrentState] = useState(null);

  // Current sorting order: "asc", "desc", or null (no sorting)
  const [currentOrder, setCurrentOrder] = useState(null);

  // Used to trigger a re-fetch when incremented
  const [refreshKey, setRefreshKey] = useState(0);

  // Toast for Clear All completion
  const [showNotification, setShowNotification] = useState(false);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const [notificationText, setNotificationText] = useState("");

    // State for the error popup
    const [errorMessage, setErrorMessage] = useState(null);

  const showToast = (text) => {
    setNotificationText(text);
    setShowNotification(true);
    setTimeout(() => setNotificationVisible(true), 10);
    setTimeout(() => setNotificationVisible(false), 2800);
    setTimeout(() => setShowNotification(false), 3300);
  };

  // Fetch conversations whenever sorting or refreshKey changes
  useEffect(() => {
    getConversations();
  }, [currentState, currentOrder, refreshKey]);

  /**
   * Fetch conversations from backend API with optional sorting.
   */
  async function getConversations() {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:3000/chat/history", {
        params: {
          user_id: sub,
          // Only send sorting params if both column and order are set
          ...(currentState && currentOrder
            ? { sort_by: currentState, order: currentOrder }
            : {}),
        },
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
        },
      });

      const convoList = response.data.data.conversations;
      setConversations(convoList);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch conversations.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setLoading(false);
    }
  }

  /**
   * Toggle the sorting order for a given column.
   * Cycles through asc -> desc -> none -> asc ...
   */
  function toggleOrder(column) {
    setLoading(true);
    if (currentState === column) {
      // If already sorting this column, toggle order or reset sorting
      if (currentOrder === "asc") {
        setCurrentOrder("desc");
      } else if (currentOrder === "desc") {
        setCurrentState(null);
        setCurrentOrder(null);
      } else {
        setCurrentOrder("asc");
      }
    } else {
      // If new column, start sorting ascending
      setCurrentState(column);
      setCurrentOrder("asc");
    }
  }

  /**
   * Render the label for a column with an arrow indicating sorting direction.
   */
  function renderSortLabel(label, column) {
    if (currentState === column) {
      if (currentOrder === "asc") return `${label} ▲`;
      if (currentOrder === "desc") return `${label} ▼`;
    }
    return label;
  }

  /**
   * Increment refreshKey to trigger data reload.
   */
  const refreshConversations = () => setRefreshKey((prev) => prev + 1);

  // Called by ClearAll after backend success; refresh first, then show toast when UI updated
  const handleCleared = async (err) => {
    await new Promise((resolve) => {
      setRefreshKey((prev) => prev + 1);
      // allow next render tick to complete before showing toast
      setTimeout(resolve, 0);
    });
    if (err) {
      showToast("Failed to delete chats. See console for details.");
    } else {
      showToast("All chats deleted successfully.");
    }
  };

  return (
    <div className="container-fluid px-0">
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {showNotification && (
        <div
          style={{
            position: 'fixed',
            top: 24,
            left: '50%',
            transform: 'translateX(-50%)',
            background: 'var(--bg-login-button-color)',
            color: '#fff',
            padding: '2rem 3.5rem',
            borderRadius: 16,
            fontSize: '1.5rem',
            boxShadow: '0 4px 24px rgba(0,0,0,0.25)',
            zIndex: 9999,
            fontWeight: 'bold',
            border: 'none',
            transition: 'opacity 0.5s',
            opacity: notificationVisible ? 1 : 0,
            pointerEvents: 'none',
          }}
          aria-live="polite"
        >
          {notificationText}
        </div>
      )}
      {/* Header row with sortable column labels */}
      <div className="history-header-row mb-4" style={{ alignItems: "center" }}>
        {/* Title column header */}
        <div
          className={`fw-bold text-truncate ${
            currentState === "Title" ? "text-primary text-decoration-underline" : ""
          }`}
          id="title-button"
          style={{
            flex: 2,
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: 0,
            margin: 0,
            marginLeft: "6px",
            boxShadow: "none",
          }}
          onClick={() => toggleOrder("Title")}
          tabIndex={0}
        >
          {renderSortLabel("Title", "Title")}
        </div>

        {/* CreatedAt column header */}
        <div
          className={`fw-bold text-truncate ${
            currentState === "CreatedAt" ? "text-primary text-decoration-underline" : ""
          }`}
          id="created-at-button"
          style={{
            flex: 1,
            cursor: "pointer",
            background: "none",
            border: "none",
            padding: 0,
            margin: 0,
            marginLeft: "-54px",
            boxShadow: "none",
          }}
          onClick={() => toggleOrder("CreatedAt")}
          tabIndex={0}
        >
          {renderSortLabel("Created at", "CreatedAt")}
        </div>

        {/* Clear all chats button aligned right */}
        <div style={{ flex: 1, display: "flex", justifyContent: "flex-end" }}>
          <ClearAllChatsButton onCleared={handleCleared} />
        </div>
      </div>

      {/* Conversation list or loading / empty states */}
      {loading ? (
        <div className="text-center mt-5">
          <Spinner animation="border" role="status" />
          <div>Loading conversations...</div>
        </div>
      ) : conversations.length === 0 ? (
        // No conversations found message.
        <div
          className="text-center"
          style={{ color: "var(--text-color)" }}
        >
          No conversations found.
        </div>
      ) : (
        <div style={{ overflow: "visible", height: "550px" }}>
          {conversations.map((conv, index) => (
            <HistoryRow
              key={index}
              conversation={conv}
              onRename={refreshConversations}
              onDelete={refreshConversations}
            />
          ))}
        </div>
      )}
    </div>
  );
}