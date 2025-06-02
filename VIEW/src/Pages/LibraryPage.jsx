import Sidebar from "./Components/Sidebar"
import UserPicture from "./Components/Buttons/UserPicture"
import PopUpBoxSignOut from "./Components/PopUpBoxSignOut"
import LibraryPageProjectContainer from "./Components/LibraryPageProjectContainer"
import {createContext} from "react"
import CreateProject from "./Components/Buttons/CreateProject"
import SearchBar from "./Components/Buttons/SearchBar"
import "./LibraryPage.css"
/**
 * IDContext is the ID of the container which is to be transformed forward or backward.
 */
export const IDContext = createContext();
/**
 * LibraryPage is the page that is used to display the library page.
 * @returns {JSX} - The React component for the library page.
 */
function LibraryPage() {
    return(
        <>
        <div className="library-page-container">
            <div className="library-page-header">
                <hr className="library-page-line"></hr>
                <div className="library-page-header-content">
                    <h1 className="arcai-logo">ArcAI</h1>
                    <UserPicture className = "library-page-user-button" left = {"85%"} bottom= {"14%"}/>
                    <PopUpBoxSignOut left = {"82%"} top = {"15%"}/>
                </div>
                <hr className="library-page-line"></hr>
                <div className="library-page-content">
                    <div className="library-page-content-container" id = "library-page-content-container">
                        <h1 className="library-page-content-container-title">My Projects</h1>
                        <div className="library-page-content-container-dashboard">
                            <SearchBar/>
                            <CreateProject/>
                        </div>
                        <LibraryPageProjectContainer/>
                    </div>
                    <IDContext.Provider value = {"library-page-content-container"}>
                        <Sidebar/>
                    </IDContext.Provider>
                </div>
            </div>
        </div>
        </>
    )
}
export default LibraryPage