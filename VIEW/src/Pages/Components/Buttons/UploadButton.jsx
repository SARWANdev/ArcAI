import "./UploadButton.css"
/**
 * UploadButton is the component that is used to display the upload button in the library page.
 * @returns {JSX} - The React component for the upload button.
 */
export default function UploadButton() {
    return (
        <div className="upload-button-container">
            <button className="upload-button" title="Upload">Upload</button>
        </div>
    )
}