import os
import librosa
import numpy as np
from scipy.signal import correlate
import argparse
import time
from concurrent.futures import ThreadPoolExecutor


# Function to load audio
def load_audio(file_path, sample_rate):
	audio, _ = librosa.load(file_path, sr=sample_rate, dtype='float32')
	return audio

# Function to load song and compare using cross-correlation
def compare(file_path, sample_audio, sample_rate):
	song_audio = load_audio(file_path, sample_rate)
	correlation = correlate(song_audio, sample_audio, mode='valid')
	return file_path, np.max(correlation)

def runComparison(clip_file, song_folder, sample_rate):
	# Load and compute cross-correlation
	sample_audio = load_audio(clip_file, sample_rate)
	best_correlation = float('-inf')
	best_match = None

	with ThreadPoolExecutor() as executor:
		futures = []
		for filename in os.listdir(song_folder):
			if filename.endswith(".mp3") or filename.endswith(".wav"):
				file_path = os.path.join(song_folder, filename)
				futures.append(executor.submit(compare, file_path, sample_audio, sample_rate))

		for future in futures:
			song_name, correlation = future.result()
			print(f"Song: {song_name}, Correlation: {correlation}")

			if correlation > best_correlation:
				correlation_spread = correlation - best_correlation
				best_correlation = correlation
				best_match = song_name

	return best_match, best_correlation, correlation_spread

# Argument parsing for dynamic clip file input
if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Compare audio sample to multiple songs in a folder using cross-correlation.")
	parser.add_argument('clip_file', type=str, help="Path to the audio clip file (wav, mp3)")
	parser.add_argument('song_folder', type=str, help="Path to the folder containing potential songs")
	parser.add_argument('--sample-rate', type=int, default=2000, help="Sample rate for audio processing")

	args = parser.parse_args()

	# Start the timer
	start_time = time.time()

	best_match, best_correlation, correlation_spread = runComparison(args.clip_file, args.song_folder, args.sample_rate)

	total_time = time.time() - start_time

	# Output the best matching song and some stats
	print(f"\nBest Match: {best_match}")
	print(f"Correlation: {best_correlation}")
	print(f"Spread: {correlation_spread}")

	print(f"\nTotal runtime: {total_time:.2f} seconds")
