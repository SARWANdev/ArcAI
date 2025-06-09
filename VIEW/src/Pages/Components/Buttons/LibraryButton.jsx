import "./LibraryButton.css"
import { useNavigate } from 'react-router-dom';
/**
 * LibraryButton is the component that is used to display the library button.
 * @param {string} content - The content of the library button.
 * @returns {JSX} - The React component for the library button.
 */
function LibraryButton({content}) {
    const navigate = useNavigate()
    /**
     * goToLibrary is the function that is used to navigate to the library page.
     */
    function goToLibrary(e) {
        if (e) e.preventDefault();
        navigate("/home/library", { replace: true });   //TODO: Change to /library
    }
    
    return (
        <div className="library-container" style={content != "Library" ? {height: "70px", width: "70px"} : {}}>
            <button className="arcai-library-button" onClick={goToLibrary} id = "library-button" title="Library">
                <img src="../../images/book.png" className="image-library-button" alt="library"/>
            </button>
            <label htmlFor="library-button" className="library-label" id="library-label">{content}</label>
        </div>
    )
}
export default LibraryButton