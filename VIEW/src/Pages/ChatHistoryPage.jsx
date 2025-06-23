import { useNavigate } from "react-router-dom";
import UserMenu from "./Components/Buttons/UserMenu";
import ClearAllChatsButton from "./Components/Buttons/ClearAllChatsButton";
import { Sidebar } from "./Components/Sidebar";
import { Button } from "react-bootstrap";
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
        <div className="container-fluid py-2">
            {/* Header: Logo and User Menu */}
            <div className="row justify-content-between align-items-center px-3">
                <div className="col-auto">
                    <img
                        src="../images/arcai-logo.png"
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px", position: "relative", right: "16px" }}
                    />
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "white", color: "grey" , border: "none"}} onClick={handleChatButtonClick}>Chat</Button>
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "white", color: "black", border: "none"}} onClick={handleHistoryButtonClick}>History</Button>
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
                    <div className="d-flex justify-content-end mt-4">
                        <ClearAllChatsButton/>
                    </div>
                </div>
            </div>
        </div>
        </>
    )
}
