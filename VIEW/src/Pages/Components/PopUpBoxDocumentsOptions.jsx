import DeleteButton from "./Buttons/DeleteButton"
import RenameButton from "./Buttons/RenameButton"
import DuplicateButton from "./Buttons/DuplicateButton"
import ExportBibtex from "./Buttons/ExportBibtex"
import "./PopUpBoxDocumentsOptions.css"
export default function PopUpBoxDocumentsOptions() {
    return (
        <div className="pop-up-box-documents-options" id = "documents-options-container">
            <DeleteButton/>
            <DuplicateButton/>
            <ExportBibtex/>
            <RenameButton/>
        </div>
    )
}