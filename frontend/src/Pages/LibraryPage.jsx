import CreateProjectButton from "./Components/Buttons/CreateProjectButton"; // Button to create new projects
import ProjectGrid from "./Components/Grids/ProjectGrid"; // Grid component displaying list of projects
import PageLayout from "./Components/Containers/PageLayout"; // Layout wrapper for consistent page structure
import SearchBar from "./Components/Buttons/SearchBar"; // Search input component

export default function LibraryPage() {
    return (
        <PageLayout>
            {/* Page title */}
            <h1 className="fs-1 fw-bold mb-4">My Projects</h1>

            {/* Responsive row for SearchBar and CreateProjectButton */}
            <div className="d-flex flex-column flex-md-row align-items-stretch align-items-md-center justify-content-between gap-2 mb-4">
                {/* Search bar: full width on mobile, auto on larger screens */}
                <div className="flex-grow-1 flex-md-grow-0">
                    <SearchBar ifDoc={true} />
                </div>

                {/* Create project button */}
                <div>
                    <CreateProjectButton />
                </div>
            </div>

            {/* Grid displaying the projects */}
            <ProjectGrid />
        </PageLayout>
    );
}
