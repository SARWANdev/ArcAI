import UserMenu from "./Components/Buttons/UserMenu"
import "bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from 'react-router-dom';
import { Button } from "react-bootstrap"
import { useContext } from "react";
import { ThemeContext } from "./Components/ThemeContext";
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import "./HomePage.css"
// Create a drop down button which will contain the required commands
/**
 * HomePage is the page that is used to display the home page when the user is logged in.
 * @returns {JSX} - The React component for the home page when the user is logged in.
 */
export default function HomePage(){
    const { theme } = useContext(ThemeContext);
    const navigate = useNavigate()
    /**
     * goToLibrary is the function that is used to navigate to the library page.
     */
    function goToLibrary() {
        navigate("/home/library")
    }

    return(
      <div className="container-fluid vh-100 d-flex flex-column p-0 overflow-hidden">
        <div className="row justify-content-between align-items-center mx-0 px-4 py-3">
                <div className="col-auto">
                    <img
                        src={theme === "dark" ? "../images/b0e06.png" : "../images/arcai-logo-light-theme.png"}
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px" }}
                    />
                </div>
                <div className="col-auto">
                    <UserMenu right={7.5} />
                </div>
            </div>

            <hr className="my-0" />

        <main className="text-center">
          <div className="mb-5">
            <h2 className="fw-bold display-3">
              Your research,<br />supercharged by AI
            </h2>
            <p className="fs-1 fw-bold" style={{color: "var(--text-secondary-color)"}}>Upload. Chat. Write. Cite.</p>
          </div>

          <div className="row justify-content-center g-4 mb-5">
            <div className="col-12 col-md-6 col-lg-5" style={{height : 150}}>
              <div className="d-flex align-items-center border rounded p-3 h-100">
                <img
                  src={theme === "dark" ? "../images/library-dark-theme.png" : "../images/library-light-theme.png"}
                  alt="book"
                  className="img-fluid me-3"
                  style={{ width: "68px", height: "68px", transition: "background 0.3s ease, color 0.3s ease"}}
                />
                <div className="text-start">
                  <h5 className="mb-1 fw-bold fs-2">My Library</h5>
                  <p className="mb-0 fs-4" style={{color: "var(--text-secondary-color)"}}>Organize and browse your PDFs</p>
                </div>
              </div>
            </div>

            <div className="col-12 col-md-6 col-lg-5">
              <div className="d-flex align-items-center border rounded p-3 h-100">
                <img
                  src={theme === "dark" ? "../images/chat-dark-theme.png" : "../images/chat-light-theme.png"}
                  alt="chat"
                  className="img-fluid me-3"
                  style={{ width: "68px", height: "68px", transition: "background 0.3s ease, color 0.3s ease"}}
                />
                <div className="text-start">
                  <h5 className="mb-1 fw-bold fs-2">Chat</h5>
                  <p className="mb-0 fs-4" style={{color: "var(--text-secondary-color)"}}>Ask Questions & summarize papers</p>
                </div>
              </div>
            </div>
          </div>
          <Button className="fs-2 fw-bold" id = "go-to-library-button" onClick={goToLibrary}>Go to Library</Button>
        </main>
      </div>
    )
}