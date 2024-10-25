
# Audio Matching with Cross-Correlation

This matches a short audio clip against a set of potential audio files by to find the best match. It is useful for identifying which audio a clip belongs to, even if there is significant distortion.

## How It Works

The script compares the audio sample to each song using **cross-correlation**, a technique that slides the audio clip along the length of each song to measure the similarity. The song with the highest correlation score is considered the best match.

## Features
- Uses **cross-correlation** to compare audio samples with songs.
- Loads and processes multiple songs in parallel.
- Supports **MP3** and **WAV** file formats.

## Requirements

Make sure you have the following dependencies installed:

- `librosa`
- `numpy`
- `scipy`

You can install the necessary dependencies using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## Usage

```bash
python3 audiomatch.py [-h] [--sample-rate SAMPLE_RATE] clip_file song_folder
```

### Example

```bash
python3 audiomatch.py clip-1.wav potential
```

## Output

This will compare the provided audio clip with all songs in the audio folder and output the best match.

```
Song: potential/song1.mp3, Correlation: 0.875
Song: potential/song2.mp3, Correlation: 0.912
Song: potential/song3.mp3, Correlation: 0.743

The best matching song is: potential/song2.mp3 with correlation 0.912
```

