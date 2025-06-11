import DeleteButton from "./Buttons/DeleteButton";
import RenameButton from "./Buttons/RenameButton";
import "./ChatHistoryActionMenu.css"
/**
 * ChatHistoryActionMenu is the component that is used to display the pop up box for the chat history options.
 * @returns {JSX} - The React component for the pop up box for the chat history options.
 */
export default function ChatHistoryActionMenu(){
    return(
        <div className="chat-history-action-menu">
            <DeleteButton/>
            <RenameButton/>
        </div>
    )
}