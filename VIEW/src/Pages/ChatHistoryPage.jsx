import { useNavigate } from "react-router-dom";
import UserMenu from "./Components/Buttons/UserMenu";
import ClearAllChatsButton from "./Components/Buttons/ClearAllChatsButton";
import { Sidebar } from "./Components/Sidebar";
import "./ChatHistoryPage.css";
/**
 * ChatHistoryPage is the page that is used to display the chat history page.
 * @returns {JSX} - The React component for the chat history page.
 */
export default function ChatHistoryPage() {
    const navigate = useNavigate();
    /**
     * handleChatButtonClick is the function that is used to navigate to the chat page.
     * @param {*} e - The event object.
     */
    function handleChatButtonClick(e){
        if (e) e.preventDefault();
        navigate("/home/chat-chatbot", { replace: true });
    }
    /**
     * handleHistoryButtonClick is the function that is used to navigate to the chat history page.
     * @param {*} e - The event object.
     */
    function handleHistoryButtonClick(e){
        if (e) e.preventDefault();
        navigate("/home/chat-history", { replace: true });
    }
    
    return(
        <>
        <div className="chat-history-page-container">
            <div className="chat-history-page-header">
                <hr className="chat-history-page-line"></hr>
                <div className="chat-history-page-header-content">
                    <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
                    <button className="chat-history-page-button" id = "chat-history-page-chat-button" onClick={handleChatButtonClick} title="Chat">Chat</button>
                    <button className="chat-history-page-button" id = "chat-history-page-history-button" onClick={handleHistoryButtonClick} title="History">History</button>
                    <UserMenu className = "chat-history-page-user-button" top = {"20px"} leftMenu = {"83.5%"} topMenu = {"15%"}/>
                </div>
                <hr className="chat-history-page-line"></hr>
                <div className="chat-history-page-content">
                    <Sidebar/>
                    <div className="chat-history-page-content-container" id = "chat-history-page-content-container">
                        <ClearAllChatsButton/>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}
