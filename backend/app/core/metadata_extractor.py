import h5py
import numpy as np
import os

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
            year = musicbrainz_group['year'][0] if 'year' in musicbrainz_group.dtype.names else "Unknown"

            return {
                "title": title,
                "artist_name": artist_name,
                "album_name": album_name,
                "year": int(year) if isinstance(year, (int, np.integer)) else "Unknown",
            }
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None


def preprocess_metadata(dataset_path, output_file='./song_metadata.npy'):
    """Process all .h5 files in the dataset and save metadata."""
    metadata_dict = {}
    for root, _, files in os.walk(dataset_path):
        for file in files:
            if file.endswith('.h5'):
                file_path = os.path.join(root, file)
                metadata = extract_metadata(file_path)
                if metadata:
                    metadata_dict[file_path] = metadata
    np.save(output_file, metadata_dict)
    print(f"Metadata saved to {output_file}")

if __name__ == "__main__":
    # Example usage
    # file_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5'
    # preprocess_metadata('C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset')
    preprocess_metadata('./public/MillionSongSubset')
