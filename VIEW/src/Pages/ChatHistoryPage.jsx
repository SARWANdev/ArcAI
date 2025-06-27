import { useNavigate } from "react-router-dom";
import UserMenu from "./Components/Buttons/UserMenu";
import ClearAllChatsButton from "./Components/Buttons/ClearAllChatsButton";
import { Sidebar } from "./Components/Sidebar";
import { Button } from "react-bootstrap";
import { useContext } from "react";
import { ThemeContext } from "./Components/ThemeContext";
/**
 * ChatHistoryPage is the page that is used to display the chat history page.
 * @returns {JSX} - The React component for the chat history page.
 */
export default function ChatHistoryPage() {
    const navigate = useNavigate();
    const { theme } = useContext(ThemeContext);
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
        <div className="container-fluid vh-100 d-flex flex-column py-2 px-0 overflow-hidden">
            {/* Header: Logo and User Menu */}
            <div className="row justify-content-between align-items-center mx-0 px-4 py-2">
                <div className="col-auto">
                    <img
                        src={theme === "dark" ? "../images/b0e06.png" : "../images/arcai-logo-light-theme.png"}
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px"}}
                    />
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "var(--bg-color)", color: "var(--text-secondary-color)" , border: "none", transition: "background 0.3s ease, color 0.3s ease"}} onClick={handleChatButtonClick}>Chat</Button>
                </div>
                <div className="col-auto">
                    <Button className="fs-1 fw-bold" style={{backgroundColor: "var(--bg-color)", color: "var(--text-color)", border: "none", transition: "background 0.3s ease, color 0.3s ease"}} onClick={handleHistoryButtonClick}>History</Button>
                </div>
                <UserMenu right = {1.03}/>
            </div>

            <hr className="mb-0" style={{marginTop: "8px"}}/>

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
