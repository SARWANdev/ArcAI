import "./RenameButton.css"
/**
 * RenameButton is the component that is used to display the rename button in the document viewer page and the chat page.
 * @returns {JSX} - The React component for the rename button.
 */
export default function RenameButton() {
    return (
        <div className="rename-button-container">
            <button className="rename-button" title="Rename">Rename</button>
        </div>
    )
}