import "./UserAvatar.css"
/**
 * UserAvatar is the component that is used to display the user avatar.
 * @param {string} top - The top position of the user picture.
 * @param {string} bottom - The bottom position of the user picture.
 * @param {string} left - The left position of the user picture.
 * @param {string} right - The right position of the user picture.
 */
function UserAvatar({top, bottom, left, right}) {
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
    
    return(
        <>
        <button className="user-avatar" id = "user-avatar" onClick={showSignOutPopUp} style={positionImage} title="User Avatar">
            <img src = "../images/userPhoto.jpg" alt = "userPhoto" className="user-avatar-image" style={{width: "60px", height: "60px"}}></img></button>
        </>
    )
}
export default UserAvatar