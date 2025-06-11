import SignOutButton from "./SignOutButton";
import "./UserMenu.css"
/**
 * UserMenu is the component that is used to display the user picture which acts as a button and when clicked opens a pop up box
 * for the user, if the user wants to sign out or click close button.
 * @param {string} top - The top position of the user picture.
 * @param {string} bottom - The bottom position of the user picture.
 * @param {string} left - The left position of the user picture.
 * @param {string} right - The right position of the user picture.
 */
export default function UserMenu({top, bottom, left, right, topMenu, bottomMenu, leftMenu, rightMenu}) {
    /**
     * positionImage positions the user picture.
     */
    const positionImage = {
    position: "relative",
    ...(top && { top }),
    ...(bottom && { bottom }),
    ...(left && { left }),
    ...(right && { right }),
  };

    /**
     * showSignOutPopUp is the function that is used to show the sign out pop up.
     */
    const showSignOutPopUp = () => {
        document.getElementById("user-menu-container").style.display = "flex";
    }
    /**
     * To hide the sign out pop up when the user clicks outside of it.
     */
    document.addEventListener('mouseup', function(e) {
    if (!document.getElementById("user-menu-container").contains(e.target)) {
        document.getElementById("user-menu-container").style.display = 'none';
    }
    });


    const hideSignOutPopUp = () => {
        document.getElementById("user-menu-container").style.display = "";
    }
    /**
     * positionStyle is the style of the pop up box.
     */
    const positionStyle = {
        position: "absolute",
        ...(topMenu && { top: topMenu }),
        ...(bottomMenu && { bottom: bottomMenu }),
        ...(leftMenu && { left: leftMenu }),
        ...(rightMenu && { right: rightMenu }),
      };
    console.log(leftMenu)
    console.log(topMenu)
    return(
        <>
        <button className="user-avatar" id = "user-avatar" onClick={showSignOutPopUp} style={positionImage} title="User Avatar">
            <img src = "../images/userPhoto.jpg" alt = "userPhoto" className="user-avatar-image" style={{width: "60px", height: "60px"}}></img></button>
        <div className="user-menu" id = "user-menu-container" style={positionStyle}>
            <SignOutButton/>
            <br/>
            <button className="user-menu-cancel-button" onClick={hideSignOutPopUp} title="Cancel">Cancel</button>
        </div>
        </>
    )
}
