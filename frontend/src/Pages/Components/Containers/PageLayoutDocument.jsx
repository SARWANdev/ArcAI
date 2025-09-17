import Logo from "../Buttons/Logo";
import UserMenu from "../Buttons/UserMenu";
import "./PageLayoutDocument.css"
import { SidebarDocument } from "./SideBarDocument";

export default function PageLayoutDocument({ children, headerRight, className = "", style = {}, isHeaderVisible, setIsHeaderVisible, projectId, projectTitle }) {
  const toggleHeader = () => {
    setIsHeaderVisible(!isHeaderVisible);
  };

  const headerToggleBtnStyle = {
    position: 'absolute',
    // Position relative to the parent container
    top: isHeaderVisible ? '150px' : '0', 
    left: '50%',
    zIndex: 1050,
    width: '24px',
    height: '24px',
    borderRadius: '50%',
    backgroundColor: '#f8f9fa',
    border: '2px solid #dee2e6',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
  };

  const toggleIconStyle = {
    fontSize: '12px',
    color: '#495057',
    transition: 'transform 0.3s ease',
  };

  return (
    <div className="container-fluid vh-100 d-flex flex-column p-0 overflow-hidden position-relative">
      <div className={`header-container ${isHeaderVisible ? 'is-visible' : 'is-hidden'}`}>
        <div className="row justify-content-between align-items-center mx-0 px-4 py-3">
          <div className="col-auto">
            <Logo />
          </div>
          <div className="col-auto">
            {headerRight || <UserMenu right={7.5} />}
          </div>
        </div>
        <hr className="my-0" />
      </div>

      <button 
        onClick={toggleHeader} 
        style={headerToggleBtnStyle}
        className="header-toggle-btn"
        aria-label={isHeaderVisible ? "Hide header" : "Show header"}
      >
        <span style={toggleIconStyle} className="toggle-icon">
          {isHeaderVisible ? "▲" : "▼"}
        </span>
      </button>

      <div className="row flex-grow-1 g-0 mx-0" style={{ overflow: 'hidden' }}>
        <div className="col-auto h-100" style={{ overflow: 'hidden' }}>
          <SidebarDocument projectId={projectId} projectTitle={projectTitle} />
        </div>
        <div className={`col h-100 overflow-auto px-4 py-3 ${className}`} style={{ transition: 'margin-left 0.3s ease', marginLeft: '0', ...style }}>
          {children}
        </div>
      </div>
    </div>
  );
}