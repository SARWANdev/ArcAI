import { useAuth } from "../AuthContext";
import { Collapse } from "bootstrap/dist/js/bootstrap.bundle.min";
import { useRef, useEffect } from "react";

export default function UserMenu({ left = null, right = null }) {
  const { setIsAuthenticated, user } = useAuth();
  const collapseRef = useRef(null);
  const toggleButtonRef = useRef(null);
  const profilePicture = user?.picture || "../images/default-avatar.png";

  function signOut() {
    window.location.href = "http://localhost:3000/logout";
    setIsAuthenticated(false);
  }

  const hideSignOutPopUp = () => {
    const collapseElement = document.getElementById("userMenu");
    const collapseInstance = Collapse.getOrCreateInstance(collapseElement);
    collapseInstance.hide();
  };

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
        <div className="card card-body" style={{width:"115px", position: "absolute", left :"87.2%", zIndex: 1000}}>
          <a href="#" className="dropdown-item dropdown-item-custom" style={{cursor: "pointer"}}>Dark mode</a>
          <a href="#" className="dropdown-item dropdown-item-custom" style={{cursor: "pointer"}} onClick={hideSignOutPopUp}>Cancel</a>
          <hr></hr>
          <a href="#" className="dropdown-item dropdown-item-custom" style={{cursor: "pointer"}} onClick={signOut}>Sign out</a>
        </div>
      </div>
    </>
  );
}
