import { useContext } from "react";
import { useNavigate } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import { Button } from "react-bootstrap";
import { ThemeContext } from "./Components/Contexts/ThemeContext";
import PageLayoutLogin from "./Components/Containers/PageLayoutLogin";
import FeatureCard from "./Components/UI/FeatureCard";
import "./HomePage.css";
import UserMenu from "./Components/Buttons/UserMenu";

export default function HomePage() {
  const { theme } = useContext(ThemeContext);
  const navigate = useNavigate();

  // Navigate user to the library page
  const goToLibrary = () => {
    navigate("/home/library");
  };

  // Helper to get image source based on theme for FeatureCards
  const getImageSrc = (type) => {
    return theme === "dark"
      ? `/images/${type}-dark-theme.png`
      : `/images/${type}-light-theme.png`;
  };

  return (
    // PageLayoutLogin wraps the page layout and includes a UserMenu in the header
    <PageLayoutLogin headerRight={<UserMenu right={7.5} />}>
      <main className="text-center">
        {/* Headline and subtitle section */}
        <section className="mb-5">
          <h2 className="fw-bold display-3">
            Your research,<br />supercharged by AI
          </h2>
          <p className="fs-1 fw-bold" style={{ color: "var(--text-secondary-color)" }}>
            Upload. Chat. Write. Cite.
          </p>
        </section>

        {/* Feature preview cards */}
        <section className="row justify-content-center g-4 mb-5">
          <div className="col-12 col-md-6 col-lg-5" style={{ height: 150 }}>
            <FeatureCard
              imgSrc={getImageSrc("library")}
              alt="library"
              title="My Library"
              description="Organize and browse your PDFs"
            />
          </div>
          <div className="col-12 col-md-6 col-lg-5" style={{ height: 150 }}>
            <FeatureCard
              imgSrc={getImageSrc("chat")}
              alt="chat"
              title="Chat"
              description="Ask Questions & summarize papers"
            />
          </div>
        </section>

        {/* Call-to-action button to navigate to Library */}
        <Button
          className="fs-2 fw-bold"
          id="go-to-library-button"
          style={{ color: "var(--bg-color)" }}
          onClick={goToLibrary}
        >
          Go to Library
        </Button>
      </main>
    </PageLayoutLogin>
  );
}