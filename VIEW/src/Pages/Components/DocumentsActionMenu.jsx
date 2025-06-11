import DeleteButton from "./Buttons/DeleteButton"
import RenameButton from "./Buttons/RenameButton"
import DuplicateButton from "./Buttons/DuplicateButton"
import ExportBibtexButton from "./Buttons/ExportBibtexButton"
import MoveButton from "./Buttons/MoveButton"
import "./DocumentsActionMenu.css"
/**
 * DocumentsActionMenu is the component that is used to display the pop up box for the documents options.
 * @returns {JSX} - The React component for the pop up box for the documents options.
 */
export default function DocumentsActionMenu() {
    return (
        <div className="documents-action-menu" id = "documents-action-menu-container">
            <DeleteButton/>
            <DuplicateButton/>
            <ExportBibtexButton/>
            <MoveButton/>
            <RenameButton/>
        </div>
    )
}