import "./PopUpBoxProjectOptions.css"
import DeleteButton from "./Buttons/DeleteButton"
import DownloadButton from "./Buttons/DownloadButton"
import UploadButton from "./Buttons/UploadButton"
import RenameButton from "./Buttons/RenameButton"
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