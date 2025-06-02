import "./ExportBibtex.css"
/**
 * ExportBibtex is the component that is used to display the export bibtex button in the library page.
 * @returns {JSX} - The React component for the export bibtex button.
 */
export default function ExportBibtex() {
    return (
        <div className="export-bibtex-container">
            <button className="export-bibtex-button" title="Export Bibtex">Export Bibtex</button>
        </div>
    )
}