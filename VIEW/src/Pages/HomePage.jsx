import UserPicture from "./Components/Buttons/UserPicture"
import PopUpBoxSignOut from "./Components/PopUpBoxSignOut"
import GoToLibraryButton from "./Components/Buttons/GoToLibraryButton"
import "./HomePage.css"
/**
 * HomePage is the page that is used to display the home page when the user is logged in.
 * @returns {JSX} - The React component for the home page when the user is logged in.
 */
function HomePage(){
    return(
      <div className="arcai-container">
        <header className="arcai-header">
          <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
          <UserPicture/>
        </header>
        <hr className = "line-ai-to-content"></hr>
        <PopUpBoxSignOut left = {"79.5%"} top = {"10%"}/>
        <main className="arcai-main-logged">
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
        <GoToLibraryButton/>
      </main>
    </div>
    )
}
export default HomePage