import { Button } from "react-bootstrap";
import "./UploadButton.css";
import { useAuth } from "../Contexts/AuthContext";
import React, { useRef, useState } from "react";
import axios from "axios";

/**
 * UploadButton is a component that allows users to upload PDF files to a specific project.
 * @param {Object} props
 * @param {string} props.project_id - The ID of the project the file should be uploaded to.
 * @param {Function} [props.onUploadComplete] - Optional callback to run when upload finishes successfully.
 * @returns {JSX.Element} The rendered upload button component.
 */
export default function UploadButton({ project_id, onUploadComplete }) {
  const fileInputRef = useRef(null); // Ref to the hidden file input
  const { sub } = useAuth(); // Get the authenticated user ID from context

  // State variables for managing file upload status
  const [selectedFile, setSelectedFile] = useState(null); // Not strictly needed, but tracks selected file
  const [uploading, setUploading] = useState(false); // True while upload is in progress
  const [uploaded, setUploaded] = useState(false); // True if upload was successful
  const [errorMessage, setErrorMessage] = useState(null);

  // Trigger file picker dialog
  const handleButtonClick = () => {
    fileInputRef.current.click();
  };

  // When a file is chosen, immediately trigger upload
  const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
      setSelectedFile(file);
      uploadFile(file, sub, project_id);
    }
  };

  // Upload the file to the backend
  const uploadFile = async (file, user_sub, project_id) => {
    const formData = new FormData();
    formData.append("file", file);
    formData.append("user_sub", user_sub);
    formData.append("project_id", project_id);

    try {
      setUploading(true);
      const res = await axios.post("http://localhost:3000/document/upload", formData, {
        withCredentials: true,
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      console.log("Upload successful:", res.data);
      setUploaded(true);
      if (onUploadComplete) {
        onUploadComplete(); // Notify parent if needed
      }
    } catch (error) {
      setErrorMessage(error.response?.data?.error|| "Upload failed");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setUploading(false);
    }
  };

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      {/* Hidden file input field, triggered by button click */}
      <input
        type="file"
        ref={fileInputRef}
        style={{ display: "none" }}
        onChange={handleFileChange}
        accept=".pdf,application/pdf"
      />

      {/* Upload button with dynamic label */}
      <Button
        className="fw-bold mb-1"
        title="Upload"
        onClick={handleButtonClick}
        disabled={uploading}
        style={{
          border : "none",
          backgroundColor : "var(--bg-button-color)",
          color : "var(--text-color)",
          width: "114px",
          transition : "background 0.3s ease, color 0.3s ease"
        }}
      >
        {uploading
          ? "Uploading..."
          : uploaded
          ? "Uploaded ✓"
          : "Upload"}
      </Button>
    </>
  );
}