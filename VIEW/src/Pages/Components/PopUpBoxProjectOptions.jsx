import "./PopUpBoxProjectOptions.css"
import DeleteButton from "./Buttons/DeleteButton"
import DownloadButton from "./Buttons/DownloadButton"
export default function PopUpBoxProjectOptions() {
    return (
        <div className="pop-up-box-project-options" id = "project-options-container">
            <DeleteButton/>
            <DownloadButton/>
        </div>
    )
}