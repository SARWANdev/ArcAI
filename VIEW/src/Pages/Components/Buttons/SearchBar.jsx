export default function SearchBar() {
    return (
        <form className="d-flex align-items-center bg-light rounded p-1 me-5" style={{ width: '540px', height: '50px' }}>
            <input
                type="text"
                placeholder="Search Library"
                className="form-control border-0 bg-light text-secondary fs-5"
                style={{ width: '500px' }}
            />
            <button
                type="submit"
                className="btn p-0 border-0 bg-transparent"
                title="Search"
            >
                <img
                    src="../../../images/search-icon.png"
                    alt="search"
                    style={{ width: '37px', height: '37px' }}
                />
            </button>
        </form>
    );
}