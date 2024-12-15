from fastapi import APIRouter, File, UploadFile, HTTPException
from sklearn.preprocessing import normalize
import os
import faiss
import tempfile
import librosa
import numpy as np
import h5py

router = APIRouter()

def load_file_paths(file_paths_file='./file_paths.npy'):
    """Load the list of file paths used for indexing."""
    if not os.path.exists(file_paths_file):
        raise HTTPException(status_code=500, detail="File paths file not found.")
    return np.load(file_paths_file, allow_pickle=True)

def load_faiss_index(index_file='./song_similarity.index'):
    """Load the precomputed FAISS index."""
    if not os.path.exists(index_file):
        raise HTTPException(status_code=500, detail="FAISS index file not found.")
    return faiss.read_index(index_file)

def extract_metadata(file_path):
    """Extract metadata from a single .h5 file."""
    try:
        with h5py.File(file_path, 'r') as h5_file:
            # Metadata is in the `/metadata/songs` group
            metadata_group = h5_file['/metadata/songs']

            # Extract fields from the metadata group
            title = metadata_group['title'][0].decode('utf-8') if 'title' in metadata_group.dtype.names else "Unknown"
            artist_name = metadata_group['artist_name'][0].decode('utf-8') if 'artist_name' in metadata_group.dtype.names else "Unknown"
            album_name = metadata_group['release'][0].decode('utf-8') if 'release' in metadata_group.dtype.names else "Unknown"

            # Musicbrainz group contains additional information
            musicbrainz_group = h5_file['/musicbrainz/songs']
            # year = musicbrainz_group['year'][0] if 'year' in musicbrainz_group.dtype.names else None                   
            year = musicbrainz_group['year'][0] if 'year' in musicbrainz_group.dtype.names else 0                   
            if isinstance(year, (int, np.integer)) and year > 0:
                year = int(year)
            else:
                year = "Unknown"

            return {
                "title": title,
                "artist_name": artist_name,
                "album_name": album_name,
                # "year": int(year) if isinstance(year, (int, np.integer)) else "Unknown",                                   
                "year": year,
            }
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None

def normalize_similarity(distances, min_dist=0, max_dist=300):  # Assume 300 as a reasonable max distance
    similarities = 100 - ((distances - min_dist) / (max_dist - min_dist)) * 100
    similarities = np.clip(similarities, 0, 99)  # Cap at 99% to avoid misleading results
    return similarities


@router.post("/upload-and-find")
async def upload_and_find(file: UploadFile):
    if not file.filename.endswith(('.mp3', '.wav')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an MP3 or WAV file.")

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        # Load and normalize the audio file
        y, sr = librosa.load(temp_path, sr=None)
        mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
        query_features = np.mean(mfcc_features.T, axis=0).astype(np.float32)
        query_features /= np.linalg.norm(query_features)  # L2 normalize the query
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded file: {str(e)}")
    finally:
        os.remove(temp_path)

    try:
        # Load FAISS index and search
        index = load_faiss_index()
        query_features = query_features.reshape(1, -1)
        distances, indices = index.search(query_features, k=5)

        # Normalize distances into similarity scores
        similarities = normalize_similarity(distances[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the FAISS index: {str(e)}")

    try:
        # Map results to file paths and metadata
        file_paths = load_file_paths()
        similar_songs = [
            {
                "song": file_paths[idx],
                "similarity": float(sim),
                "metadata": extract_metadata(file_paths[idx])
            }
            for idx, sim in zip(indices[0], similarities)
            if file_paths[idx] != temp_path  # Exclude self-match
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file paths or metadata: {str(e)}")

    return {"similar_songs": similar_songs}