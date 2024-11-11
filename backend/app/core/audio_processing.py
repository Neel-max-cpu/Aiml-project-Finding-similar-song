# backend/app/core/audio_processing.py

import numpy as np
from scipy.spatial.distance import cosine
from app.core.data_loader import get_h5_files, load_h5_file

def cosine_similarity(features1, features2):
    """
    Calculate cosine similarity between two feature vectors.

    Args:
        features1 (numpy.ndarray): Feature vector of the first song.
        features2 (numpy.ndarray): Feature vector of the second song.

    Returns:
        float: Cosine similarity score (0 to 1, where 1 means identical).
    """
    return 1 - cosine(features1, features2)

def find_similar_songs(input_song_features, all_files, threshold=0.9):
    """
    Find songs that are similar to the input song based on feature similarity.

    Args:
        input_song_features (numpy.ndarray): Feature vector of the input song.
        all_files (list): List of all .h5 file paths.
        threshold (float): Minimum similarity score to consider songs as similar.

    Returns:
        list: List of tuples (file_path, similarity) for similar songs.
    """
    similar_songs = []
    
    for file in all_files:
        features = load_h5_file(file)
        if features is not None:
            similarity = cosine_similarity(input_song_features, features)
            if similarity >= threshold:
                similar_songs.append((file, similarity))
    
    # Sort similar songs by similarity score (highest first)
    similar_songs = sorted(similar_songs, key=lambda x: x[1], reverse=True)
    
    return similar_songs



def test_find_similar_songs():
    base_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset'
    files = get_h5_files(base_path)
    
    print(f"Found {len(files)} files.")  # Debugging: Print the number of files found
    
    # Get the features for the first file (or any file you want)
    first_song_features = load_h5_file(files[0])
    if first_song_features is None:
        print("No features loaded for the first song.")
        return
    
    print(f"Features for {files[0]}: {first_song_features}")  # Debugging: Print the features of the first song
    
    # Find similar songs with the first song's features
    similar_songs = find_similar_songs(first_song_features, files, threshold=0.95) 
    
    if not similar_songs:
        print("No similar songs found.")
    else:
        print(f"Similar songs to {files[0]}:")
        for song, similarity in similar_songs:
            print(f"Song: {song}, Similarity: {similarity}")


if __name__ == "__main__":
    test_find_similar_songs()
