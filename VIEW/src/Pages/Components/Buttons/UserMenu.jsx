import { useAuth } from "../AuthContext";
import { Collapse } from "bootstrap/dist/js/bootstrap.bundle.min";
import { useRef, useEffect } from "react";
import { Button } from "react-bootstrap";
import ThemeToggle from "./ThemeToggle"
import "./UserMenu.css"

export default function UserMenu({ left = null, right = null }) {
  const { setIsAuthenticated, user } = useAuth();
  const collapseRef = useRef(null);
  const toggleButtonRef = useRef(null);
  const profilePicture = user?.picture || "../images/default-avatar.png";
  const userName = user?.given_name || "User"

  function signOut() {
    window.location.href = "http://localhost:3000/logout";
    setIsAuthenticated(false);
  }

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

  const toggleButtonStyle = {
    width: 60,
    height: 60,
    position: "relative",
    ...(left != null ? { left: `${left}%` } : {}),
    ...(right != null ? { right: `${right}%` } : {}),
  };

  return (
    <>
      <button
        ref={toggleButtonRef}
        className="btn p-0"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#userMenu"
        aria-expanded="false"
        aria-controls="userMenu"
        style={toggleButtonStyle}
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

      <div className="collapse" id="userMenu" ref={collapseRef}>
        <div className="card card-body" style={{width:"300px", height: "300px", position: "absolute", left :"80.2%", zIndex: 1000, backgroundColor: "var(--bg-button-color)", transition: "background 0.3s ease, color 0.3s ease"}}>
          <h1 className="text-center p-3">Hi, {userName}!</h1>
          <ThemeToggle/>
          <Button className="fw-bold wb-1 p-2" id = "sign-out-button" style = {{transition: "background 0.3s ease, color 0.3s ease"}}onClick={signOut}>Sign out</Button>
          <hr></hr>
          <Button className="fw-bold wb-1 p-2" id = "delete-button" style={{border: "none", color: "red", transition: "background 0.3s ease, color 0.3s ease"}}>Delete</Button>
        </div>
      </div>
    </>
  );
}
