import FavouriteButton from "../Buttons/FavouriteButton";
import ReadStatusButton from "../Buttons/ReadStatusButton";
import DeleteButton from "../Buttons/DeleteButton";
import DuplicateButton from "../Buttons/DuplicateButton";
import ExportBibtexButton from "../Buttons/ExportBibtexButton";
import MoveButton from "../Buttons/MoveButton";
import RenameButton from "../Buttons/RenameButton";
import TagManager from "./TagManager";
import DownloadButton from "../Buttons/DownloadButton";
import SetBibtexButton from "../Buttons/SetBibtexButton";  

export default function DocumentRow({
  document,
  idx,
  favourite,
  setFavourite,
  read,
  setRead,
  project_id,
  sub,
  openIdx,
  setOpenIdx,
  settingsButtonRefs,
  collapseRef,
  isExpanded,
  refreshDocuments,
  formatDaysAgo,
}) {
  const handleRowClick = (e) => {
    if (
      e.target.closest('.favourite-button') || 
      e.target.closest('.settings-button') || 
      e.target.closest('.card-body')
    ) {
      return;
    }
    window.location.href = `http://localhost:5173/home/library/document/${document.DocumentId}`;
  };
  
  return (
    <div className="col-md-12" key={document.DocumentId}>
      <div 
        className="d-flex align-items-center p-2 border-top border-secondary" 
        id="document-button"
        style={{ height: "80px", cursor: "pointer" }}
        onClick={handleRowClick}
      >
        <div className="favourite-button" onClick={(e) => e.stopPropagation()}>
          <FavouriteButton
            user_id={sub}
            project_id={project_id}
            document_id={document.DocumentId}
            isFavourite={favourite instanceof Set ? favourite.has(document.DocumentId) : false}
            onChange={(newState) => {
              setFavourite((prev) => {
                const updated = new Set(prev);
                newState ? updated.add(document.DocumentId) : updated.delete(document.DocumentId);
                return updated;
              });
            }}
          />
        </div>

        <div 
          className="text-truncate"
          id="document-title"
          style={{
            color: document.TagColor || "var(--text-color)",
            width: "250px",
            marginLeft: "5px",
            fontStyle: read instanceof Set && read.has(document.DocumentId) ? "italic" : "normal"
          }}        
        >
          {document.Title}
        </div>

        <div id="document-author" className="text-truncate" style={{marginLeft: "8px", width: "100px" }}>
          {(() => {
            try {
              const safeString = document.Authors.replace(/'/g, '"');
              const authorsArray = JSON.parse(safeString);
              return Array.isArray(authorsArray) ? authorsArray.join(", ") : document.Authors;
            } catch {
              return document.Authors || "None";
            }
          })()}
        </div>

        <div id="document-year">
          {document.Year || "None"}
        </div>

        <div id="document-source" className="text-truncate">
          {document.Source || "None"}
        </div>

        <div id="document-created-at">
          {formatDaysAgo(document.CreatedAt)}
        </div>

        <button
          ref={(el) => (settingsButtonRefs.current[idx] = el)}
          className="btn btn-sm btn-outline-secondary settings-button"
          onClick={(e) => {
            e.stopPropagation();
            setOpenIdx(openIdx === idx ? null : idx);
          }}
        />
      </div>

      {openIdx === idx && (
        <div
          ref={collapseRef}
          style={{
            position: "absolute",
            left: isExpanded ? "90%" : "85.5%",
            zIndex: 1000,
            width: "150px",
            marginTop: "30px",
          }}
        >
          <div className="card card-body p-2" style={{backgroundColor: "var(--bg-color)"}}>
            <TagManager user_id={sub} document={document} refreshDocuments={refreshDocuments} />
            <DeleteButton document_id={document.DocumentId} onCloseSettings={() => setOpenIdx(null)} />
            <DownloadButton document_id={document.DocumentId}/>
            <DuplicateButton document_id={document.DocumentId} refreshDocuments={refreshDocuments}/>
            <ExportBibtexButton document_id={document.DocumentId}/>
            <ReadStatusButton
              user_id={sub}
              project_id={project_id}
              document_id={document.DocumentId}
              isRead={read instanceof Set ? read.has(document.DocumentId) : false}
              onChange={(newState) => {
                setRead((prev) => {
                  const updated = new Set(prev);
                  newState ? updated.add(document.DocumentId) : updated.delete(document.DocumentId);
                  return updated;
                });
              }}
            />
            <MoveButton document_id={document.DocumentId} refreshDocuments={refreshDocuments}/>
            <RenameButton document_id={document.DocumentId} document_title={document.Title} refreshDocuments={refreshDocuments}/>
            <SetBibtexButton document_id={document.DocumentId} refreshDocuments={refreshDocuments}/>
          </div>
        </div>
      )}
    </div>
  );
}