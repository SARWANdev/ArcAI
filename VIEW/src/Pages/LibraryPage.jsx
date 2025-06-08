import Sidebar from "./Components/Sidebar"
import UserAvatar from "./Components/Buttons/UserAvatar"
import UserMenu from "./Components/UserMenu"
import ProjectGrid from "./Components/ProjectGrid"
import {createContext} from "react"
import CreateProjectButton from "./Components/Buttons/CreateProjectButton"
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
                    <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
                    <UserAvatar className = "library-page-user-button"/>
                </div>
                <UserMenu left = {"83%"} top = {"15%"}/>
                <hr className="library-page-line"></hr>
                <div className="library-page-content">
                    <div className="library-page-content-container" id = "library-page-content-container">
                        <h1 className="library-page-content-container-title">My Projects</h1>
                        <div className="library-page-content-container-dashboard">
                            <SearchBar/>
                            <CreateProjectButton/>
                        </div>
                        <ProjectGrid/>
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