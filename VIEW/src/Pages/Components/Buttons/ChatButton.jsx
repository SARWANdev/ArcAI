import "./ChatButton.css"
import { useNavigate } from 'react-router-dom';
/**
 * ChatButton is the component that is used to display the chat button.
 * @param {string} content - The content of the chat button.
 * @returns {JSX} - The React component for the chat button.
 */
function ChatButton({content}) {
    const navigate = useNavigate()
    /**
     * goToChat is the function that is used to navigate to the chat page.
     * @param {Event} e - The event that is used to prevent the default behavior of the button.
     */
    function goToChat(e) {
        if (e) e.preventDefault();
        navigate("/workspace/chat", { replace: true });
    }
    return (
        <div className="chat-container" style={content != "Chat" ? {height: "70px", width: "70px"} : {}}>
            <form>
                <button className="arcai-chat-button" onClick={goToChat} id = "chat-button"><img src="../../images/chat.png" className="image-chat-button"></img></button>
                <label htmlFor="chat-button" className="chat-label">{content}</label>
            </form>
        </div>
    )

}
export default ChatButton