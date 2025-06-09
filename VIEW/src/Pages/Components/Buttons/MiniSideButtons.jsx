import SidebarToggleButton from "./SideBarToggleButton"
import LibraryButton from "./LibraryButton"
import ChatButton from "./ChatButton"
import "./MiniSideButtons.css"
/**
 * MiniSideButtons is the component that is used to display the miniature side buttons.
 * @returns {JSX} - The React component for the miniature side buttons.
 */
function MiniSideButtons() {
    return(
        <div className="mini-side-buttons-container" id = "mini-side-buttons-container">
            <SidebarToggleButton direction = {"right"} imgsrc = "../../images/sidebar-expand.png" className = "side-bar-open-button"/>
            <LibraryButton className = "mini-library-button"/>
            <ChatButton className = "mini-chat-button"/>
        </div>
    )
}
export default MiniSideButtons