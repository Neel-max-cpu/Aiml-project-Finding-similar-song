import h5py
import numpy as np

def extract_metadata(file_path):
    try:
        with h5py.File(file_path, 'r') as h5_file:
            # Extracting metadata from the "songs" dataset in the "metadata" group
            songs_data = h5_file['metadata']['songs'][0]  # Get the first (and probably only) song
            
            # Extracting fields from the structured array
            metadata = {}

            # Extract fields from the structured array
            metadata["title"] = songs_data['title'].decode('utf-8') if 'title' in songs_data.dtype.names else 'Unknown Title'
            metadata["artist_name"] = songs_data['artist_name'].decode('utf-8') if 'artist_name' in songs_data.dtype.names else 'Unknown Artist'
            metadata["album_name"] = songs_data['release'].decode('utf-8') if 'release' in songs_data.dtype.names else 'Unknown Album'
            metadata["year"] = int(songs_data['year']) if 'year' in songs_data.dtype.names else 'Unknown Year'

            # Extracting additional metadata like artist_terms and similar_artists
            artist_terms = h5_file['metadata']['artist_terms']
            artist_terms_freq = h5_file['metadata']['artist_terms_freq']
            similar_artists = h5_file['metadata']['similar_artists']

            # Convert to lists if they are not empty arrays
            metadata["artist_terms"] = artist_terms[:].tolist() if artist_terms.size > 0 else []
            metadata["artist_terms_freq"] = artist_terms_freq[:].tolist() if artist_terms_freq.size > 0 else []
            metadata["similar_artists"] = similar_artists[:].tolist() if similar_artists.size > 0 else []

        return metadata
    except Exception as e:
        print(f"Error extracting metadata: {e}")
        return None

if __name__ == "__main__":
    # Test the function on one of your .h5 files
    # test_file_path = "./public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5"
    test_file_path = "C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5"
    metadata = extract_metadata(test_file_path)

    if metadata:
        print("Extracted Metadata:")
        print(metadata)
    else:
        print("Failed to extract metadata.")



    
    
# test_file_path = "C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5"

