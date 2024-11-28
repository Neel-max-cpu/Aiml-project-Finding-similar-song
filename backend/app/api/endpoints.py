# from fastapi import APIRouter, File, UploadFile, HTTPException
# import os
# import faiss
# import tempfile
# import librosa
# import numpy as np
# import h5py



# # @router.post("/upload-and-find")
# # async def upload_and_find(file: UploadFile = File(...)):
  
    
# #     try:
# #         logging.debug(f"Received file: {file.filename}")
# #         # Process the file here
# #     except Exception as e:
# #         logging.error(f"Error occurred: {e}")
# #         raise HTTPException(status_code=500, detail="Internal Server Error")





# # covert to csv---


# # import h5pyimport pandas as pd 

# # paths = []with h5py.File('examples/test.h5','r') as hf:
# #     hf.visit(paths.append)
# # dt = pd.HDFStore('examples/test.h5').get(paths[1])
# # dt.to_csv('test.csv')



# router = APIRouter()

# def load_file_paths(file_paths_file='./file_paths.npy'):
#     """Load the list of file paths used for indexing."""
#     if not os.path.exists(file_paths_file):
#         raise HTTPException(status_code=500, detail="File paths file not found.")
#     return np.load(file_paths_file, allow_pickle=True)

# def load_faiss_index(index_file='./song_similarity.index'):
#     """Load the precomputed FAISS index."""
#     if not os.path.exists(index_file):
#         raise HTTPException(status_code=500, detail="FAISS index file not found.")
#     return faiss.read_index(index_file)


# @router.post("/upload-and-find")
# async def upload_and_find(file: UploadFile):
#     # Save the uploaded file temporarily
#     if not file.filename.endswith(('.mp3', '.wav')):
#         raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an MP3 or WAV file.")
    
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
#         temp_file.write(await file.read())
#         temp_path = temp_file.name

#     try:
#         # Load the audio file and extract features
#         y, sr = librosa.load(temp_path, sr=None)
#         mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
#         query_features = np.mean(mfcc_features.T, axis=0).astype(np.float32)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error processing the uploaded file: {str(e)}")
#     finally:
#         os.remove(temp_path)  # Clean up the temporary file

#     # Find similar songs using the FAISS index
#     try:
#         index = load_faiss_index()
#         query_features = query_features.reshape(1, -1)
#         distances, indices = index.search(query_features, k=5)
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error querying the FAISS index: {str(e)}")

#     # Retrieve file paths from indices
#     try:
#         file_paths = load_file_paths()
#         similar_songs = [
#             {"song": file_paths[idx], "similarity": float(dist)}
#             for idx, dist in zip(indices[0], distances[0])
#         ]
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error retrieving file paths: {str(e)}")

#     return {"similar_songs": similar_songs}




from fastapi import APIRouter, File, UploadFile, HTTPException
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
                year = "Unknown Year"

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

@router.post("/upload-and-find")
async def upload_and_find(file: UploadFile):
    # Save the uploaded file temporarily
    if not file.filename.endswith(('.mp3', '.wav')):
        raise HTTPException(status_code=400, detail="Unsupported file format. Please upload an MP3 or WAV file.")
    
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    try:
        # Load the audio file and extract features
        y, sr = librosa.load(temp_path, sr=None)
        mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
        query_features = np.mean(mfcc_features.T, axis=0).astype(np.float32)

        # Replace NaN values with zeros
        query_features = np.nan_to_num(query_features, nan=0.0)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing the uploaded file: {str(e)}")
    finally:
        os.remove(temp_path)  # Clean up the temporary file

    # Find similar songs using the FAISS index
    try:
        index = load_faiss_index()
        query_features = query_features.reshape(1, -1)
        distances, indices = index.search(query_features, k=5)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error querying the FAISS index: {str(e)}")

    # Retrieve file paths from indices
    try:
        file_paths = load_file_paths()
        similar_songs = []

        # Find min and max distances for normalization
        min_dist = np.min(distances)
        max_dist = np.max(distances)

        for idx, dist in zip(indices[0], distances[0]):
            song_file_path = file_paths[idx]
            song_metadata = extract_metadata(song_file_path)

            # Normalize the similarity score to be between 0 and 100
            normalized_similarity = 100 - ((dist - min_dist) / (max_dist - min_dist)) * 100
            normalized_similarity = np.nan_to_num(normalized_similarity, nan=0.0)  # Ensure no NaN values

            # if normalized_similarity == 0:
            #     normalized_similarity = "Very Small"
            # else:
            #     normalized_similarity = float(normalized_similarity)

            similar_songs.append({
                "song": song_file_path,
                "similarity": float(normalized_similarity),
                # "similarity": normalized_similarity,
                "metadata": song_metadata,
            })
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file paths or metadata: {str(e)}")

    return {"similar_songs": similar_songs}
