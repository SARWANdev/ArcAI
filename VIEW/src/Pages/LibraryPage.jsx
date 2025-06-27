import UserMenu from "./Components/Buttons/UserMenu";
import SearchBar from "./Components/Buttons/SearchBar";
import { Sidebar } from "./Components/Sidebar";
import { useContext } from "react";
import { ThemeContext } from "./Components/ThemeContext";
import CreateProjectButton from "./Components/Buttons/CreateProjectButton";
import ProjectGrid from "./Components/ProjectGrid";

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

            <hr className="my-0" />

            {/* Main Layout: Sidebar and Content */}
            <div className="row flex-grow-1 g-0 mx-0" style={{ overflow: 'hidden' }}>
                {/* Sidebar - Will adjust width automatically */}
                <div className="col-auto h-100" style={{ overflow: 'hidden' }}>
                    <Sidebar />
                </div>

                {/* Content Area - Will adjust to sidebar width changes */}
                <div className="col h-100 overflow-auto px-4 py-3" 
                     style={{ 
                         transition: 'margin-left 0.3s ease',
                         marginLeft: '0' // Will be adjusted by sidebar width
                     }}>
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