import SidebarViewButton from "./SideBarToggleButton"
import LibraryButton from "./LibraryButton"
import ChatButton from "./ChatButton"
import "./MiniatureSideButtons.css"
/**
 * MiniatureSideButtons is the component that is used to display the miniature side buttons.
 * @returns {JSX} - The React component for the miniature side buttons.
 */
function MiniatureSideButtons() {
    return(
        <div className="mini-container" id = "mini-container">
            <SidebarViewButton direction = {"right"} imgsrc = "../../images/sidebar-expand.png" className = "side-bar-open-button"/>
            <LibraryButton className = "mini-library-button"/>
            <ChatButton className = "mini-chat-button"/>
        </div>
    )
}
export default MiniatureSideButtons