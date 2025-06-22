import { Button } from "react-bootstrap";
export default function CreateProjectButton() {
    return (
        <Button className="btn btn-light fs-5">
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