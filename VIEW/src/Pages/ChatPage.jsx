import UserPicture from "./Components/Buttons/UserPicture"
import PopUpBoxSignOut from "./Components/Buttons/PopUpBoxSignOut"
import Sidebar from "./Components/Sidebar"
import "./ChatPage.css"
import { IDContext } from "./LibraryPage"
import { useNavigate } from "react-router-dom";
/**
 * ChatPage is the page that is used to display the chat page.
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
        navigate("/workspace/chat-chatbot", { replace: true });
    }
    /**
     * handleHistoryButtonClick is the function that is used to navigate to the chat history page.
     * @param {*} e 
     */
    function handleHistoryButtonClick(e){
        if (e) e.preventDefault();
        navigate("/workspace/chat-history", { replace: true });
    }
    return(
        <>
        <div className="chat-page-container">
            <div className="chat-page-header">
                <hr className="chat-page-line"></hr>
                <div className="chat-page-header-content">
                    <h1 className="arcai-logo">ArcAI</h1>
                    <button className="chat-page-button" id = "chat-page-chat-button" onClick={handleChatButtonClick} title="Chat">Chat</button>
                    <button className="chat-page-button" id = "chat-page-history-button" onClick={handleHistoryButtonClick} title="History">History</button>
                    <UserPicture className = "chat-page-user-button" right = {"12.8px"}/>
                    <PopUpBoxSignOut left = {"82%"} top = {"15%"}/>
                </div>
                <hr className="chat-page-line"></hr>
                <div className="chat-page-content">
                    <div className="chat-page-content-container" id = "chat-page-content-container">
                        <h1 className="chat-page-content-container-title">What can I help with?</h1>
                    </div>
                    <IDContext.Provider value = {"chat-page-content-container"}>
                        <Sidebar/>
                    </IDContext.Provider>
                </div>
            </div>
        </div>
        </>
    )
}
export default ChatPage