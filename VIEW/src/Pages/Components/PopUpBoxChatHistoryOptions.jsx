import DeleteButton from "./Buttons/DeleteButton";
import RenameButton from "./Buttons/RenameButton";
import "./PopUpBoxChatHistoryOptions.css"
/**
 * PopUpBoxChatHistoryOptions is the component that is used to display the pop up box for the chat history options.
 * @returns {JSX} - The React component for the pop up box for the chat history options.
 */
export default function PopUpBoxChatHistoryOptions(){
    return(
        <div className="pop-up-box-chat-history-options">
            <DeleteButton/>
            <RenameButton/>
        </div>
    )
}