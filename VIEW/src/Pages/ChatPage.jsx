import UserMenu from "./Components/Buttons/UserMenu";
import AIChatContainer from "./Components/AIChatContainer"
import { useNavigate } from "react-router-dom";
import { Sidebar } from "./Components/Sidebar";
import "./ChatPage.css"
/**
 * ChatPage is the page that is used to display the chat with the AI.
 * @returns {JSX} - The React component for the chat page.
 */
function ChatPage() {
    const navigate = useNavigate();
    /**
     * handleChatButtonClick is the function that is used to navigate to the chat page.
     * @param {*} e 
     */
    function handleChatButtonClick(e){
        if (e) e.preventDefault();
        navigate("/home/chat-chatbot", { replace: true });
    }
    /**
     * handleHistoryButtonClick is the function that is used to navigate to the chat history page.
     * @param {*} e 
     */
    function handleHistoryButtonClick(e){
        if (e) e.preventDefault();
        navigate("/home/chat-history", { replace: true });
    }
    return(
        <>
        <div className="chat-page-container">
            <div className="chat-page-header">
                <hr className="chat-page-line"></hr>
                <div className="chat-page-header-content">
                    <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
                    <button className="chat-page-button" id = "chat-page-chat-button" onClick={handleChatButtonClick} title="Chat">Chat</button>
                    <button className="chat-page-button" id = "chat-page-history-button" onClick={handleHistoryButtonClick} title="History">History</button>
                    <UserMenu className = "chat-page-user-button" top = {"20px"} leftMenu = {"83.5%"} topMenu = {"15%"}/>
                </div>
                <hr className="chat-page-line"></hr>
                <div className="chat-page-content">
                    <Sidebar/>
                    <div className="chat-page-content-container" id = "chat-page-content-container">
                        <h1 className="chat-page-content-container-title">What can I help with?</h1>
                        <AIChatContainer/>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}
export default ChatPage