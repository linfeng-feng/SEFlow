import os
import librosa
import numpy as np

def find_min_vmin(root_folder):
    min_vmin = float('inf')
    max_vmax = -min_vmin
    
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if file.lower().endswith('.flac'):
                file_path = os.path.join(root, file)
                try:
                    y, sr = librosa.load(file_path, sr=None)
                    
                    D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=1.0)
                    
                    current_vmin = np.min(D)
                    if current_vmin < min_vmin:
                        min_vmin = current_vmin
                        print(f"New vmin: {min_vmin:.4f} dB found in {file_path}")
                    
                    current_vmax = np.max(D)
                    if current_vmax > max_vmax:
                        max_vmax = current_vmax
                        print(f"New vmax: {max_vmax:.4f} dB found in {file_path}")
                    
                except Exception as e:
                    print(f"Error processing {file_path}: {str(e)}")
    
    return min_vmin, max_vmax

if __name__ == "__main__":
    folder_path = './'
    min_vmin, max_vmax = find_min_vmin(folder_path)