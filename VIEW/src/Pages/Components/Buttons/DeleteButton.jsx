import "./DeleteButton.css"
/**
 * DeleteButton is the component that is used to display the delete button in the library page and chat history page.
 * @returns {JSX} - The React component for the delete button.
 */
export default function DeleteButton() {
    return (
        <div className="delete-button-container">
            <button className="delete-button" title="Delete">Delete</button>
        </div>
    )
}