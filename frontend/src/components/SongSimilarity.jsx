import React, { useState } from "react";
import axios from "axios";

const SongSimilarity = () => {
  const [file, setFile] = useState(null);
  const [similarSongs, setSimilarSongs] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleUpload = async () => {
    if (!file) {
      setError("Please select a file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setLoading(true);
    setError("");
    try {
      const response = await axios.post("http://127.0.0.1:8000/api/upload-and-find", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setSimilarSongs(response.data.similar_songs);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h1>Copy Right Check!</h1>
      <input type="file" accept=".mp3,.wav" onChange={handleFileChange} />
      <button onClick={handleUpload} disabled={loading}>
        {loading ? "Uploading..." : "Find Similar Songs"}
      </button>
      {error && <p style={{ color: "red" }}>{error}</p>}
      {similarSongs.length > 0 && (
        <div>
          <h2>Similar Songs</h2>
          <ul>
            {similarSongs.map((song, index) => (
              <li key={index}>
                <strong>Title:</strong> {song.metadata.title} <br />
                <strong>Artist:</strong> {song.metadata.artist_name} <br />
                <strong>Album:</strong> {song.metadata.album_name} <br />
                <strong>Year:</strong> {song.metadata.year} <br />
                <strong>Similarity:</strong> {song.similarity === 0 ? "Very Low" : song.similarity.toFixed(2) + "%"} <br />
                <em>File Path:</em> {song.song}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
};

export default SongSimilarity;
