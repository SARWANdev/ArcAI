import UserMenu from "./Components/Buttons/UserMenu";
import SearchBar from "./Components/Buttons/SearchBar";
import { Sidebar } from "./Components/Sidebar";
import { useContext } from "react";
import { ThemeContext } from "./Components/ThemeContext";
import CreateProjectButton from "./Components/Buttons/CreateProjectButton";
import ProjectGrid from "./Components/ProjectGrid";

/**
 * LibraryPage is the page that is used to display the library page.
 * @returns {JSX} - The React component for the library page.
 */
export default function LibraryPage() {
    const { theme } = useContext(ThemeContext);
    return (
        <div className="container-fluid vh-100 d-flex flex-column p-0 overflow-hidden">
            {/* Header: Logo and User Menu */}
            <div className="row justify-content-between align-items-center mx-0 px-4 py-3">
                <div className="col-auto">
                    <img
                        src={theme === "dark" ? "../images/b0e06.png" : "../images/arcai-logo-light-theme.png"}
                        alt="logo"
                        className="img-fluid"
                        style={{ width: "115px", height: "128px" }}
                    />
                </div>
                <div className="col-auto">
                    <UserMenu right={7.5} />
                </div>
            </div>

            <hr className="my-0" />  {/* Kept your original divider */}

            {/* Main Layout: Sidebar and Content */}
            <div className="row flex-grow-1 g-0 mx-0">
                {/* Sidebar - Fixed width, full height */}
                <div className="col-auto h-100" style={{ minWidth: "250px" }}>
                    <Sidebar />
                </div>

                {/* Content Area - Flexible width, scrollable, with original spacing */}
                <div className="col h-100 overflow-auto px-4 py-3">
                    <h1 className="fs-1 fw-bold mb-4">My Projects</h1>

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