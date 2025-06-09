import DeleteButton from "./Buttons/DeleteButton"
import RenameButton from "./Buttons/RenameButton"
import DuplicateButton from "./Buttons/DuplicateButton"
import ExportBibtex from "./Buttons/ExportBibtex"
import MoveButton from "./Buttons/MoveButton"
import "./DocumentsActionMenu.css"
/**
 * PopUpBoxDocumentsOptions is the component that is used to display the pop up box for the documents options.
 * @returns {JSX} - The React component for the pop up box for the documents options.
 */
export default function DocumentsActionMenu() {
    return (
        <div className="documents-action-menu" id = "documents-action-menu-container">
            <DeleteButton/>
            <DuplicateButton/>
            <ExportBibtex/>
            <MoveButton/>
            <RenameButton/>
        </div>
    )
}