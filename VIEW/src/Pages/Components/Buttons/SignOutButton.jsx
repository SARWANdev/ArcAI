import "./SignOutButton.css"
import { useNavigate } from 'react-router-dom';
/**
 * SignOutButton is the component that is used to display the sign out button.
 * @returns {JSX} - The React component for the sign out button.
 */
function SignOutButton() {
    //Should come under backend
    const navigate = useNavigate()
    /**
     * signOut is the function that is used to sign out the user.
     */
    function signOut(){
        localStorage.setItem("ifLogged", null);
        navigate("/");
    }
    return(
        <button onClick={signOut} className = "sign-out-button">Sign out</button>
    )
}
export default SignOutButton