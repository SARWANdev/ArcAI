import "./AIChatContainer.css"
export default function AIChatContainer(){
    return(
        <form className="ai-chat-container">
            <input type="text" placeholder="Ask me anything..." className="ai-chat-container-input"/>
            <input type="file" className="ai-chat-container-file-input"/>
        </form>
    )
}