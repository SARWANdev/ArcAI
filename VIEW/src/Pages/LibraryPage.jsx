import Sidebar from "./Components/Sidebar"
import UserPicture from "./Components/Buttons/UserPicture"
import PopUpBoxSignOut from "./Components/Buttons/PopUpBoxSignOut"
import LibraryPageProjectContainer from "./Components/LibrayPageProjectContainer"
import "./LibraryPage.css"
import {createContext} from "react"
import CreateProject from "./Components/Buttons/CreateProject"
export const IDContext = createContext();
//Add near the create Project button another div element which will eventually contain the search bar
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