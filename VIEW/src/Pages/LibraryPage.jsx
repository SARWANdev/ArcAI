import UserMenu from "./Components/Buttons/UserMenu"
import ProjectGrid from "./Components/ProjectGrid"
import CreateProjectButton from "./Components/Buttons/CreateProjectButton"
import SearchBar from "./Components/Buttons/SearchBar"
import { Sidebar } from "./Components/Sidebar"
import "./LibraryPage.css"
/**
 * LibraryPage is the page that is used to display the library page.
 * @returns {JSX} - The React component for the library page.
 */
function LibraryPage() {
    return(
        <>
        {/* <div className="library-page-container">
            <div className="library-page-header">
                <hr className="library-page-line"></hr>
                <div className="library-page-header-content">
                    <img src = "../images/arcai-logo.png" alt = "logo" className = "arcai-logo"/>
                    <UserMenu className = "library-page-user-button" leftMenu = {"83%"} topMenu = {"15%"}/>
                </div>
                <hr className="library-page-line"></hr>
                <div className="library-page-content">
                    <Sidebar/>
                    <div className="library-page-content-container" id = "library-page-content-container">
                        <h1 className="library-page-content-container-title">My Projects</h1>
                        <div className="library-page-content-container-dashboard">
                            <SearchBar/>
                            <CreateProjectButton/>
                        </div>
                        <ProjectGrid/>
                    </div>
                </div>
            </div>
        </div> */}
        <div className="container-fluid py-2">
            <div className="row justify-content-between align-items-center">
                <img src="../images/arcai-logo.png" alt="logo" className="img-fluid mb-4 p-0" style={{ width: "115px", height: "128px", position: "relative", left: "8.6%" }} />
                <UserMenu/>
            </div>
            <hr className="w-100" />
            <main className="text-center">
                <Sidebar/>
            </main>
        </div>
        </>
    )
}
export default LibraryPage