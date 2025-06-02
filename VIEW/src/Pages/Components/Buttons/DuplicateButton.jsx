import "./DuplicateButton.css"
/**
 * DuplicateButton is the component that is used to display the duplicate button in the library page.
 * @returns {JSX} - The React component for the duplicate button.
 */
export default function DuplicateButton() {
    return (
        <div className="duplicate-button-container">
            <button className="duplicate-button" title="Duplicate">Duplicate</button>
        </div>
    )
}