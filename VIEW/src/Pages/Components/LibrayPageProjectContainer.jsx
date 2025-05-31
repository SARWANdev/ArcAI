import "./LibraryPageProjectContainer.css"
export default function LibraryPageProjectContainer({projectContainer}){
    return(
        <div className="library-page-project-container">
            {Array.isArray(projectContainer) && projectContainer.map((project) => (
                <div key={project.Project_ID}>
                    <h1>{project.Name}</h1>
                </div>
            ))}
        </div>
    )
}