import DeleteButton from "./Buttons/DeleteButton"
import RenameButton from "./Buttons/RenameButton"
import DuplicateButton from "./Buttons/DuplicateButton"
import ExportBibtex from "./Buttons/ExportBibtex"
import MoveButton from "./Buttons/MoveButton"
import "./PopUpBoxDocumentsOptions.css"
export default function PopUpBoxDocumentsOptions() {
    return (
        <div className="pop-up-box-documents-options" id = "documents-options-container">
            <DeleteButton/>
            <DuplicateButton/>
            <ExportBibtex/>
            <MoveButton/>
            <RenameButton/>
        </div>
    )
}