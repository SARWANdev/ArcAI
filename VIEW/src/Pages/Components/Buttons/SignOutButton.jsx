import "./SignOutButton.css"
import { useAuth } from "../AuthContext";
/**
 * SignOutButton is the component that is used to display the sign out button.
 * @returns {JSX} - The React component for the sign out button.
 */
function SignOutButton() {
    const { setIsAuthenticated } = useAuth();
    /**
     * signOut is the function that is used to sign out the user.
     */
    function signOut(){
        window.location.href = "http://localhost:3000/logout";
        setIsAuthenticated(false);
    }
    return(
        <button onClick={signOut} className = "sign-out-button" title="Sign out">Sign out</button>
    )
}
export default SignOutButton