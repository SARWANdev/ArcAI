import "./SearchBar.css"
export default function SearchBar() {
    return (
        <form className="d-flex align-items-center rounded p-1 me-5" style={{ width: '540px', height: '50px', backgroundColor: "var(--bg-button-color)", transition: "background 0.3s ease, color 0.3s ease" }}>
            <input
                type="text"
                id = "input-text"
                placeholder="Search Library"
                className="form-control border-0 text-secondary fs-5"
                style={{ width: '500px' , backgroundColor: "var(--bg-button-color)", transition: "background 0.3s ease, color 0.3s ease"}}
            />
            <button
                type="submit"
                className="btn p-0 border-0 bg-transparent"
                title="Search"
            >
                <img
                    src="../../../images/search-icon.png"
                    alt="search"
                    style={{ width: '37px', height: '37px', transition: "background 0.3s ease, color 0.3s ease" }}
                />
            </button>
        </form>
    );
}