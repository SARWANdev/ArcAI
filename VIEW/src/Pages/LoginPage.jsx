import LoginButton from "./Components/Buttons/LoginButton";
import "./LoginPage.css"
/**
 * GuestHomePage is the page that is used to display the home page when the user is not logged in.
 * @returns {JSX} - The React component for the home page when the user is not logged in.
 */
function LoginPage(){ 
    return (
    <div className="arcai-container">
      <header className="arcai-header">
        <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
      </header>
      <hr className = "line-ai-to-content"></hr>
      
      <main className="arcai-main">
        <div className="arcai-hero">
          <h2 className="arcai-tagline">Your research,<br />supercharged by AI</h2>
          <p className="arcai-subtagline">Upload. Chat. Write. Cite.</p>
        </div>
        
        <div className="arcai-features">
          <div className="arcai-feature-item">
            <label htmlFor="library">
              <img src = "../images/book.png" alt = "book" className="image-in-box"></img>
              <span className="arcai-feature-title">My Library</span>
              <span className="arcai-feature-desc">Organize and browse your PDFs</span>
            </label>
          </div>
          
          <div className="arcai-feature-item">
            <label htmlFor="chat">
              <img src = "../images/chat.png" alt = "chat" className="image-in-box"></img>
              <span className="arcai-feature-title">Chat</span>
              <span className="arcai-feature-desc">Ask Questions & summarize papers</span>
            </label>
          </div>
        </div>
        <LoginButton/>
      </main>
    </div>
  );
}
export default LoginPage