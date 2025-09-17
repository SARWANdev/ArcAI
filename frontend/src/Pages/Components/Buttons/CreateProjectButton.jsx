import { Button, Modal, Form } from "react-bootstrap";
import { useState } from "react";
import axios from "axios";
import { useAuth } from "../Contexts/AuthContext";
import { useProjects } from "../Contexts/ProjectsContext";
import { createPortal } from "react-dom";
import "./CreateProjectButton.css";
/**
 * CreateProjectButton Component
 * 
 * This component renders a "Create Project" button which, when clicked,
 * opens a modal dialog allowing the user to enter a project name. Upon submission,
 * the entered project name and user ID (from AuthContext) are sent to the backend
 * via a POST request to create a new project.
 * 
 * Features:
 * - Modal-based UI for entering a new project name
 * - Uses `axios` to make HTTP POST request to `/library/create-project`
 * - Integrates with user authentication context (`useAuth`)
 * - Cleans up modal state after submission or cancelation
 * 
 * Dependencies:
 * - `axios` for HTTP requests
 * - `react-bootstrap` for UI components (`Button`, `Modal`, `Form`)
 * - `useAuth` from custom AuthContext for accessing `sub` (user ID)
 * - CSS styling from `CreateProjectButton.css`
 * 
 * Backend Requirement:
 * - Endpoint must accept JSON with `user_id` and `name` in request body
 * - Example payload: { user_id: "abc123", name: "My Project" }
 * 
 */
export default function CreateProjectButton() {
  const {projectCount, setProjectCount} = useProjects();
  const { sub } = useAuth();
  const [showModal, setShowModal] = useState(false);
  const [projectName, setProjectName] = useState("");
  const [creating, setCreating] = useState(false);
  const [error, setError] = useState("");

  const handleShow = () => {
    setShowModal(true);
    setError(""); // Clear any previous errors
  };
  
  const handleClose = () => {
    setProjectName("");
    setError(""); // Clear errors when closing
    setShowModal(false);
  };

  async function handleCreate() {
    try {
      setCreating(true);
      const data = {
        user_id: sub,
        name: projectName || "Untitled Project", // fallback
      };

      const response = await axios.post(
        "http://localhost:3000/library/create-project",
        data,
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
          },
        }
      );
      
      setProjectCount(projectCount + 1);
      handleClose(); // Only close on success
    } catch (err) {
      setError(err.response?.data?.error|| "Failed to create project.");
      setTimeout(() => setError(""), 5000);
    } finally {
      setCreating(false);
      // Don't close the modal here - only close on success
    }
  }

  const handleKeyPress = (e) => {
    if (e.key === "Enter" && projectName.trim()) {
      handleCreate();
    }
  };

  return (
    <>
      {/* Error Popup - Rendered at document body level */}
      {error && createPortal(
        <div className="error-popup">
          <p>{error}</p>
        </div>,
        document.body
      )}
      
      <Button className="fs-5" id="create-project-button" onClick={handleShow}>
        <img
          src="/images/Upload.png"
          alt="upload"
          style={{ width: "29px", height: "29px" }}
          className="me-3"
        />
        Create Project
      </Button>

      <Modal
        show={showModal}
        onHide={handleClose}
        centered
      >
        <Modal.Header
          closeButton
          style={{ backgroundColor: "var(--bg-color)", 
            color: "var(--text-color)", 
            borderTop: "1px solid var(--text-color)",
            borderRight: "1px solid var(--text-color)",
            borderLeft: "1px solid var(--text-color)" }}
        >
          <Modal.Title>New Project</Modal.Title>
        </Modal.Header>
        <Modal.Body style={{ backgroundColor: "var(--bg-color)", 
            color: "var(--text-color)", 
            borderRight: "1px solid var(--text-color)",
            borderLeft: "1px solid var(--text-color)" }}>
          <Form.Group>
            <Form.Label>Project Name</Form.Label>
            <Form.Control
              type="text"
              placeholder="Enter project name"
              value={projectName}
              style={{
                backgroundColor: "var(--bg-color)", 
                color: "var(--text-color)"
              }}
              onChange={(e) => setProjectName(e.target.value)}
              onKeyDown={handleKeyPress}
              autoFocus
            />
          </Form.Group>
        </Modal.Body>
        <Modal.Footer style={{ backgroundColor: "var(--bg-color)",
          borderRight: "1px solid var(--text-color)",
          borderLeft: "1px solid var(--text-color)",
          borderBottom: "1px solid var(--text-color)"
         }}>
          <Button variant="secondary" onClick={handleClose}>
            Cancel
          </Button>
          <Button
            variant="primary"
            onClick={handleCreate}
            disabled={!projectName.trim()}
          >
            {creating ? "Creating..." : "Create"}
          </Button>
        </Modal.Footer>
      </Modal>
    </>
  );
}