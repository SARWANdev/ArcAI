import { Button } from "react-bootstrap";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { useState } from "react";
import "./DownloadButton.css";

export default function DownloadButton({ document_id, project_id }) {
  const { sub } = useAuth();
  const [downloading, setDownloading] = useState(false);
  const [downloaded, setDownloaded] = useState(false);
  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);
  const handleDownload = async () => {
    try {
      setDownloading(true);
      setDownloaded(false);
      const user_id = sub;
      const params = { user_id };
      
      let url = "";
      let filename = "";

      if (document_id) {
        url = "http://localhost:3000/document/download";
        params.document_id = document_id;
        filename = `document_${document_id}.zip`;
      } else if (project_id) {
        url = "http://localhost:3000/library/download";
        params.project_id = project_id;
        filename = `project_${project_id}_bundle.zip`;
      } else {
        console.error("No document_id or project_id provided for download.");
        return;
      }

      // Fetch ZIP blob from backend
      const response = await axios.get(url, {
        params,
        responseType: "blob",         // Receive data as binary blob
        withCredentials: true         // Include cookies/auth headers
      });

      // Create blob object
      const blob = new Blob([response.data], { type: "application/zip" });

      // Generate temporary URL for download
      const urlBlob = window.URL.createObjectURL(blob);
      const link = document.createElement("a");
      link.href = urlBlob;
      link.setAttribute("download", filename);

      // Programmatically trigger download
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(urlBlob);
      setDownloaded(true);

    } catch (error) {
      setErrorMessage(err.response?.data?.error|| "Failed to download.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setDownloading(false);
    }
  };

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
    <Button
      className="fw-bold w-100 mb-1"
      id="download-button"
      title="Download"
      onClick={handleDownload}
      disabled={downloading}
    >
      {downloading
        ? "Downloading\n..."
        : downloaded
        ? "Downloaded\n✓"
        : "Download"}
    </Button>
    </>
  );
}