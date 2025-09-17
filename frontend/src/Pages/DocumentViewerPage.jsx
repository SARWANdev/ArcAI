import { useParams } from "react-router-dom";
import { useEffect, useState, useRef } from "react";
import { useAuth } from "./Components/Contexts/AuthContext";
import NotepadToggleButton from "./Components/Buttons/NotepadToggleButton";
import AIChatToggleButton from "./Components/Buttons/AIChatToggleButton";
import axios from "axios";
import PageLayoutDocument from "./Components/Containers/PageLayoutDocument";

export default function DocumentViewerPage() {
  const [isHeaderVisible, setIsHeaderVisible] = useState(true);
  const params = useParams();
  const { sub } = useAuth();

  // New state variables for project data
  const [projectId, setProjectId] = useState(null);
  const [projectTitle, setProjectTitle] = useState("Loading project...");

  // State to hold raw PDF bytes fetched from backend
  const [pdfBytes, setPdfBytes] = useState(null);

  // Blob URL generated from pdfBytes for iframe src
  const [blobUrl, setBlobUrl] = useState(null);

  // Ref to the iframe element to communicate via postMessage
  const iframeRef = useRef(null);

  // UI state toggles for Notepad and AI Chat panels
  const [showNotepad, setShowNotepad] = useState(false);
  const [showAIChat, setShowAIChat] = useState(false);

  // Notepad state
  const [noteText, setNoteText] = useState("");
  const [savedText, setSavedText] = useState("");

  // Notification UI states for file save confirmation
  const [showNotification, setShowNotification] = useState(false);
  const [notificationVisible, setNotificationVisible] = useState(false);

  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);

  // Fetch the PDF document and project details on component mount
  useEffect(() => {
    getDocument();
    getProjectDetails();
  }, []);

  // Fetch note for the document
  const fetchNote = async () => {
    try {
      if (!sub || !params.documentId) return;
      const response = await axios.get("http://localhost:3000/document/note", {
        params: { user_id: sub, document_id: params.documentId },
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

  // New: Fetch project details from backend API
  async function getProjectDetails() {
    try {
      const response = await axios.get("http://localhost:3000/document/project", {
        params: {
          user_id: sub,
          document_id: params.documentId,
        },
        withCredentials: true,
      });

      // Assuming the backend returns an object like { projectId: "...", projectName: "..." }
      setProjectId(response.data[0]);
      setProjectTitle(response.data[1]);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch project details.");
      setTimeout(() => setErrorMessage(null), 5000);
      setProjectTitle("Project not found");
    }
  }

  // Fetch document bytes from backend API
  async function getDocument() {
    try {
      const data = {
        user_id: sub,
        document_id: params.documentId,
      };

      // GET request expects an ArrayBuffer containing PDF bytes
      const response = await axios.get("http://localhost:3000/document/get-document", {
        params: data,
        responseType: "arraybuffer",
        withCredentials: true,
      });

      setPdfBytes(response.data);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch document.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  }

  // When pdfBytes changes, create a Blob URL for iframe source
  useEffect(() => {
    if (!pdfBytes) return;

    const blob = new Blob([pdfBytes], { type: "application/pdf" });
    const url = URL.createObjectURL(blob);
    setBlobUrl(url);

    // Clean up blob URL on component unmount or pdfBytes change
    return () => URL.revokeObjectURL(url);
  }, [pdfBytes]);

  // Listen for postMessage events from iframe to handle PDF interactions
  useEffect(() => {
    function handleMessage(event) {
      const { data } = event;

      // Add new annotation when highlights are updated inside iframe
      if (data?.type === "HIGLIGHTS_UPDATED") {
        // NOTE: The original code uses setAnnotations but it is undefined.
        // If annotation state is needed, define it here.
        // setAnnotations(prev => [...prev, data.annotation]);
      }
      // Respond with raw PDF bytes if iframe requests it
      else if (data?.type === "REQUEST_PDF_BYTES") {
        if (iframeRef.current && pdfBytes) {
          iframeRef.current.contentWindow.postMessage({
            type: "PDF_BYTES_RESPONSE",
            pdfBytes: Array.from(new Uint8Array(pdfBytes)),
          }, "*");
        }
      }
      // Receive modified PDF bytes from iframe and save them
      else if (data?.type === "MODIFIED_PDF_BYTES") {
        const modifiedBytes = new Uint8Array(data.pdfBytes);
        setPdfBytes(modifiedBytes);
        handleSavePdf(modifiedBytes);
      }
    }

    window.addEventListener("message", handleMessage);
    return () => window.removeEventListener("message", handleMessage);
  }, [pdfBytes]);

  // Send PDF bytes to iframe once it finishes loading
  const handleIframeLoad = () => {
    if (iframeRef.current && pdfBytes) {
      iframeRef.current.contentWindow.postMessage({
        type: "LOAD_PDF",
        pdfBytes: Array.from(new Uint8Array(pdfBytes)),
      }, "*");
    }
  };

  // Save PDF bytes to backend via multipart/form-data POST request
  async function handleSavePdf(bytesToSave = null) {
    const bytes = bytesToSave || pdfBytes;
    if (!bytes) return;

    try {
      const blob = new Blob([bytes], { type: "application/pdf" });

      const formData = new FormData();
      formData.append("file", blob, `${params.documentId}.pdf`);
      formData.append("user_id", sub);
      formData.append("document_id", params.documentId);

      await axios.post("http://localhost:3000/document/save", formData, {
        headers: { "Content-Type": "multipart/form-data" },
        withCredentials: true,
      });

      // Show save success notification with fade-in/out effects
      setShowNotification(true);
      setTimeout(() => setNotificationVisible(true), 10); // fade in
      setTimeout(() => setNotificationVisible(false), 2800); // fade out before hide
      setTimeout(() => setShowNotification(false), 3300); // hide after fade out
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to save PDF.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  }

  return (
    <PageLayoutDocument 
    projectId={projectId} 
    projectTitle={projectTitle} 
    isHeaderVisible={isHeaderVisible} 
    setIsHeaderVisible={setIsHeaderVisible}
    >
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Save confirmation notification */}
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
        >
          File saved successfully!
        </div>
      )}

      {/* PDF viewer iframe or loading message */}
      {blobUrl ? (
        <iframe
          ref={iframeRef}
          src="/pdf-viewer.html"
          title="PDF Viewer"
          className="flex-grow-1 border"
          style={{
            width: "100%",
            minHeight: 0,
            borderRadius: 8,
            height: isHeaderVisible ? "76vh" : "95vh",
          }}
          onLoad={handleIframeLoad}
        />
      ) : (
        <div>Loading document...</div>
      )}

      {/* Toggle buttons for Notepad and AI Chat (only one visible at a time) */}
      {!showAIChat && (
        <NotepadToggleButton
          document_id={params.documentId}
          showNotepad={showNotepad}
          setShowNotepad={setShowNotepad}
          setShowAIChat={setShowAIChat}
          noteText={noteText}
          setNoteText={setNoteText}
          savedText={savedText}
          setSavedText={setSavedText}
          fetchNote={fetchNote}
        />
      )}
      {!showNotepad && (
        <AIChatToggleButton
          document_id={params.documentId}
          showAIChat={showAIChat}
          setShowAIChat={setShowAIChat}
          setShowNotepad={setShowNotepad}
          fetchNote={fetchNote}
        />
      )}
    </PageLayoutDocument>
  );
}