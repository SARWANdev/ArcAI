import LoginButton from "./Components/Buttons/LoginButton";
import "bootstrap/dist/css/bootstrap.min.css";
/**
 * LoginPage is the page that is used to display the login page of the application
 * @returns {JSX} - The React component for the Login page.
 */
export default function LoginPage() {
  return (
    <div className="container-fluid py-2">
        <div className="col-auto">
            <img src="../images/arcai-logo.png" alt="logo" className="img-fluid" style={{ width: "115px", height: "128px"}} />
        </div>

      <hr className="mb-5" />

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
        <LoginButton />
      </main>
    </div>
  );
}