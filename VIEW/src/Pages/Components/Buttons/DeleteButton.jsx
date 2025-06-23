import { Button } from "react-bootstrap";
/**
 * DeleteButton is the component that is used to display the delete button in the library page and chat history page.
 * @returns {JSX} - The React component for the delete button.
 */
export default function DeleteButton() {
    return (
        <Button className="btn btn-light" title= "Delete">Delete</Button>
    )
}