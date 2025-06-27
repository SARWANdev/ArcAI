import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import "./LoginButton.css"
/**
 * LoginButton is the component that is used to display the login button.
 * @returns {JSX} - The React component for the login button.
 */
export default function LoginButton() {
  /**
   * The react component sends the user to a login page where the user will be authenticated by giving the email address and password.
   */
  const handleLogin = () => {
    // Redirect to Flask backend's /login endpoint
    window.location.href = "http://localhost:3000/login";
  };
  
  return(
        <Button className="fs-2 fw-bold" id = "login-button" onClick={handleLogin}>Log in</Button>
    )
}