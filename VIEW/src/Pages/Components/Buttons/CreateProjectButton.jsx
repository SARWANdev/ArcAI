import { Button } from "react-bootstrap";
import "./CreateProjectButton.css"
export default function CreateProjectButton() {
    return (
        <Button className="fs-5" id = "create-project-button">
            <img
            src="../../../images/Upload.png"
            alt="upload"
            style={{ width: "29px", height: "29px" }}
            className="me-3"
            />
            Create Project
        </Button>
    );
}