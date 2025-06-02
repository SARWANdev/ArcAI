import DeleteButton from "./Buttons/DeleteButton";
import RenameButton from "./Buttons/RenameButton";
import "./PopUpBoxChatHistoryOptions.css"
export default function PopUpBoxChatHistoryOptions(){
    return(
        <div className="pop-up-box-chat-history-options">
            <DeleteButton/>
            <RenameButton/>
        </div>
    )
}