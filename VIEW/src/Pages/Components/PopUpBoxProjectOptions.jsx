import "./PopUpBoxProjectOptions.css"
import DeleteButton from "./Buttons/DeleteButton"
import DownloadButton from "./Buttons/DownloadButton"
import UploadButton from "./Buttons/UploadButton"
import RenameButton from "./Buttons/RenameButton"
/**
 * PopUpBoxProjectOptions is the component that is used to display the pop up box for the project options.
 * @returns {JSX} - The React component for the pop up box for the project options.
 */
export default function PopUpBoxProjectOptions() {
    return (
        <div className="pop-up-box-project-options" id = "project-options-container">
            <DeleteButton/>
            <DownloadButton/>
            <UploadButton/>
            <RenameButton/>
        </div>
    )
}