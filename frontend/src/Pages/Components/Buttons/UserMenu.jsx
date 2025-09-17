import PropTypes from "prop-types";
import { useAuth } from "../Contexts/AuthContext";
import { Collapse } from "bootstrap";
import { useRef, useEffect, useState } from "react";
import { Button, Modal } from "react-bootstrap";
import ThemeToggle from "./ThemeToggle";
import "./UserMenu.css";

/**
 * The UserMenu component is a user profile dropdown menu that displays the user's profile picture, 
 * name, and options such as theme toggle, sign out, and delete. It uses Bootstrap's Collapse for 
 * animation and React Bootstrap for styled buttons.
 * 
 * It also closes the dropdown menu when the user clicks outside of it, using a document event listener.
 * The menu includes a theme toggle component and buttons for sign-out and account deletion.
 *
 * @param {Object} props - Props passed to the component
 * @param {number|null} [props.left=null] - Optional percentage from the left edge to position the profile button
 * @param {number|null} [props.right=null] - Optional percentage from the right edge to position the profile button
 * 
 * @returns {JSX.Element} A JSX element representing the user profile dropdown menu
 */
export default function UserMenu({ left = null, right = null }) {
  const { setIsAuthenticated, picture, name, sub } = useAuth();
  const collapseRef = useRef(null);
  const toggleButtonRef = useRef(null);
  const profilePicture = picture || "/images/userPhoto.jpg";
  const userName = name || "User";
  const [errorMessage, setErrorMessage] = useState(null);

  // Confirm delete modal + deleting state
  const [showConfirmDelete, setShowConfirmDelete] = useState(false);
  const [deleting, setDeleting] = useState(false);

  // Sign out handler
  const handleSignOut = () => {
    window.location.href = "http://localhost:3000/logout";
    setIsAuthenticated(false);
  };

  // Open confirm delete modal
  const requestDelete = () => {
    setShowConfirmDelete(true);
  };

  // Close confirm delete modal
  const cancelDelete = () => {
    setShowConfirmDelete(false);
  };

  // Delete user handler (runs after confirming)
  const handleDeleteUser = async () => {
    try {
      setDeleting(true);
      const response = await fetch("http://localhost:3000/user/delete", {
        method: "DELETE",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ user_id: sub }),
        credentials: "include",
      });

      if (!response.ok) {
        const errorData = await response.json();
        console.error("Delete failed:", errorData.message || "Unknown error");
        return false;
      }

      const data = await response.json();
      window.location.href = "http://localhost:3000/logout";
      setIsAuthenticated(false);
      console.log("User deleted successfully:", data);
      return true;
    } catch (error) {
      setErrorMessage(err.response?.data?.error|| "Error deleting user");
      setTimeout(() => setErrorMessage(null), 5000);
      return false;
    } finally {
      // Close modal and collapse menu
      setDeleting(false);
      setShowConfirmDelete(false);
      const collapseEl = collapseRef.current;
      if (collapseEl) {
        const instance = Collapse.getInstance(collapseEl);
        if (instance) instance.hide();
      }
    }
  };

  // Close dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event) => {
      const collapseEl = collapseRef.current;
      const toggleBtnEl = toggleButtonRef.current;

      if (
        collapseEl &&
        !collapseEl.contains(event.target) &&
        toggleBtnEl &&
        !toggleBtnEl.contains(event.target)
      ) {
        const instance = Collapse.getInstance(collapseEl);
        if (instance) instance.hide();
      }
    };

    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  // Close dropdown when pressing ESC
  useEffect(() => {
    const handleEsc = (event) => {
      if (event.key === "Escape") {
        const collapseEl = collapseRef.current;
        if (collapseEl) {
          const instance = Collapse.getInstance(collapseEl);
          if (instance) instance.hide();
        }
      }
    };
    document.addEventListener("keydown", handleEsc);
    return () => document.removeEventListener("keydown", handleEsc);
  }, []);

  // Dynamic button style
  const toggleButtonStyle = {
    width: 60,
    height: 60,
    position: "relative",
    ...(left != null ? { left: `${left}%` } : {}),
    ...(right != null ? { right: `${right}%` } : {}),
    border: "none",
    backgroundColor: "var(--bg-color)",
  };

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      <button
        ref={toggleButtonRef}
        className="btn p-0"
        type="button"
        aria-label="Open user menu"
        onClick={() => {
          const collapseEl = collapseRef.current;
          if (collapseEl) {
            const instance = Collapse.getOrCreateInstance(collapseEl);
            instance.toggle();
          }
        }}
        style={toggleButtonStyle}
        hidden={!sub}
      >
        <img
          src={profilePicture}
          alt="userPhoto"
          className="img-fluid"
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
            borderRadius: "50%",
          }}
        />
      </button>

      <div className="collapse" ref={collapseRef}>
        <div
          className="card card-body"
          style={{
            width: "300px",
            minHeight: "300px",
            maxHeight : "max-content",
            position: "absolute",
            left: "80.2%",
            zIndex: 1600,
            backgroundColor: "var(--bg-button-color)",
            overflow: "visible",
            transition: "background 0.3s ease, color 0.3s ease",
          }}
        >
          <h1 className="text-center p-3">Hi, {userName}!</h1>
          <ThemeToggle className="mb-3" />
          <Button
            className="fw-bold wb-1 p-2"
            id="sign-out-button"
            style={{ transition: "background 0.3s ease, color 0.3s ease" }}
            onClick={handleSignOut}
          >
            Sign out
          </Button>
          <hr />
          <Button
            className="fw-bold wb-1 p-2"
            id="delete-button"
            onClick={requestDelete} // open confirm modal instead of direct delete
            style={{
              border: "none",
              color: "red",
              transition: "background 0.3s ease, color 0.3s ease",
            }}
          >
            Delete
          </Button>
        </div>
      </div>

      {/* Confirm delete modal */}
      <Modal show={showConfirmDelete} onHide={cancelDelete} centered>
        <Modal.Header closeButton>
          <Modal.Title>Delete account content?</Modal.Title>
        </Modal.Header>
        <div className="p-3">
          Are you sure you want to delete the content of your account? This action cannot be undone.
        </div>
        <div className="d-flex justify-content-between align-items-center p-3 pt-0">
          <Button variant="secondary" onClick={cancelDelete}>
            Keep Account
          </Button>
          <div className="d-flex gap-2">
            <Button variant="danger" onClick={handleDeleteUser} disabled={deleting}>
              {deleting ? "Deleting..." : "Delete Account"}
            </Button>
          </div>
        </div>
      </Modal>
    </>
  );
}

UserMenu.propTypes = {
  left: PropTypes.number,
  right: PropTypes.number,
};
