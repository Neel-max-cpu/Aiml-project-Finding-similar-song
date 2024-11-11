import h5py

def list_datasets(file_path):
    try:
        with h5py.File(file_path, 'r') as f:
            # Check for the 'analysis' group and list its datasets
            if 'analysis' in f:
                analysis_group = f['analysis']
                print(f"Datasets in 'analysis' group of {file_path}:")
                for name in analysis_group:
                    print(name)  # This will print all datasets under 'analysis'
            else:
                print(f"No 'analysis' group in {file_path}")
    except Exception as e:
        print(f"Error loading {file_path}: {e}")

if __name__ == "__main__":
    # Provide the path to one of your .h5 files here
    file_path = 'C:/Users/NEEL/Desktop/new Coding/react1/find_similar_songs/backend/public/MillionSongSubset/A/A/A/TRAAAAW128F429D538.h5'  # Replace with your file path
    list_datasets(file_path)
