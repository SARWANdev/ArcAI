import "./SearchBar.css"
export default function SearchBar() {
    return(
        <form className="search-bar-form">
            <input type="text" placeholder="Search Library" id = "search-input"/>
            <button type="submit" id = "search-button" title="Search"><img src= "../../../images/search-icon.png" alt="search" className="search-icon"/></button>
        </form>
    )
}