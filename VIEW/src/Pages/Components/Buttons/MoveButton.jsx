import "./MoveButton.css"
/**
 * MoveButton is the component that is used to display the move button in the library page.
 * @returns {JSX} - The React component for the move button.
 */
export default function MoveButton() {
    return (
        <div className="move-button-container">
            <button className="move-button" title="Move">Move</button>
        </div>
    )
}