import "./SideBarToggleButton.css";
import {useContext} from "react"
import {IDContext} from "../../LibraryPage"
/**
 * SideBarToggleButton is the component that is used to display the sidebar view button.
 * @param {string} direction - The direction of the sidebar view button.
 * @param {string} imgsrc - The source of the image of the sidebar view button.
 * @returns {JSX} - The React component for the sidebar view button.
 */
function SideBarToggleButton({direction, imgsrc}) {
    let nextDirection = direction;
    const id = useContext(IDContext);
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
        miniSideBar.style.display = "flex";
        miniSideBar.style.flexDirection = "column";
        miniSideBar.style.gap = "20px";
        sidebarButtons.style.display = "none";

        const libraryPageContentContainer = document.getElementById(id);
        libraryPageContentContainer.style.display = "flex";
        libraryPageContentContainer.style.alignItems = "center";
        libraryPageContentContainer.style.transition = "width 2s ease";
        libraryPageContentContainer.style.transform = "translateX(-30.8%)";
        libraryPageContentContainer.style.width = "1170px";
    }

    /**
     * goRight is the function that is used to push the sidebar to the right direction.
     */
    function goRight() {
        const sidebar = document.getElementById("side-bar-container");
        const sidebarButtons = document.getElementById("side-bar-contents");
        sidebar.style.transition = "transform 0.3s ease";
        
        sidebar.style.transform = "translateX(0%)";
        const miniSideBar = document.getElementById("mini-container");
        miniSideBar.style.display = "none";
        sidebarButtons.style.display = "flex";
        sidebarButtons.style.flexDirection = "column";

        const libraryPageContentContainer = document.getElementById(id);
        libraryPageContentContainer.style.display = "flex";
        libraryPageContentContainer.style.alignItems = "center";
        libraryPageContentContainer.style.transition = "width 2s ease";
        libraryPageContentContainer.style.transform = "translateX(0%)";
        libraryPageContentContainer.style.width = "911px";
    }
    
    return(
        <button className="side-bar-toggle-button" title={nextDirection == "right" ? "Collapse sidebar view" : "Expand sidebar view"}><img className = "image-side-bar-toggle-button" src = {imgsrc} alt="collapse sidebar view" onClick={ nextDirection == "right" ? goRight : goLeft}></img></button>
    )
}
export default SideBarToggleButton