import { useContext } from "react";
import "bootstrap/dist/css/bootstrap.min.css"; // Bootstrap CSS for styling
import LoginButton from "./Components/Buttons/LoginButton"; // Login button component
import { ThemeContext } from "./Components/Contexts/ThemeContext"; // Context to get current theme (dark/light)
import PageLayoutLogin from "./Components/Containers/PageLayoutLogin"; // Layout component specific for login page
import FeatureCard from "./Components/UI/FeatureCard"; // Component to show feature preview cards

export default function LoginPage() {
  // Get current theme from ThemeContext to decide images & styles
  const { theme } = useContext(ThemeContext);

  return (
    <PageLayoutLogin>
      {/* Main content container, center-aligned text */}
      <main className="text-center">
        {/* Headline and subtitle section */}
        <div className="mb-5">
          <h2 className="fw-bold display-3">
            Your research,<br />supercharged by AI
          </h2>
          <p
            className="fs-1 fw-bold"
            style={{ color: "var(--text-secondary-color)" }}
          >
            Upload. Chat. Write. Cite.
          </p>
        </div>

        {/* Feature preview cards section */}
        <div className="row justify-content-center g-4 mb-5">
          {/* First feature card: My Library */}
          <div className="col-12 col-md-6 col-lg-5" style={{ height: 150 }}>
            <FeatureCard
              // Choose image depending on current theme (dark or light)
              imgSrc={
                theme === "dark"
                  ? "/images/library-dark-theme.png"
                  : "/images/library-light-theme.png"
              }
              alt="library"
              title="My Library"
              description="Organize and browse your PDFs"
            />
          </div>

          {/* Second feature card: Chat */}
          <div className="col-12 col-md-6 col-lg-5" style={{ height: 150 }}>
            <FeatureCard
              // Choose chat image based on theme
              imgSrc={
                theme === "dark"
                  ? "/images/chat-dark-theme.png"
                  : "/images/chat-light-theme.png"
              }
              alt="chat"
              title="Chat"
              description="Ask Questions & summarize papers"
            />
          </div>
        </div>

        {/* Login button below the features */}
        <LoginButton />
      </main>
    </PageLayoutLogin>
  );
}