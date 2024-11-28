from fastapi import APIRouter, File, UploadFile, HTTPException
import os
import faiss
import tempfile
import librosa
import numpy as np





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
        similar_songs = [
            {"song": file_paths[idx], "similarity": float(dist)}
            for idx, dist in zip(indices[0], distances[0])
        ]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving file paths: {str(e)}")

    return {"similar_songs": similar_songs}
