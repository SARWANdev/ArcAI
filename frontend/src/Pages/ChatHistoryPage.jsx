import UserMenu from "./Components/Buttons/UserMenu";
import SearchBar from "./Components/Buttons/SearchBar";
import HistoryGrid from "./Components/Grids/HistoryGrid";
import PageLayoutChat from "./Components/Containers/PageLayoutChat";

export default function ChatHistoryPage() {
  return (
    // Page layout with a black-themed history chat and user menu aligned right
    <PageLayoutChat headerRight={<UserMenu right={28} />} historyBlack={true}>
      {/* Page title */}
      <h1 className="fw-bold mt-3">History</h1>

      {/* Search bar container with spacing */}
      <div className="row mt-4 align-items-center mb-3">
        <div className="col-auto">
          <div style={{ width: "250px" }}>
            {/* Search bar configured for chat history filtering */}
            <SearchBar ifChat={true} />
          </div>
        </div>
        <div className="col" /> {/* Spacer column for layout alignment */}
      </div>
    <div>
    <HistoryGrid />
    </div>
    </PageLayoutChat>
  );
}