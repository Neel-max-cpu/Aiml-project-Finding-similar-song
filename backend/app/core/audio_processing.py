import numpy as np
import os
import h5py
from sklearn.metrics.pairwise import cosine_similarity

def calculate_similarity(features1, features2):
    """Calculate cosine similarity between two feature vectors."""
    return cosine_similarity([features1], [features2])[0][0]

def load_features(file):
    """Load audio features from an .h5 file."""
    try:
        print(f"Loading features from {file}...")
        with h5py.File(file, 'r') as f:
            # Check if the key exists before accessing it
            if 'analysis/segments_timbre' in f:
                features = f['analysis/segments_timbre'][:].flatten()[:12]  # Take only the first 12 values
                print(f"Loaded features for {file}: {features}")  # Print the loaded features for verification
                return features
            else:
                print(f"Key 'analysis/segments_timbre' not found in {file}")
                return None
    except Exception as e:
        print(f"Error loading {file}: {e}")
        return None

def process_in_batches(base_path, batch_size=100):
    """Process files in batches to optimize memory usage."""
    # Use os.walk to find all .h5 files in subdirectories
    files = []
    for root, dirs, files_in_dir in os.walk(base_path):
        for file in files_in_dir:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                files.append(file_path)
                print(f"Found file: {file_path}")  # Print all found .h5 files

    # If no .h5 files are found, notify and exit
    if not files:
        print(f"No .h5 files found in {base_path}")
        return {}

    features_dict = {}
    
    # Process files in batches
    for batch_start in range(0, len(files), batch_size):
        batch_files = files[batch_start:batch_start + batch_size]
        print(f"Processing batch {batch_start//batch_size + 1}...")
        
        for idx, file in enumerate(batch_files):
            features = load_features(file)
            if features is not None:
                features_dict[file] = features
        
        print(f"Processed {len(batch_files)} files in this batch.")
    return features_dict

def find_similar_songs(base_path, threshold=0.95, batch_size=100):
    """Find similar songs by comparing feature vectors."""
    print("Starting the process of finding similar songs...")
    
    features_dict = process_in_batches(base_path, batch_size)
    
    if len(features_dict) == 0:
        print("No features were loaded, exiting process.")
        return

    print(f"Loaded features for {len(features_dict)} songs, starting similarity comparisons...")

    # Open the result file to save the similarity results
    with open("similarity_results.txt", "w") as f:
        # Sequential similarity comparison
        for file1, feature1 in features_dict.items():
            print(f"Comparing {file1} with others...")
            similar_songs = []
            for file2, feature2 in features_dict.items():
                if file1 != file2:
                    similarity = calculate_similarity(feature1, feature2)
                    print(f"Similarity between {file1} and {file2}: {similarity:.4f}")  # Debugging similarity score
                    if similarity >= threshold:
                        similar_songs.append((file2, similarity))
            
            # Sort and save similar songs for the current file
            similar_songs.sort(key=lambda x: x[1], reverse=True)
            f.write(f"\nSimilar songs to {file1}:\n")
            for song, similarity in similar_songs:
                f.write(f"Song: {song}, Similarity: {similarity:.4f}\n")

    print("Similarity comparison process completed and results saved to similarity_results.txt.")

# Run the function to find similar songs
base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
find_similar_songs(base_path)
