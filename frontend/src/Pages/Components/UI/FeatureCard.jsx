import React from "react";

/**
 * FeatureCard displays an icon, title, and description for a feature preview.
 * @param {string} imgSrc - The image source URL.
 * @param {string} alt - The alt text for the image.
 * @param {string} title - The title of the feature.
 * @param {string} description - The description of the feature.
 * @param {object} imgStyle - Optional: style object for the image.
 * @param {string} className - Optional: additional class for the card.
 */
export default function FeatureCard({ imgSrc, alt, title, description, imgStyle = {}, className = "" }) {
  return (
    <div className={`d-flex align-items-center border rounded p-3 h-100 ${className}`}>
      <img
        src={imgSrc}
        alt={alt}
        className="img-fluid me-3"
        style={{ width: "68px", height: "68px", transition: "background 0.3s ease, color 0.3s ease", ...imgStyle }}
      />
      <div className="text-start">
        <h5 className="mb-1 fw-bold fs-2">{title}</h5>
        <p className="mb-0 fs-4" style={{ color: "var(--text-secondary-color)" }}>
          {description}
        </p>
      </div>
    </div>
  );
} 