import { useState } from "react";
import { Button, Modal, Form } from "react-bootstrap";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import "./MoveButton.css";

/**
 * MoveButton allows the user to move a document to another project.
 * Opens a modal listing available projects and sends the move request to the backend.
 *
 * Props:
 * - document_id: ID of the document to move
 * - user_id: ID of the user (optional, not used due to AuthContext)
 * - refreshDocuments: callback to refresh the document list after move
 */
export default function MoveButton({ document_id, user_id, refreshDocuments }) {
  const { sub } = useAuth(); // Get the authenticated user ID
  const [showModal, setShowModal] = useState(false); // Controls modal visibility
  const [projects, setProjects] = useState([]); // List of available projects
  const [selectedProject, setSelectedProject] = useState(null); // Selected project for move
  // Toast notification state (match Notepad/Document toasts)
  const [showNotification, setShowNotification] = useState(false);
  const [notificationVisible, setNotificationVisible] = useState(false);
  const [notificationText, setNotificationText] = useState("");
  const [errorMessage, setErrorMessage] = useState(null);

  const showToast = (text) => {
    setNotificationText(text);
    setShowNotification(true);
    setTimeout(() => setNotificationVisible(true), 10);
    setTimeout(() => setNotificationVisible(false), 2800);
    setTimeout(() => setShowNotification(false), 3300);
  };

  // Fetch available projects for the user
  const fetchProjects = async () => {
    try {
      const response = await axios.get("http://localhost:3000/library/get-projects", {
        params: { user_id: sub },
        withCredentials: true,
      });

      const projectList = Array.isArray(response.data?.data?.projects)
        ? response.data.data.projects
        : [];

      setProjects(projectList);
    } catch (error) {
      setErrorMessage(err.response?.data?.error|| "Error fetching projects");
      setTimeout(() => setErrorMessage(null), 5000);
      setProjects([]);
    }
  };

  // Handle moving the document to the selected project
  const handleMove = async () => {
    try {
      if (!selectedProject) return;

      await axios.post(
        "http://localhost:3000/document/move",
        {
          document_id,
          project_id: selectedProject,
          user_id: sub,
        },
        { withCredentials: true }
      );
      setShowModal(false);
      showToast("Document moved successfully!");
      if (refreshDocuments) {
        // Delay refresh so toast stays visible on screen
        setTimeout(() => {
          refreshDocuments();
        }, 3400);
      }
    } catch (error) {
      setErrorMessage(err.response?.data?.error|| "Failed to move");
      setTimeout(() => setErrorMessage(null), 5000);
    }
  };

  // Open the modal and fetch projects
  const handleOpen = () => {
    setShowModal(true);
    fetchProjects();
  };

  // Close the modal and reset selected project
  const handleClose = () => {
    setShowModal(false);
    setSelectedProject(null);
  };

  return (
    <>
      {/* Toast overlay matching Notepad style */}
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

      {/* Move button */}
      <Button
        className="btn btn-light"
        title="Move"
        id="move-button"
        onClick={handleOpen}
      >
        Move
      </Button>

      {/* Modal for selecting destination project */}
      <Modal show={showModal} onHide={handleClose} centered>
        <Modal.Header closeButton>
          <Modal.Title>Select Destination Project</Modal.Title>
        </Modal.Header>

        <Modal.Body>
          {projects.length === 0 ? (
            <p>No available projects found.</p>
          ) : (
            <div style={{ maxHeight: "320px", overflowY: "auto" }}>
              <Form>
                {projects.map((project) => (
                  <Form.Check
                    key={project.ProjectId}
                    type="radio"
                    id={`project-${project.ProjectId}`}
                    label={project.Title}
                    name="project-radio"
                    value={project.ProjectId}
                    checked={selectedProject === project.ProjectId}
                    onChange={() => setSelectedProject(project.ProjectId)}
                    className="project-radio d-flex align-items-center mb-2"
                  />
                ))}
              </Form>
            </div>
          )}
        </Modal.Body>

        <Modal.Footer>
          <Button variant="secondary" onClick={handleClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleMove}
            disabled={!selectedProject}
          >
            Move
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}