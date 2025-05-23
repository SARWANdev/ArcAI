import SidebarViewButton from "./Buttons/SidebarViewButton"
import LibraryButton from "./Buttons/LibraryButton"
import ChatButton from "./Buttons/ChatButton"
import MiniatureSideButtons from "./Buttons/MiniatureSideButtons"
import "./Sidebar.css"

/**
 * Sidebar is the component that is used to display the sidebar.
 * @returns {JSX} - The React component for the sidebar.
 */
function Sidebar() {
    return(
        <div className="side-bar-container" id="side-bar-container">
            <div id="side-bar-contents">
                <SidebarViewButton direction = {"left"} imgsrc = "../../images/sidebar-collapse.png"/>
                <LibraryButton content = "Library"/>
                <ChatButton content = "Chat"/>
            </div>
            <MiniatureSideButtons/>
        </div>
    )
}
export default Sidebar