import Logo from "../Buttons/Logo";
import UserMenu from "../Buttons/UserMenu";

/**
 * PageLayout abstracts the common layout: header (logo + user menu), sidebar, and main content.
 * @param {React.ReactNode} children - The main content to render inside the layout.
 * @param {React.ReactNode} headerRight - Optional: custom content for the right side of the header (instead of UserMenu).
 * @param {string} className - Optional: additional class for the main content area.
 * @param {object} style - Optional: additional style for the main content area.
 */
export default function PageLayoutLogin({ children, headerRight, className = "", style = {} }) {
  return (
    <div className="container-fluid vh-100 d-flex flex-column p-0 overflow-hidden">
      {/* Header: Logo and User Menu */}
      <div className="row justify-content-between align-items-center mx-0 px-4 py-3">
        <div className="col-auto">
          <Logo />
        </div>
        <div className="col-auto">
          {headerRight || <UserMenu right={7.5} />}
        </div>
      </div>
      <hr className="my-0" />
      {/* Main Layout: Sidebar and Content */}
      <div className="row flex-grow-1 g-0 mx-0" style={{ overflow: 'hidden' }}>
        {/* Content Area - Will adjust to sidebar width changes */}
        <div className={`col h-100 overflow-auto px-4 py-3 ${className}`} style={{ transition: 'margin-left 0.3s ease', marginLeft: '0', ...style }}>
          {children}
        </div>
      </div>
    </div>
  );
} 