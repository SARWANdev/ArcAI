import "./ProjectGrid.css"
/**
 * LibraryPageProjectContainer is the component that is used to display the projects in the library page.
 * @returns {JSX} - The React component for the project container.
 */
export default function ProjectGrid(){
    return(
        <div className="library-page-project-title-container">
            <div className="library-page-project-title-form">
                <button className="library-page-project-title-button" title="Title button">Title</button>
                <button className="library-page-project-last-accessed-button" title="Last Accessed button">Last Accessed</button>
            </div>
        </div>
    )
}