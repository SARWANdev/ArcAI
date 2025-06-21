import UserMenu from "./Components/Buttons/UserMenu"
import "bootstrap/dist/css/bootstrap.min.css";
import { useNavigate } from 'react-router-dom';
import { Button } from "react-bootstrap"
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
// Create a drop down button which will contain the required commands
/**
 * HomePage is the page that is used to display the home page when the user is logged in.
 * @returns {JSX} - The React component for the home page when the user is logged in.
 */
function HomePage(){
    const navigate = useNavigate()
    /**
     * goToLibrary is the function that is used to navigate to the library page.
     */
    function goToLibrary() {
        navigate("/home/library")
    }

    return(
      <div className="container-fluid py-2">
        <div className="row justify-content-between align-items-center">
          <img src="../images/arcai-logo.png" alt="logo" className="img-fluid mb-4 p-0" style={{ width: "115px", height: "128px", position: "relative", left: "8.6%" }} />
          <UserMenu/>
        </div>

        <hr className="mb-5 w-100" />

        <main className="text-center">
          <div className="mb-5">
            <h2 className="fw-bold display-3">
              Your research,<br />supercharged by AI
            </h2>
            <p className="text-muted fs-1 fw-bold">Upload. Chat. Write. Cite.</p>
          </div>

          <div className="row justify-content-center g-4 mb-5">
            <div className="col-12 col-md-6 col-lg-5" style={{height : 150}}>
              <div className="d-flex align-items-center border rounded p-3 h-100">
                <img
                  src="../images/book.png"
                  alt="book"
                  className="img-fluid me-3"
                  style={{ width: "68px", height: "68px" }}
                />
                <div className="text-start">
                  <h5 className="mb-1 fw-bold fs-2">My Library</h5>
                  <p className="mb-0 text-muted fs-4">Organize and browse your PDFs</p>
                </div>
              </div>
            </div>

            <div className="col-12 col-md-6 col-lg-5">
              <div className="d-flex align-items-center border rounded p-3 h-100">
                <img
                  src="../images/chat.png"
                  alt="chat"
                  className="img-fluid me-3"
                  style={{ width: "68px", height: "68px" }}
                />
                <div className="text-start">
                  <h5 className="mb-1 fw-bold fs-2">Chat</h5>
                  <p className="mb-0 text-muted fs-4">Ask Questions & summarize papers</p>
                </div>
              </div>
            </div>
          </div>
          <Button className="fs-2 fw-bold" style={{width : 250, height: 70}} onClick={goToLibrary}>Go to Library</Button>
        </main>
      </div>
    )
}
export default HomePage