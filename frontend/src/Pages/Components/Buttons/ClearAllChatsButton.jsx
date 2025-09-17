import { Button } from "react-bootstrap";
import { useState } from "react";
import "./ClearAllChatsButton.css";
import { useAuth } from "../Contexts/AuthContext";
import axios from "axios";

export default function ClearAllChatsButton({ onCleared }) {
    const { sub } = useAuth();
    const [loading, setLoading] = useState(false);
      // State for the error popup
    const [errorMessage, setErrorMessage] = useState(null);

    const handleClearAll = async () => {
        try {
            setLoading(true);
            const response = await axios.delete("http://localhost:3000/chat/delete-all", {
                data: { user_id: sub },
                headers: {
                    "Content-Type": "application/json",
                },
                withCredentials: true,
            });

            if (response.status === 200) {
                if (typeof onCleared === "function") {
                    await onCleared();
                }
            }
        } catch (error) {
            setErrorMessage(err.response?.data?.error|| "Failed to clear all chat");
            setTimeout(() => setErrorMessage(null), 5000);
            if (typeof onCleared === "function") {
                await onCleared(new Error("delete-failed"));
            }
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
        {errorMessage && (
        <div className="error-popup">
          <p>{errorMessage}</p>
        </div>
      )}
      <Button
            className="btn"
            title="Clear all"
            id="btn"
            onClick={handleClearAll}
            disabled={loading}
        >
            {loading ? "Clearing..." : "Clear All"}
        </Button>
        </>
    );
}