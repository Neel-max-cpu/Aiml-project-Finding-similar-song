# import numpy as np
# import os
# import h5py
# from sklearn.metrics.pairwise import cosine_similarity

# def calculate_similarity(features1, features2):
#     """Calculate cosine similarity between two feature vectors."""
#     return cosine_similarity([features1], [features2])[0][0]

# def load_features(file):
#     """Load audio features from an .h5 file."""
#     try:
#         print(f"Loading features from {file}...")
#         with h5py.File(file, 'r') as f:
#             # Check if the key exists before accessing it
#             if 'analysis/segments_timbre' in f:
#                 features = f['analysis/segments_timbre'][:].flatten()[:12]  # Take only the first 12 values
#                 print(f"Loaded features for {file}: {features}")  # Print the loaded features for verification
#                 return features
#             else:
#                 print(f"Key 'analysis/segments_timbre' not found in {file}")
#                 return None
#     except Exception as e:
#         print(f"Error loading {file}: {e}")
#         return None

# def process_in_batches(base_path, batch_size=100):
#     """Process files in batches to optimize memory usage."""
#     # Use os.walk to find all .h5 files in subdirectories
#     files = []
#     for root, dirs, files_in_dir in os.walk(base_path):
#         for file in files_in_dir:
#             if file.endswith('.h5'):
#                 file_path = os.path.join(root, file)
#                 files.append(file_path)
#                 print(f"Found file: {file_path}")  # Print all found .h5 files

#     # If no .h5 files are found, notify and exit
#     if not files:
#         print(f"No .h5 files found in {base_path}")
#         return {}

#     features_dict = {}
    
#     # Process files in batches
#     for batch_start in range(0, len(files), batch_size):
#         batch_files = files[batch_start:batch_start + batch_size]
#         print(f"Processing batch {batch_start//batch_size + 1}...")
        
#         for idx, file in enumerate(batch_files):
#             features = load_features(file)
#             if features is not None:
#                 features_dict[file] = features
        
#         print(f"Processed {len(batch_files)} files in this batch.")
#     return features_dict

# def find_similar_songs(base_path, threshold=0.95, top_n=10, batch_size=100):
#     """Find similar songs by comparing feature vectors."""
#     print("Starting the process of finding similar songs...")
    
#     features_dict = process_in_batches(base_path, batch_size)
    
#     if len(features_dict) == 0:
#         print("No features were loaded, exiting process.")
#         return

#     print(f"Loaded features for {len(features_dict)} songs, starting similarity comparisons...")

#     # Open the result file to save the similarity results
#     with open("similarity_results.txt", "w") as f:
#         # Sequential similarity comparison
#         for file1, feature1 in features_dict.items():
#             print(f"Comparing {file1} with others...")
#             similar_songs = []
#             for file2, feature2 in features_dict.items():
#                 if file1 != file2:
#                     similarity = calculate_similarity(feature1, feature2)
#                     print(f"Similarity between {file1} and {file2}: {similarity:.4f}")  # Debugging similarity score
#                     if similarity >= threshold:
#                         similar_songs.append((file2, similarity))
            
#             # Sort and save only the top N most similar songs for the current file
#             similar_songs.sort(key=lambda x: x[1], reverse=True)
#             top_similar_songs = similar_songs[:top_n]  # Limit to the top N similar songs
            
#             f.write(f"\nSimilar songs to {file1}:\n")
#             for song, similarity in top_similar_songs:
#                 f.write(f"Song: {song}, Similarity: {similarity:.4f}\n")

#     print("Similarity comparison process completed and results saved to similarity_results.txt.")

# # Run the function to find similar songs
# base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
# find_similar_songs(base_path, threshold=0.95, top_n=10)  # Adjust the threshold and top_n as needed

import faiss
import numpy as np
import h5py
import os
from sklearn.preprocessing import normalize


# Load the precomputed FAISS index from the root directory
def load_faiss_index(index_file='./song_similarity.index'):
    """Load the precomputed FAISS index."""
    index = faiss.read_index(index_file)
    return index

def load_features(file):
    """Load and normalize audio features from an .h5 file."""
    try:
        with h5py.File(file, 'r') as f:
            if 'analysis/segments_timbre' in f:
                features = f['analysis/segments_timbre'][:].flatten()[:12]
                features = normalize([features])[0]  # Normalize features before returning
                return features
    except Exception as e:
        print(f"Error loading {file}: {e}")
    return None

def get_file_paths(base_path):
    """Generate a list of file paths for all .h5 files in the directory."""
    file_paths = []
    for root, dirs, files in os.walk(base_path):
        for file in files:
            if file.endswith('.h5'):
                file_paths.append(os.path.join(root, file))
    return file_paths

def find_similar_songs(query_file, index, file_paths, k=5):
    """Find the top k most similar songs using the FAISS index."""
    query_features = load_features(query_file)
    if query_features is None:
        return []
    
    # Print query features for verification
    print(f"Query Features: {query_features}")
    
    query_feature = np.array([query_features], dtype=np.float32)
    
    distances, indices = index.search(query_feature, k)
    similar_songs = [(file_paths[idx], distances[0][i]) for i, idx in enumerate(indices[0])]
    
    # Print the features of similar songs
    for song, _ in similar_songs:
        print(f"Similar Song: {song}, Features: {load_features(song)}")
    
    return similar_songs

# Example usage
base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
index = load_faiss_index()  # Load the precomputed index
file_paths = get_file_paths(base_path)  # Get the list of file paths corresponding to the .h5 files

query_file = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5'  # Example query song file path
similar_songs = find_similar_songs(query_file, index, file_paths)

# Display similar songs
for song, similarity in similar_songs:
    print(f"Song: {song}, Similarity: {similarity:.4f}")
