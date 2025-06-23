import UserMenu from "./Components/Buttons/UserMenu";
import SearchBar from "./Components/Buttons/SearchBar";
import { Sidebar } from "./Components/Sidebar";
import CreateProjectButton from "./Components/Buttons/CreateProjectButton";
import ProjectGrid from "./Components/ProjectGrid";

/**
 * LibraryPage is the page that is used to display the library page.
 * @returns {JSX} - The React component for the library page.
 */
export default function LibraryPage() {
    return (
        <div className="container-fluid py-2">
            {/* Header: Logo and User Menu */}
            <div className="row justify-content-between align-items-center">
                <div className="col-auto">
                    <img
                        src="../images/arcai-logo.png"
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px" }}
                    />
                </div>
                <UserMenu right={7.5}/>
            </div>

            <hr className="mb-0" style={{marginTop: "16px"}}/>

            {/* Main Layout: Sidebar and Content */}
            <div className="row flex-nowrap">
                <div className="col-auto">
                    <Sidebar />
                </div>

                <div className="col px-4">
                    <h1 className="fs-1 fw-bold mb-4">My Projects</h1>

                    {/* Search and Create Button Row */}
                    <div className="row g-2 align-items-center mb-4">
                        <div className="col-md-auto">
                            <SearchBar />
                        </div>
                        <div className="col-md-auto">
                            <CreateProjectButton />
                        </div>
                    </div>

                    <ProjectGrid />
                </div>
            </div>
        </div>
    );
}