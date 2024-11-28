from fastapi import FastAPI, File, UploadFile
import os
import faiss
import tempfile
import librosa
import numpy as np

app = FastAPI()

def load_file_paths(file_paths_file='./file_paths.npy'):
    if not os.path.exists(file_paths_file):
        raise FileNotFoundError(f"File paths file not found at: {file_paths_file}")
    return np.load(file_paths_file, allow_pickle=True)

def load_faiss_index(index_file='./song_similarity.index'):
    if not os.path.exists(index_file):
        raise FileNotFoundError(f"FAISS index file not found at: {index_file}")
    return faiss.read_index(index_file)


# @app.post("/api/upload-and-find")
# async def upload_and_find(file: UploadFile, k:int=5):
#     # Save the uploaded file temporarily
#     with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
#         temp_file.write(await file.read())
#         temp_path = temp_file.name

#     # Extract features using librosa
#     try:
#         y, sr = librosa.load(temp_path, sr=None)
#         mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
#         query_features = np.mean(mfcc_features.T, axis=0).astype(np.float32)

#     except Exception as e:
#         return {"error": f"Could not process the uploaded file: {str(e)}"}
#     finally:
#         os.remove(temp_path)  # Clean up

#     # Find similar songs using your FAISS index
#     index = load_faiss_index()
#     query_features = query_features.reshape(1, -1)
#     distances, indices = index.search(query_features, k=k)

#     # Retrieve file paths from indices
#     file_paths = load_file_paths()
#     similar_songs = [
#         {"song": file_paths[idx],
#         "similarity": float(dist)
#         }
#         for idx, dist in zip(indices[0], distances[0])
#     ]


#     return {"similar_songs": similar_songs}

@app.post("/api/upload-and-find")
async def upload_and_find(file: UploadFile, k: int = 5):
    # Save the uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(await file.read())
        temp_path = temp_file.name

    # Extract features using librosa
    try:
        y, sr = librosa.load(temp_path, sr=None)
        mfcc_features = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=12)
        query_features = np.mean(mfcc_features.T, axis=0).astype(np.float32)

    except Exception as e:
        return {"error": f"Could not process the uploaded file: {str(e)}"}
    finally:
        os.remove(temp_path)  # Clean up

    # Find similar songs using your FAISS index
    index = load_faiss_index()
    query_features = query_features.reshape(1, -1)
    distances, indices = index.search(query_features, k=k)

    # Normalize the distances to a range of 0 to 1
    try:
        file_paths = load_file_paths()
        max_distance = max(distances[0])  # Find the maximum distance
        min_distance = min(distances[0])  # Find the minimum distance

        if max_distance == min_distance:  # Avoid division by zero
            normalized_distances = [1.0] * len(distances[0])  # If all distances are equal, set all scores to 1
        else:
            normalized_distances = [
                1 - (dist - min_distance) / (max_distance - min_distance)  # Normalize and invert
                for dist in distances[0]
            ]

        similar_songs = [
            {
                "song": file_paths[idx],
                "similarity": norm_dist
            }
            for idx, norm_dist in zip(indices[0], normalized_distances)
        ]
    except Exception as e:
        return {"error": f"Error retrieving or normalizing file paths: {str(e)}"}

    return {"similar_songs": similar_songs}
