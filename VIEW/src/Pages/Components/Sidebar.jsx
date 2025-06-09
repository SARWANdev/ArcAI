import SideBarToggleButton from "./Buttons/SideBarToggleButton"
import LibraryButton from "./Buttons/LibraryButton"
import ChatButton from "./Buttons/ChatButton"
import MiniSideButtons from "./Buttons/MiniSideButtons"
import "./Sidebar.css"

/**
 * Sidebar is the component that is used to display the sidebar.
 * @returns {JSX} - The React component for the sidebar.
 */
function Sidebar() {
    return(
        <div className="side-bar-container" id="side-bar-container">
            <div id="side-bar-contents">
                <SideBarToggleButton direction = {"left"} imgsrc = "../../images/sidebar-collapse.png"/>
                <LibraryButton content = "Library"/>
                <ChatButton content = "Chat"/>
            </div>
            <MiniSideButtons/>
        </div>
    )
}
export default Sidebar