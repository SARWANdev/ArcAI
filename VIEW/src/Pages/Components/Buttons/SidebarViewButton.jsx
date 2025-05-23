import "./SidebarViewButton.css";
/**
 * SidebarViewButton is the component that is used to display the sidebar view button.
 * @param {string} direction - The direction of the sidebar view button.
 * @param {string} imgsrc - The source of the image of the sidebar view button.
 * @returns {JSX} - The React component for the sidebar view button.
 */
function SidebarViewButton({direction, imgsrc}) {
    let nextDirection = direction;

    /**
     * goLeft is the function that is used to push the sidebar to the left direction.
     */
    function goLeft() {
        const sidebar = document.getElementById("side-bar-container");
        const sidebarButtons = document.getElementById("side-bar-contents");
        sidebar.style.transition = "transform 0.3s ease";
        // Apply the transform
        sidebar.style.transform = "translateX(-80%)";

        const miniSideBar = document.getElementById("mini-container");
        miniSideBar.style.display = "block";
        sidebarButtons.style.display = "none";
    }

    /**
     * goRight is the function that is used to push the sidebar to the right direction.
     */
    function goRight() {
        const sidebar = document.getElementById("side-bar-container");
        const sidebarButtons = document.getElementById("side-bar-contents");
        sidebar.style.transition = "transform 0.3s ease";
        // Apply the transform
        sidebar.style.transform = "translateX(0%)";
        const miniSideBar = document.getElementById("mini-container");
        miniSideBar.style.display = "none";
        sidebarButtons.style.display = "block";
    }
    
    return(
        <button className="side-bar-button"><img className = "image-side-bar-button" src = {imgsrc} alt="collapse sidebar view" onClick={ nextDirection == "right" ? goRight : goLeft}></img></button>
    )
}
export default SidebarViewButton