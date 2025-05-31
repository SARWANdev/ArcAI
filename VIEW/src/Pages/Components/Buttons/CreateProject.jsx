import "./CreateProject.css"
export default function CreateProject({setProjectContainer}) {
    //TODO: Create a function which shows the projects on the library page
    const URL_CREATE_PROJECT = "http://127.0.0.1:5000/create-project";
    const URL_GET_PROJECTS = "http://127.0.0.1:5000/get-projects";
    /**
     * This function is called when the user clicks the create project button
     */
    async function onCreateProjectClick(){
        const response = await fetch(URL_CREATE_PROJECT, {
        method: "POST",
        });
        const data = await response.json();
        console.log(data);
        if (data.status == "success"){
            console.log("Getting projects from the server");
            const projectList = async function getProjects(){
                const response = await fetch(URL_GET_PROJECTS);
                const data = await response.json();
                return data;
            }
            const projects_list = await projectList();
            setProjectContainer(projects_list.projects);
        }
    }

    return (
        <button className="create-project-button" onClick={onCreateProjectClick}><img src={"../../../images/Upload.png"} alt="upload" className="upload-icon"/>Create Project</button>
    )
}