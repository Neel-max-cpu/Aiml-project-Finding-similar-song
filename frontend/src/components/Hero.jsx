import React, { useState } from "react";
import axios from "axios";
import MainCard from "./MainCard";
import Podium from "./Podium";


const Hero = () => {
  const testSongs = [
    {
      "id": 1,
      "metadata": {
        "title": "abc",
        "artist_name": "abc",
        "album_name": "xyz",
        "year": 1960,


      }
    },
    {
      "id": 2,
      "metadata": {
        "title": "abc",
        "artist_name": "abc",
        "album_name": "xyz",
        "year": 1960,


      }
    },
    {
      "id": 3,
      "metadata": {
        "title": "abc",
        "artist_name": "abc",
        "album_name": "xyz",
        "year": 1960,


      }
    },
    {
      "id": 4,
      "metadata": {
        "title": "abc",
        "artist_name": "abc",
        "album_name": "xyz",
        "year": 1960,


      }
    }
  ]
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
      console.log(similarSongs)
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  // sort the songs based on similarity
  const sortedSongs = [...similarSongs].sort((a, b) => b.similarity - a.similarity);

  return (
    <div className='flex justify-center'>
      <div className="w-full flex flex-col justify-center items-center m-4 ">

        <h1 className="text-5xl font-semibold mt-12 mb-12">Copy Right Check!</h1>
        <div className="flex flex-col sm:flex-row">

          <input className="file:bg-blue-600 file:text-white file:border-none file:rounded-full file:py-2 file:px-4 file:cursor-pointer border border-slate-600 p-2 rounded-full sm:mr-4 mb-4 sm:mb-0" type="file" accept=".mp3,.wav" onChange={handleFileChange} />
          <button className="bg-black text-white rounded-full  py-4 px-6" onClick={handleUpload} disabled={loading}>
            {loading ? "Uploading..." : "Find Similar Songs"}
          </button>
        </div>
        {error && <p className="my-4 text-red-600">{error}</p>}
        {similarSongs.length > 0 && (
          <div className=" mt-10 w-full">
            <h2 className="text-center text-3xl mb-5">Top Similar Songs</h2>
            <Podium topSongs={sortedSongs.slice(0, 3)} />
           <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 mx-6">
              {/* Map the sorted songs to MainCard */}
              {sortedSongs.map((song, index) => (
                <MainCard song={song} index={index}/>              
              ))}
           </div>
            
          </div>
        )}
      </div>
    </div>
  )
}

export default Hero
