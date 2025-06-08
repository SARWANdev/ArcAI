import "./CreateProjectButton.css"
/**
 * CreateProject is the component that is used to display the create project button in the library page.
 * @returns {JSX} - The React component for the create project button.
 */
export default function CreateProjectButton() {
    return (
        <button className="create-project-button" title="Create Project"><img src={"../../../images/Upload.png"} alt="upload" className="upload-icon"/>Create Project</button>
    )
}