import "./ExportBibtexButton.css";
import { Button } from "react-bootstrap";
import { useAuth } from "../Contexts/AuthContext";
import { useState } from "react";
import axios from "axios";

/**
 * ExportBibtexButton is the component that is used to display the export bibtex button in the library page.
 * @returns {JSX} - The React component for the export bibtex button.
 */
export default function ExportBibtexButton({document_id}) {
  const { sub } = useAuth();
  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);
  const handleExport = async () => {
    try {
      const response = await axios.get("http://localhost:3000/document/bibtex", {
        params: { document_id: document_id, user_id : sub },
        responseType: "blob",
        withCredentials: true,
      });

      const blob = new Blob([response.data], { type: "application/x-bibtex" });
      const url = window.URL.createObjectURL(blob);

      const a = document.createElement("a");
      a.href = url;
      a.download = "export.bib"; // Suggested file name

      document.body.appendChild(a);
      a.click();

      a.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch projects.");
      setTimeout(() => setErrorMessage(null), 5000);
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
      className="btn btn-light"
      title="Export Bibtex"
      id="export-bibtex-button"
      onClick={handleExport}
    >
      Export Bibtex
    </Button>
    </>
  );
}