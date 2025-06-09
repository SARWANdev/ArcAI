import { useNavigate } from 'react-router-dom';
import "./LoginButton.css"
/**
 * LoginButton is the component that is used to display the login button.
 * @returns {JSX} - The React component for the login button.
 */
function LoginButton() {
  const navigate = useNavigate()
  // For now set the ifLogged to true
  window.localStorage.setItem("ifLogged", "true");
  
  return(
        <button className="arcai-login-button" onClick={() => navigate("/home")} title="Log in">Log in</button>
    )
}
export default LoginButton