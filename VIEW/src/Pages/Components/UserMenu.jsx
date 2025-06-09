import "./UserMenu.css"
import SignOutButton from "./Buttons/SignOutButton";
/**
 * PopUpBoxSignOut is the component that is used to display the sign out pop up box.
 * @param {string} top - The top position of the pop up box.
 * @param {string} bottom - The bottom position of the pop up box.
 * @param {string} left - The left position of the pop up box.
 * @param {string} right - The right position of the pop up box.
 */
function UserMenu({top, bottom, left, right}) {
    /**
     * hideSignOutPopUp is the function that is used to hide the sign out pop up box.
     */
    const hideSignOutPopUp = () => {
        document.getElementById("user-menu-container").style.display = "";
    }
    /**
     * positionStyle is the style of the pop up box.
     */
    const positionStyle = {
    position: "absolute",
    ...(top && { top }),
    ...(bottom && { bottom }),
    ...(left && { left }),
    ...(right && { right }),
  };
  
    return(
        <div className="user-menu" id = "user-menu-container" style={positionStyle}>
            <SignOutButton/>
            <br/>
            <button className="user-menu-cancel-button" onClick={hideSignOutPopUp} title="Cancel">Cancel</button>
        </div>
    )
}
export default UserMenu