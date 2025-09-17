import Logo from "../Buttons/Logo";
import UserMenu from "../Buttons/UserMenu";
import { Sidebar } from "../Containers/SideBar";
import { Button } from "react-bootstrap";
import { useNavigate } from "react-router-dom";

/**
 * PageLayout abstracts the common layout: header (logo + user menu), sidebar, and main content.
 * @param {React.ReactNode} children - The main content to render inside the layout.
 * @param {React.ReactNode} headerRight - Optional: custom content for the right side of the header (instead of UserMenu).
 * @param {string} className - Optional: additional class for the main content area.
 * @param {object} style - Optional: additional style for the main content area.
 */
export default function PageLayoutChat({ children, headerRight, className = "", style = {}, chatBlack, historyBlack }) {
  const navigate = useNavigate();

  function handleChatButtonClick(e){
    if (e) e.preventDefault();
    navigate("/home/chat-chatbot", { replace: true });
}
function handleHistoryButtonClick(e){
    if (e) e.preventDefault();
    navigate("/home/chat-history", { replace: true });
}
  return (
    <div className="container-fluid vh-100 d-flex flex-column p-0 overflow-hidden">
      {/* Header: Logo and User Menu */}
        <div className="d-flex justify-content-between align-items-center px-4 py-3">
          <Logo left = {0.76}/>
          <Button className="fs-1 fw-bold" id="chat-button" style={{backgroundColor: "var(--bg-color)", color: chatBlack ? "var(--text-color)" : "var(--text-secondary-color)", border: "none", transition: "background 0.3s ease, color 0.3s ease"}} onClick={handleChatButtonClick}>Chat</Button>
          <Button className="fs-1 fw-bold" id="history-button" style={{backgroundColor: "var(--bg-color)", color: historyBlack ? "var(--text-color)" : "var(--text-secondary-color)", border: "none", transition: "background 0.3s ease, color 0.3s ease"}} onClick={handleHistoryButtonClick}>History</Button>
          <div className="col-auto">
            {headerRight || <UserMenu right={7.5} />}
          </div>
        </div>
      <hr className="my-0" />
      {/* Main Layout: Sidebar and Content */}
      <div className="row flex-grow-1 g-0 mx-0" style={{ overflow: 'hidden' }}>
        {/* Sidebar - Will adjust width automatically */}
        <div className="col-auto h-100" style={{ overflow: 'hidden' }}>
          <Sidebar />
        </div>
        {/* Content Area - Will adjust to sidebar width changes */}
        <div className={`col h-100 overflow-auto px-4 py-3 ${className}`} style={{ transition: 'margin-left 0.3s ease', marginLeft: '0', ...style }}>
          {children}
        </div>
      </div>
    </div>
  );
} 