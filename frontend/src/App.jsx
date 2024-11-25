import React, { useState } from "react";

function App() {
  const [file, setFile] = useState(null);
  const [similarSongs, setSimilarSongs] = useState([]);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("/api/upload-and-find", {
      method: "POST",
      body: formData,
    });

    const data = await response.json();
    setSimilarSongs(data.similar_songs);
  };

  return (
    <div>
      <input type="file" onChange={handleFileChange} />
      <button onClick={handleSubmit}>Find Similar Songs</button>
      <ul>
        {similarSongs.map((song, index) => (
          <li key={index}>{song}</li>
        ))}
      </ul>
    </div>
  );
}

export default App;
