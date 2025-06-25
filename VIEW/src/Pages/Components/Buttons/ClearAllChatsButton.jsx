import { Button } from "react-bootstrap"
import "./ClearAllChatsButton.css"
/**
 * ClearAllChatsButton is the component that is used to display the clear all button in the chat history page.
 * @returns {JSX} - The React component for the clear all chats button.
 */
export default function ClearAllChatsButton(){
    return(
        <Button className="btn" title="Clear all" id = "btn">Clear All</Button>
    )
}