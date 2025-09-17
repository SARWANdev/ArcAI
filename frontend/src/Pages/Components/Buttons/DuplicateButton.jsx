import "./DuplicateButton.css";
import {
  Button,
  Modal,
  ModalBody,
  ModalFooter,
  ModalHeader
} from "react-bootstrap";
import { useState, useEffect } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";

export default function DuplicateButton({ document_id, refreshDocuments }) {
  const [openModal, setOpenModal] = useState(false);
  const [projects, setProjects] = useState([]);
  const [selectedProjectId, setSelectedProjectId] = useState(null);
  const [status, setStatus] = useState(""); // "", "success", or "failure"
  const { sub } = useAuth();
  const [duplicating, setDuplicating] = useState(false);
  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);

  const fetchProjects = async () => {
    try {
      const res = await axios.get("http://localhost:3000/library/get-projects", {
        params: { user_id: sub },
        withCredentials: true,
      });
      setProjects(res.data.data.projects || []);
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch projects.");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  useEffect(() => {
    if (openModal) fetchProjects();
  }, [openModal]);

  const handleDuplicate = async () => {
    if (!selectedProjectId) return;

    try {
      setDuplicating(true);
      const response = await axios.post(
        "http://localhost:3000/document/duplicate",
        {
          user_id: sub,
          project_id: selectedProjectId,
          document_id: document_id,
        },
        { withCredentials: true }
      );
      await refreshDocuments();
      console.log(response.status)

      if (response.status === 200) {
        setStatus("success");
      } else {
        setStatus("failure");
      }
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Failed to fetch projects.");
      setTimeout(() => setErrorMessage(null), 5000);
      setStatus("failure");
    } finally {
      setOpenModal(false);
      setSelectedProjectId(null);
      setDuplicating(false);
      // Reset button after 3 seconds
      setTimeout(() => setStatus(""), 3000);
    }
  };

  const getButtonText = () => {
    if (status === "success") return "✓ Duplicated!";
    if (status === "failure") return "✗ Failed to Duplicate";
    return "Duplicate";
  };

  const getButtonVariant = () => {
    if (status === "success") return "success";
    if (status === "failure") return "danger";
    return "light";
  };

  return (
    <>
      {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      <div className="d-flex flex-column">
      <Button
        variant="light" // or keep it "outline-secondary"
        title="Duplicate"
        id="duplicate-button"
        style={{
            color:
            status === "success"
                ? "green"
                : status === "failure"
                ? "red"
                : "var(--text-color)",
        }}
        onClick={() => {
            setOpenModal(true);
            setStatus(""); // reset status when reopening modal
        }}
        >
        {getButtonText()}
        </Button>
      </div>

      <Modal show={openModal} onHide={() => setOpenModal(false)} centered size="md">
        <ModalHeader closeButton>
          <h5>Select Project to Save Duplicate</h5>
        </ModalHeader>

        <ModalBody>
          {projects.length > 0 ? (
            <ul className="list-unstyled">
              {projects.map((project) => (
                <li
                  key={project.ProjectId}
                  onClick={() =>
                    setSelectedProjectId(
                      selectedProjectId === project.ProjectId ? null : project.ProjectId
                    )
                  }
                  style={{
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    padding: "6px 0",
                    fontWeight: selectedProjectId === project.ProjectId ? "bold" : "normal",
                  }}
                >
                  <span style={{ width: "20px", textAlign: "center" }}>
                    {selectedProjectId === project.ProjectId ? "✓" : ""}
                  </span>
                  <span>{project.Title}</span>
                </li>
              ))}
            </ul>
          ) : (
            <p className="text-muted">No projects found.</p>
          )}
        </ModalBody>

        <ModalFooter className="d-flex justify-content-between w-100">
          <Button
            variant="primary"
            onClick={handleDuplicate}
            disabled={!selectedProjectId}
          >
            {duplicating ? "Duplicating..." : "Duplicate"}
          </Button>
          <Button variant="secondary" onClick={() => setOpenModal(false)}>
            Cancel
          </Button>
        </ModalFooter>
      </Modal>
    </>
  );
}