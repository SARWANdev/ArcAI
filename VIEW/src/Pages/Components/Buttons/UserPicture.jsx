import "./UserPicture.css"
/**
 * UserPicture is the component that is used to display the user picture.
 * @param {string} top - The top position of the user picture.
 * @param {string} bottom - The bottom position of the user picture.
 * @param {string} left - The left position of the user picture.
 * @param {string} right - The right position of the user picture.
 */
function UserPicture({top, bottom, left, right}) {
    console.log(top, bottom, left, right)
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
        document.getElementById("sign-out-container").style.display = "flex";
    }
    /**
     * To hide the sign out pop up when the user clicks outside of it.
     */
    document.addEventListener('mouseup', function(e) {
    var container = document.getElementById("sign-out-container");
    if (!container.contains(e.target)) {
        container.style.display = 'none';
    }
    });
    
    return(
        <>
        <button className="userButton" id = "userButton" onClick={showSignOutPopUp} style={positionImage}>
            <img src = "../images/userPhoto.jpg" alt = "userPhoto" className="userImage" style={{width: "60px", height: "60px"}}></img></button>
        </>
    )
}
export default UserPicture