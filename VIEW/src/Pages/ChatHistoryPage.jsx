import { useNavigate } from "react-router-dom";
import UserAvatar from "./Components/Buttons/UserAvatar";
import PopUpBoxSignOut from "./Components/PopUpBoxSignOut";
import Sidebar from "./Components/Sidebar";
import { IDContext } from "./LibraryPage";
import ClearAllButton from "./Components/Buttons/ClearAllButton";
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
        navigate("/workspace/chat-chatbot", { replace: true });
    }
    /**
     * handleHistoryButtonClick is the function that is used to navigate to the chat history page.
     * @param {*} e - The event object.
     */
    function handleHistoryButtonClick(e){
        if (e) e.preventDefault();
        navigate("/workspace/chat-history", { replace: true });
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
                    <UserAvatar className = "chat-history-page-user-button" top = {"20px"}/>
                </div>
                <PopUpBoxSignOut left = {"83.5%"} top = {"15%"}/>
                <hr className="chat-history-page-line"></hr>
                <div className="chat-history-page-content">
                    <div className="chat-history-page-content-container" id = "chat-history-page-content-container">
                        <ClearAllButton/>
                    </div>
                    <IDContext.Provider value = {"chat-history-page-content-container"}>
                        <Sidebar/>
                    </IDContext.Provider>
                </div>
            </div>
        </div>
        </>
    )
}
