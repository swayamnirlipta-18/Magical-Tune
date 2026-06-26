#!/usr/bin/env python
# coding: utf-8

# In[4]:


import os
from collections import defaultdict

import librosa
import matplotlib.pyplot as plt
import numpy as np
from skimage.feature import peak_local_max


# Load Song
def load_song(path):
    y, sr = librosa.load(path, sr=None)
    return y, sr


# Spectrogram
def create_spectrogram(y):
    D = librosa.stft(y, n_fft=2048)
    S = librosa.amplitude_to_db(np.abs(D), ref=np.max)
    return S


# Peak Detection
def find_peaks(S):
    peaks = peak_local_max(
        S,
        min_distance=50,
        threshold_abs=-25
    )
    return peaks


# Plot Spectrogram
def plot_spectrogram(S):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.imshow(
        S,
        origin="lower",
        aspect="auto",
        cmap="magma"
    )

    ax.set_title("Spectrogram")
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


# Plot Constellation
def plot_constellation(peaks):
    fig, ax = plt.subplots(figsize=(12,6))
    ax.scatter(
        peaks[:,1],
        peaks[:,0],
        s=10,
        color="cyan"
    )

    ax.set_title("Constellation Map")
    ax.set_xlabel("Time")
    ax.set_ylabel("Frequency")
    fig.tight_layout()
    return fig


# Generate Hashes
def generate_hashes(peaks):
    hashes = []
    fan_value = 5
    peaks = peaks[np.argsort(peaks[:,1])]
    for i in range(len(peaks)):
        for j in range(1, fan_value+1):
            if i+j < len(peaks):
                f1 = int(peaks[i][0])
                f2 = int(peaks[i+j][0])
                t1 = int(peaks[i][1])
                t2 = int(peaks[i+j][1])
                delta_t = t2 - t1
                if delta_t <= 0:
                    continue
                hash_key = (f1, f2, delta_t)
                hashes.append((hash_key, t1))

    return hashes

# Database
database = {}


# Add Song
def add_song_to_database(song_name, hashes):
    for hash_key, t1 in hashes:
        if hash_key not in database:
            database[hash_key] = []
        database[hash_key].append(
            (song_name,t1)
        )


# Process Song
def process_song(path):
    y, sr = load_song(path)
    S = create_spectrogram(y)
    peaks = find_peaks(S)
    hashes = generate_hashes(peaks)
    return peaks, hashes


# Build Database
def build_database(song_folder):
    global database
    database = {}
    for file in os.listdir(song_folder):
        if file.endswith(".mp3"):
            path = os.path.join(song_folder,file)
            peaks, hashes = process_song(path)
            add_song_to_database(file,hashes)

            print(file,
                  "Peaks:",len(peaks),
                  "Hashes:",len(hashes))

    print("Database Size:",len(database))


# Match Query
def match_query(query_hashes):
    offset_votes = defaultdict(int)
    for hash_key, query_time in query_hashes:
        if hash_key in database:
            for song_name, db_time in database[hash_key]:
                offset = db_time-query_time
                offset_votes[(song_name,offset)] += 1

    return offset_votes


# Identify Song
def identify_song(query_path):
    y, sr = load_song(query_path)
    S = create_spectrogram(y)
    peaks = find_peaks(S)
    query_hashes = generate_hashes(peaks)
    offset_votes = match_query(query_hashes)
    if len(offset_votes)==0:
        return "No Match", {}
    best_match = max(
        offset_votes,
        key=offset_votes.get
    )

    detected_song = best_match[0]

    return detected_song, offset_votes

# Offset Histogram
def plot_offset_histogram(offset_votes,detected_song):
    offsets=[]
    counts=[]
    for (song,offset),count in offset_votes.items():
        if song==detected_song:
            offsets.append(offset)
            counts.append(count)
    fig, ax = plt.subplots(figsize=(10,5))
    ax.bar(offsets,counts)
    ax.set_title(
        f"Offset Histogram - {detected_song}"
    )
    ax.set_xlabel("Offset")
    ax.set_ylabel("Matches")
    fig.tight_layout()
    return fig

