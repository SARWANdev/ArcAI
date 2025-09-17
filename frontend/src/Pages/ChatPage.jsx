import AIChatContainer from "./Components/Containers/AIChatContainer";
import { useParams } from "react-router-dom";
import PageLayoutChat from "./Components/Containers/PageLayoutChat";
import UserMenu from "./Components/Buttons/UserMenu";

export default function ChatPage() {
  // Get conversationId from URL parameters
  const params = useParams();

  return (
    // Page layout with black chat theme and user menu aligned to the right
    <PageLayoutChat headerRight={<UserMenu right={28} />} chatBlack={true}>
      <div className="text-center">
        {/* AI chat interface with conversation ID from URL */}
        <AIChatContainer conversation_id={params.conversationId} />
      </div>
    </PageLayoutChat>
  );
}