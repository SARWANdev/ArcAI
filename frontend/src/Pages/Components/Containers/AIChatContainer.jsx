import React, { useState, useEffect, useRef, useContext } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { ThemeContext } from "../Contexts/ThemeContext";
import "./AIChatContainer.css";

export default function AIChatContainer({ document_id, conversation_id, height, hideTitle }) {
  const chatContainerRef = useRef(null);

  // State for user input in textarea
  const [userInput, setUserInput] = useState("");
  // List of chat messages (user and AI)
  const [messages, setMessages] = useState([]);
  // Whether project/document selection popup is visible
  const [showProjectPopup, setShowProjectPopup] = useState(false);
  // List of projects fetched from backend
  const [projects, setProjects] = useState([]);
  // ID of the currently expanded project in popup (for toggling documents)
  const [expandedProjectId, setExpandedProjectId] = useState(null);
  // Map of project ID -> list of documents for that project
  const [projectDocuments, setProjectDocuments] = useState({});
  // Current conversation ID (string)
  const [conversationId, setConversationId] = useState("");
  // Currently selected single document ID (for placeholder, etc.)
  const [selectedDocument, setSelectedDocument] = useState(null);
  // Set of selected project IDs in the popup
  const [selectedProjectIds, setSelectedProjectIds] = useState(new Set());
  // Set of selected document IDs in the popup
  const [selectedDocumentIds, setSelectedDocumentIds] = useState(new Set());
  // Get current theme (e.g., "dark" or "light") from ThemeContext
  const { theme } = useContext(ThemeContext);
  // Ref for bottom of chat container
  const bottomRef = useRef(null);
  // User identifier from auth context
  const { sub } = useAuth();
  // Show "Generating answer . . ." while waiting for backend
  const [generating, setGenerating] = useState(false);
  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);
  // Reference for the attach popup
  const attachPopupRef = useRef(null);

  /**
   * Scroll chat container to bottom whenever messages update
   */
  useEffect(() => {
    if (chatContainerRef.current) {
      chatContainerRef.current.scrollTop = chatContainerRef.current.scrollHeight;
    }
  }, [messages, generating]); // include generating to scroll when placeholder appears

  /**
   * Scroll down when the attach popup becomes visible
   */ 
  useEffect(() => {
    if (showProjectPopup) {
      // Scroll smoothly to the attach popup container
      attachPopupRef.current?.scrollIntoView({ behavior: "smooth", block: "start" });
      // Also scroll to bottom of chat thread for consistency
      bottomRef.current?.scrollIntoView({ behavior: "smooth" });
    }
  }, [showProjectPopup]);

  /**
   * On mount or when document_id or conversation_id changes,
   * fetch initial conversation either by document or conversation ID.
   */
  useEffect(() => {
    if (document_id) {
      const docId = String(document_id);
      // Pre-select the document passed as prop
      setSelectedDocumentIds(new Set([docId]));
      setSelectedDocument(docId);
      fetchInitialConversation(docId);
    } else if (conversation_id) {
      fetchInitialConversationWithConversationId(conversation_id);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [document_id, conversation_id]);

  /**
   * Scroll to bottom of chat container when new messages appear
   */
  useEffect(() => {
    if (bottomRef.current) {
      bottomRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [messages, generating]);

  /**
   * Fetch initial conversation from backend based on document ID.
   * This starts a new conversation using the given document.
   */
  const fetchInitialConversation = async (docId) => {
    try {
      const response = await axios.post(
        "http://localhost:3000/chat/conversation/document",
        {
          user_id: sub,
          document_id: [docId],
          project_id: [],
        },
        {
          withCredentials: true,
          headers: { "Content-Type": "application/json" },
        }
      );

      // Update messages and conversation ID from response
      setMessages(response.data?.data?.list_of_messages || []);
      setConversationId(response.data?.data?.conversation_id);
    } catch (err) {
      console.error("Initial conversation fetch failed:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error || "Failed to start a new conversation.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  /**
   * Fetch all documents for all projects (when popup opens)
   */
  const fetchAllDocuments = async (projectsList) => {
    for (const project of projectsList) {
      if (!projectDocuments[project.ProjectId]) {
        await fetchDocumentsForProject(project.ProjectId);
      }
    }
  };

  /**
   * Fetch existing conversation by conversation ID.
   */
  const fetchInitialConversationWithConversationId = async (convId) => {
    try {
      const response = await axios.post(
        "http://localhost:3000/chat/conversation",
        {
          user_id: sub,
          conversation_id: convId,
        },
        {
          withCredentials: true,
          headers: { "Content-Type": "application/json" },
        }
      );

      setMessages(response.data?.data?.list_of_messages || []);
      setConversationId(convId);
    } catch (err) {
      console.error("Initial conversation fetch failed:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error || "Failed to load the conversation.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  /**
   * Fetch all projects belonging to the user for the selection popup.
   */
  const getProjects = async () => {
    try {
      const response = await axios.get("http://localhost:3000/library/get-projects", {
        params: { user_id: sub, sort_by: "Title", order: "asc" },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });
      const projectList = response.data.data.projects || [];
      setProjects(projectList);
      return projectList; // return the list so caller can use it
    } catch (err) {
      console.error("Error fetching projects:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error || "Failed to fetch projects.");
      setTimeout(() => setErrorMessage(null), 5000);
      return [];
    }
  };
  

  /**
   * Fetch documents belonging to a specific project when the project is expanded.
   */
  const fetchDocumentsForProject = async (project_id) => {
    try {
      const response = await axios.get("http://localhost:3000/project/get-documents", {
        params: {
          user_id: sub,
          project_id,
          sort_states: JSON.stringify([]),
          filter_state: "",
        },
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });

      // Update documents for the given project in state
      setProjectDocuments((prev) => ({
        ...prev,
        [project_id]: response.data.documents || [],
      }));
    } catch (err) {
      console.error("Error fetching documents:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error|| "Failed to fetch documents for this project.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  /**
   * Handles sending a new user prompt.
   * Starts a new conversation or updates conversation with selected documents/projects.
   */
  const handleUserPrompt = async () => {
    if (!userInput.trim()) return;

    const prompt = userInput.trim();
    setUserInput("");

    setMessages((prev) => [...prev, { role: "user", content: prompt }]);
    setGenerating(true); // start "Generating answer . . ."

    const requestBody = {
      user_id: sub,
      user_prompt: prompt,
      document_ids: Array.from(selectedDocumentIds),
      project_ids: Array.from(selectedProjectIds),
    };

    try {
      const response = await axios.post("http://localhost:3000/chat", requestBody, {
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });

      // Overwrite with backend convo (user + AI)
      setMessages(response.data?.data?.list_of_messages || []);
      setConversationId(response.data?.data?.conversation_id);
      // Hide the project popup after the first message is sent
      setShowProjectPopup(false);
    } catch (err) {
      console.error("Prompt failed:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error || "Failed to get a response from the AI.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setGenerating(false);
    }
  };

  /**
   * Handles sending a follow-up prompt in an existing conversation.
   */
  const handleFollowUp = async () => {
    if (!userInput.trim()) return;

    const prompt = userInput.trim();
    setUserInput("");

    setMessages((prev) => [...prev, { role: "user", content: prompt }]);
    setGenerating(true); // start "Generating answer . . ."

    const requestBody = {
      user_id: sub,
      user_prompt: prompt,
      conversation_id: conversationId,
    };

    try {
      const response = await axios.post("http://localhost:3000/chat/follow-up", requestBody, {
        withCredentials: true,
        headers: { "Content-Type": "application/json" },
      });

      // Overwrite with backend response
      setMessages(response.data?.data?.list_of_messages || []);
    } catch (err) {
      console.error("Prompt failed:", err.response?.data || err.message);
      setErrorMessage(err.response?.data?.error|| "Failed to send follow-up message.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setGenerating(false);
    }
  };

  /**
   * Toggle visibility of project/document selection popup.
   * Also fetch projects if none have been loaded yet.
   */
  const handleAttachClick = async () => {
    // Only allow showing the popup if no conversation is active yet
    if (!conversationId && messages.length === 0) {
      const newState = !showProjectPopup;
      setShowProjectPopup(newState);
  
      if (newState && !projects.length) {
        // Fetch projects
        const response = await getProjects();
        // After projects are loaded, fetch all documents for them
        if (response?.length) {
          await fetchAllDocuments(response);
        }
      } else if (newState && projects.length) {
        // Projects already loaded, fetch documents right away
        await fetchAllDocuments(projects);
      }
    }
  };
  

  /**
   * Toggle project selection for filtering.
   */
  const toggleProjectSelection = (projectId) => {
    setSelectedProjectIds((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(projectId)) {
        newSet.delete(projectId);
      } else {
        newSet.add(projectId);
      }
      return newSet;
    });
  };

  /**
   * Toggle selection of all documents in a project
   */
  const toggleAllDocumentsInProject = (projectId, isSelected) => {
    const documents = projectDocuments[projectId] || [];
    const documentIds = documents.map(doc => doc.DocumentId);
    
    setSelectedDocumentIds(prev => {
      const newSet = new Set(prev);
      
      if (isSelected) {
        // Add all document IDs from this project
        documentIds.forEach(id => newSet.add(id));
      } else {
        // Remove all document IDs from this project
        documentIds.forEach(id => newSet.delete(id));
      }
      
      // UPDATE: compute the first selected id from the Set iterator (reliable for Sets)
      const firstSelected = newSet.values().next().value;
      setSelectedDocument(firstSelected || null);
      
      return newSet;
    });
  };

  /**
   * Check if all documents in a project are selected
   */
  const areAllDocumentsSelected = (projectId) => {
    const documents = projectDocuments[projectId] || [];
    if (documents.length === 0) return false;
    
    return documents.every(doc => selectedDocumentIds.has(doc.DocumentId));
  };

  /**
   * Check if some documents in a project are selected (but not all)
   */
  const areSomeDocumentsSelected = (projectId) => {
    const documents = projectDocuments[projectId] || [];
    if (documents.length === 0) return false;
    
    const hasSomeSelected = documents.some(doc => selectedDocumentIds.has(doc.DocumentId));
    const allSelected = documents.every(doc => selectedDocumentIds.has(doc.DocumentId));
    
    return hasSomeSelected && !allSelected;
  };

  /**
   * Toggle document selection for filtering.
   * Updates the selectedDocument state to the first selected document or null.
   */
  const toggleDocumentSelection = (documentId) => {
    setSelectedDocumentIds((prev) => {
      const newSet = new Set(prev);
      if (newSet.has(documentId)) {
        newSet.delete(documentId);
      } else {
        newSet.add(documentId);
      }

      // UPDATE: compute the first selected id from the Set iterator (reliable for Sets)
      const firstSelected = newSet.values().next().value;
      setSelectedDocument(firstSelected || null);

      return newSet;
    });
  };

  return (
    <>
      {/* The error popup element */}
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}

      {/* Chat messages container with fixed height and scroll */}
      <div
        style={{
          height: height ? `${height}px` : "500px",
          marginBottom: "40px"
        }}
      >
        <div
          className="chat-thread p-3"
          id="ai-chat-container"
          ref={chatContainerRef}
          style={{
            backgroundColor: "var(--bg-color)",
            color: "var(--text-color)",
            // Only set maxHeight when there are messages or generating content
            maxHeight: messages.length > 0 || generating ? "60vh" : "none",
            overflowY: messages.length > 0 || generating ? "auto" : "visible",
            transition: "background 0.3s ease, color 0.3s ease",
            // Add minHeight to maintain some height when empty
            minHeight: "200px"
          }}
        >
          {messages.length === 0 ? (
            <div
              style={{
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                minHeight: "60vh",
                width: "100%",
              }}
            >
              {/* Show title only if hideTitle prop is not true */}
              {hideTitle !== true && (
                <h1 className="fs-1 fw-bold text-center m-0">What can I help with?</h1>
              )}
            </div>
          ) : (
            // Map over messages and display bubbles
            messages.map((msg, index) => (
              <div
                key={index}
                className={`mb-2 d-flex flex-column ${
                  msg.role === "user" ? "align-items-end" : "align-items-start"
                }`}
              >
                <div
                  className={`p-2 rounded message-bubble ${
                    msg.role === "user" ? "user-message" : "ai-message"
                  }`}
                  style={{
                    maxWidth: "70%",
                    textAlign: "left",
                    wordBreak: "break-word",
                    overflowWrap: "break-word",
                  }}
                >
                  {msg.content}
                </div>
              </div>

            ))
          )}
          {/* "Generating answer . . ." placeholder while waiting */}
          {generating && (
            <div className="mb-2 d-flex flex-column align-items-start text-start">
              <div
                className="p-2 rounded ai-message"
                style={{ maxWidth: "70%", fontStyle: "italic", opacity: 0.8 }}
              >
                Generating answer . . .
              </div>
              <div className="small mt-1" style={{ color: "var(--text-secondary-color)" }}>
                AI
              </div>
            </div>
          )}
          <div ref={bottomRef} />
        </div>
      </div>

      {/* Input form and controls */}
      <div
        className="container py-3"
        style={{
          background: "var(--bg-color)",
          width: "100%",
          maxWidth: "700px",
          margin: "0 auto",
          marginTop: messages.length === 0 ? "-80px" : "0px",
          transition: "background 0.3s ease, color 0.3s ease",
        }}
      >
        <form
          className="d-flex justify-content-center"
          onSubmit={(e) => {
            e.preventDefault();
            if (!conversationId) {
              handleUserPrompt();
            } else {
              handleFollowUp();
            }
          }}
        >
          <div
            className="d-flex align-items-end p-2 rounded border"
            style={{
              width: "100%",
              backgroundColor: "var(--bg-color)",
              transition: "background 0.3s ease, color 0.3s ease",
            }}
          >
            <textarea
              className="form-control border-0"
              id="input-area"
              placeholder={
                selectedDocumentIds.size > 0
                  ? "Ask me anything..."
                  : "Select a document to start"
              }
              style={{
                resize: "none",
                maxHeight: "210px",
                overflowY: "auto",
                boxShadow: "none",
                backgroundColor: "var(--bg-color)",
                color: "var(--text-color)",
                transition: "background 0.3s ease, color 0.3s ease",
              }}
              rows={1}
              value={userInput}
              onChange={(e) => setUserInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault(); // prevent newline
                  if (!conversationId) {
                    handleUserPrompt();
                  } else {
                    handleFollowUp();
                  }
                }
              }}
            />

            {/* Attach button is only visible when no document is selected and no conversation is active */}
            {!document_id && selectedDocumentIds.size === 0 && !conversationId && messages.length === 0 && (
              <button
                type="button"
                className="btn btn-link p-0 ms-2"
                onClick={handleAttachClick}
                title="Attach"
              >
                <img
                  src={theme === "light" ? "/images/dark-attachment-button.png" : "/images/light-attachment-button.png"}
                  alt="attach"
                  style={{ width: "28px", height: "28px" }}
                />
              </button>
            )}

            <button
              type="submit"
              className="btn btn-primary ms-2"
              style={{ height: "38px" }}
              disabled={selectedDocument == null}
            >
              ➤
            </button>
          </div>
        </form>

        {/* Project/document selection popup */}
        {/* The condition here ensures it only shows if no document_id is passed,
            it's explicitly set to show, there's no conversation_id, and no messages have been sent */}
        {!document_id && showProjectPopup && !conversationId && messages.length === 0 && (
          <div
            ref={attachPopupRef}
            className="border rounded p-2 mt-2"
            style={{
              maxHeight: "170px",
              overflowY: "auto",
              backgroundColor: "var(--bg-color)",
              transition: "background 0.3s ease, color 0.3s ease",
            }}
          >
            {projects.map((project) => {
              // compute tri-state state for the project checkbox
              const allSelected = areAllDocumentsSelected(project.ProjectId);
              const someSelected = areSomeDocumentsSelected(project.ProjectId);

              // Count selected docs within this project for the counter
              const totalDocs = projectDocuments[project.ProjectId]?.length || 0;
              const selectedCount = totalDocs
                ? Array.from(selectedDocumentIds).filter((id) =>
                    projectDocuments[project.ProjectId].some((doc) => doc.DocumentId === id)
                  ).length
                : 0;

              return (
                <div key={project.ProjectId}>
                  {/* Project title row with toggle */}
                  <div
                    className="d-flex align-items-center justify-content-between"
                    onClick={() => {
                      setExpandedProjectId(
                        project.ProjectId === expandedProjectId ? null : project.ProjectId
                      );
                      if (!projectDocuments[project.ProjectId]) {
                        fetchDocumentsForProject(project.ProjectId);
                      }
                    }}
                    style={{
                      cursor: "pointer",
                      userSelect: "none",
                      padding: "5px 10px",
                      backgroundColor: selectedProjectIds.has(project.ProjectId)
                        ? "var(--primary-light)"
                        : "transparent",
                      borderRadius: "4px",
                    }}
                  >
                    <div>
                      <span>
                        <img
                          src={
                            expandedProjectId === project.ProjectId
                              ? "/images/toggle-button-down.png"
                              : "/images/toggle-button-right.png"
                          }
                          alt="toggle"
                          style={{ width: "15px", height: "15px", marginRight: "8px" }}
                        />
                        <strong>{project.Title}</strong>
                      </span>
                      {/*selected/total counter next to project title */}
                      {totalDocs > 0 && (
                        <span
                          style={{
                            marginLeft: "8px",
                            fontSize: "0.85em",
                            color: "var(--text-secondary-color)",
                          }}
                        >
                          {selectedCount}/{totalDocs}
                        </span>
                      )}
                    </div>
                    <label
                      className="d-inline-flex align-items-center"
                      onClick={(e) => e.stopPropagation()} // prevent expanding/collapsing on checkbox click
                    >
                      <input
                        type="checkbox"
                        checked={allSelected}
                        ref={(el) => {
                          // native tri-state visual (indeterminate) when some but not all are selected
                          if (el) el.indeterminate = someSelected && !allSelected;
                        }}
                        onChange={async (e) => {
                          e.stopPropagation();
                          // ensure documents are loaded before toggling all
                          if (!projectDocuments[project.ProjectId]) {
                            await fetchDocumentsForProject(project.ProjectId);
                          }
                          // toggle all documents according to checkbox
                          toggleAllDocumentsInProject(project.ProjectId, e.target.checked);

                          // Keep selectedProjectIds in sync with checkbox state (optional, for styling)
                          setSelectedProjectIds((prev) => {
                            const ns = new Set(prev);
                            if (e.target.checked) ns.add(project.ProjectId);
                            else ns.delete(project.ProjectId);
                            return ns;
                          });
                        }}
                        onClick={(e) => e.stopPropagation()}
                      />
                    </label>
                  </div>

                  {/* Documents list for expanded project */}
                  {expandedProjectId === project.ProjectId && projectDocuments[project.ProjectId] && (
                    <div style={{ paddingLeft: "20px" }}>
                      {projectDocuments[project.ProjectId].map((doc) => {
                        const checked = selectedDocumentIds.has(doc.DocumentId);
                        return (
                          <div
                            key={doc.DocumentId}
                            className="d-flex align-items-center py-1"
                            onClick={() => toggleDocumentSelection(doc.DocumentId)} // click on row toggles selection
                            style={{ cursor: "pointer", userSelect: "none" }}
                          >
                            <input
                              className="me-2"
                              type="checkbox"
                              checked={checked}
                              onChange={() => toggleDocumentSelection(doc.DocumentId)}
                              onClick={(e) => e.stopPropagation()} // prevent double toggle / bubbling
                            />
                            <span>{doc.Title}</span>
                          </div>
                        );
                      })}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        )}
      </div>
    </>
  );
}
