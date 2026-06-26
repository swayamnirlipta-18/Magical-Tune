# Song Recognizer
#Project Overview

This project implements a simplified Shazam-like music recognition system. It identifies songs from short audio clips using spectrogram-based fingerprinting instead of comparing raw audio signals.

#Working Principle
Audio signal is converted into a spectrogram (time–frequency representation)
Strong local maxima (peaks) are extracted to form a constellation map

Nearby peaks are paired to generate compact audio hashes

(frequency1, frequency2, Δtime)
These hashes are stored in a database for reference songs
A query clip is matched by comparing hashes and finding the best time-offset alignment
#Features
Upload and analyze audio clips
Generate spectrogram visualization
Detect peak constellation points
Build and match audio fingerprints
Display recognized song result
#Key Idea

A correct match produces a large number of consistent time-offset alignments, while incorrect matches produce scattered random matches.

#Observations
Short FFT window → better time resolution, lower frequency resolution
Long FFT window → better frequency resolution, lower time resolution
System is robust to moderate noise but sensitive to pitch shifts
#Tools Used

Python, NumPy, SciPy, Matplotlib, Streamlit

#Output
Spectrogram plot
Peak constellation map
Final matched song name
# Conclusion

This system demonstrates how audio fingerprinting and spectral peak matching can be used for fast and efficient music recognition, similar to realworld applications like Shazam.
