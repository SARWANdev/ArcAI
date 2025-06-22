import { Button } from "react-bootstrap"
import { useState} from "react"
/**
 * ProjectGrid is the component that is used to display the projects in the library page.
 * @returns {JSX} - The React component for the project container.
 */
export default function ProjectGrid(){
    // Lets consider that we have 2 states for filtering: Either the state has Title or last accessed Button
    const [currentState, setCurrentState] = useState("Title");
    return(
        <div className="container-fluid d-flex row mb-4">
            <Button className={`btn btn-light fw-bold ${currentState === "Title" ? "text-decoration-underline" : ""}`} title="Title" style={{width : "55px", marginRight: "542px"}} id="title-button" onClick={() => {setCurrentState("Title")}}>Title</Button>
            <Button className={`btn btn-light fw-bold ${currentState === "LastAccessed" ? "text-decoration-underline" : ""}`} title = "last accessed" style={{width : "130px"}} id = "last-accessed-button" onClick={() => {setCurrentState("LastAccessed")}}>Last Accessed</Button>
        </div>
    )
}