import "./DownloadButton.css"
/**
 * DownloadButton is the component that is used to display the download button in the library page.
 * @returns {JSX} - The React component for the download button.
 */
export default function DownloadButton() {
    return (
        <div className="download-button-container">
            <button className="download-button" title="Download">Download</button>
        </div>
    )
}