import "./ProjectGrid.css"
/**
 * LibraryPageProjectContainer is the component that is used to display the projects in the library page.
 * @returns {JSX} - The React component for the project container.
 */
export default function ProjectGrid(){
    return(
        <div className="project-grid-container">
            <div className="project-grid-title-form">
                <button className="project-grid-title-button" title="Title button">Title</button>
                <button className="project-grid-last-accessed-button" title="Last Accessed button">Last Accessed</button>
            </div>
        </div>
    )
}