import UserMenu from "./Components/Buttons/UserMenu";
import AIChatContainer from "./Components/AIChatContainer"
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";
import { Sidebar } from "./Components/Sidebar";
/**
 * ChatPage is the page that is used to display the chat with the AI.
 * @returns {JSX} - The React component for the chat page.
 */
export default function ChatPage() {
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
        <div className="container-fluid py-2">
            {/* Header: Logo and User Menu */}
            <div className="row justify-content-between align-items-center px-3">
                <div className="col-auto">
                    <img
                        src="../images/arcai-logo.png"
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px", position: "relative", right: "16px"}}
                    />
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "white", color: "black" , border: "none"}} onClick={handleChatButtonClick}>Chat</Button>
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "white", color: "grey", border: "none"}} onClick={handleHistoryButtonClick}>History</Button>
                </div>
                <UserMenu right = {7.5}/>
            </div>

            <hr className="mb-0" style={{marginTop: "16px"}}/>

            {/* Main Layout: Sidebar and Content */}
            <div className="row flex-nowrap">
                <div className="col-auto">
                    <Sidebar />
                </div>

                <div className="col px-4">
                    <h1 className="fs-1 fw-bold mb-4">What can I help with?</h1>
                    <AIChatContainer/>
                </div>
            </div>
        </div>
        </>
    )
}