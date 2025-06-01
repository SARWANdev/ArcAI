import "./GoToLibraryButton.css"
import { useNavigate } from 'react-router-dom';
/**
 * GoToLibraryButton is the component that is used to navigate to the library page.
 * @returns {JSX} - The React component for the go to library button.
 */
function GoToLibraryButton() {
    const navigate = useNavigate()
    /**
     * goToLibrary is the function that is used to navigate to the library page.
     */
    function goToLibrary() {
        navigate("/workspace/library")
    }
    return (
        <button className="arcai-go-to-library-button" onClick={goToLibrary} title="Go To Library">Go To Library</button>
    )
}
export default GoToLibraryButton