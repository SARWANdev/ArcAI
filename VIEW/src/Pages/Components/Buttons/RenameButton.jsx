import { Button } from "react-bootstrap"
/**
 * RenameButton is the component that is used to display the rename button in the document viewer page and the chat page.
 * @returns {JSX} - The React component for the rename button.
 */
export default function RenameButton() {
    return (
        <Button className="btn btn-light" title="rename">Rename</Button>
    )
}