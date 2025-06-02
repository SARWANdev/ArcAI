import "./AIChatContainer.css"
/**
 * AIChatContainer is the component that is used to display the AI chat container in the chat page.
 * @returns {JSX} - The React component for the AI chat container.
 */
export default function AIChatContainer(){
    return(
        <form className="ai-chat-container">
            <input type="text" placeholder="Ask me anything..." className="ai-chat-container-input"/>
            <input type="file" className="ai-chat-container-file-input"/>
        </form>
    )
}