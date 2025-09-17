import { Button } from "react-bootstrap";
import axios from "axios";
import { useState } from "react";

export default function FavouriteButton({
  user_id,
  project_id,
  document_id,
  isFavourite,
  onChange,
}) {
  const [loading, setLoading] = useState(false);
  // State for the error popup
  const [errorMessage, setErrorMessage] = useState(null);

  async function toggleFavourite() {
    try {
      setLoading(true);
      if (isFavourite) {
        await axios.delete("http://localhost:3000/document/favourite", {
          data: { user_id, project_id, document_id },
          withCredentials: true,
        });
        onChange(false);
      } else {
        await axios.post(
          "http://localhost:3000/document/favourite",
          { user_id, project_id, document_id },
          { withCredentials: true }
        );
        onChange(true);
      }
    } catch (err) {
      setErrorMessage(err.response?.data?.error|| "Error to toggle favourite.");
      setTimeout(() => setErrorMessage(null), 5000);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
    {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
    <Button
      variant="link"
      onClick={toggleFavourite}
      disabled={loading}
      style={{
        fontSize: "20px",
        color: isFavourite ? "#ffc107" : "#ccc",
        textDecoration: "none",
      }}
      title={isFavourite ? "Unfavorite" : "Mark as Favorite"}
    >
      {isFavourite ? "★" : "☆"}
    </Button>
    </>
  );
}