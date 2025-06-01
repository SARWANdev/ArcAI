import DeleteButton from "./Buttons/DeleteButton"
import RenameButton from "./Buttons/RenameButton"
import DuplicateButton from "./Buttons/DuplicateButton"
import "./PopUpBoxDocumentsOptions.css"
export default function PopUpBoxDocumentsOptions() {
    return (
        <div className="pop-up-box-documents-options" id = "documents-options-container">
            <DeleteButton/>
            <DuplicateButton/>
            <RenameButton/>
        </div>
    )
}