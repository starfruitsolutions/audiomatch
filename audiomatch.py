import os
import librosa
import numpy as np
from scipy.signal import correlate
import argparse
import time
from concurrent.futures import ThreadPoolExecutor

# Function to load audio
def load_audio(file_path, sr=500):
    audio, sr = librosa.load(file_path, sr=sr, dtype='float32')
    return audio, sr

# Function to compute cross-correlation between two audio signals
def compute_cross_correlation(sample_audio, song_audio):
    correlation = correlate(song_audio, sample_audio, mode='valid')
    return np.max(correlation)  # Return the maximum correlation value as the similarity measure

# Function to load all songs and compute cross-correlation
def load_songs_and_compare(folder_path, sample_audio, sample_sr):
    best_correlation = float('-inf')
    best_match = None

    with ThreadPoolExecutor() as executor:
        futures = []
        for filename in os.listdir(folder_path):
            if filename.endswith(".mp3") or filename.endswith(".wav"):
                file_path = os.path.join(folder_path, filename)
                futures.append(executor.submit(load_and_compare, file_path, sample_audio, sample_sr))

        for future in futures:
            song_name, correlation = future.result()
            print(f"Song: {song_name}, Correlation: {correlation}")

            if correlation > best_correlation:
                correlation_spread = correlation - best_correlation
                best_correlation = correlation
                best_match = song_name

    return best_match, best_correlation, correlation_spread

# Function to load song and compare using cross-correlation
def load_and_compare(file_path, sample_audio, sample_sr):
    song_audio, song_sr = librosa.load(file_path, sr=sample_sr, dtype='float32')
    correlation = compute_cross_correlation(sample_audio, song_audio)
    return file_path, correlation

# Argument parsing for dynamic clip file input
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Compare audio sample to multiple songs in a folder using cross-correlation.")
    parser.add_argument('clip_file', type=str, help="Path to the audio clip file (wav, mp3)")
    parser.add_argument('songs_folder', type=str, help="Path to the folder containing potential songs")

    args = parser.parse_args()

    # Start the timer
    start_time = time.time()

    # Load the audio sample
    sample_audio, sample_sr = load_audio(args.clip_file)

    # Load all songs from the folder and compute cross-correlation
    best_match, best_correlation, correlation_spread = load_songs_and_compare(args.songs_folder, sample_audio, sample_sr)

    # Output the best matching song and some stats
    print(f"\nBest Match: {best_match}")
    print(f"Correlation: {best_correlation}")
    print(f"Spread: {correlation_spread}")

    # Stop the timer and calculate the runtime
    end_time = time.time()
    total_time = end_time - start_time
    print(f"\nTotal runtime: {total_time:.2f} seconds")
