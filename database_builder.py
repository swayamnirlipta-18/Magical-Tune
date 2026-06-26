#!/usr/bin/env python
# coding: utf-8

# In[2]:


import os
import pickle
from utils import process_song, add_song_to_database, database
# Folder containing all songs
songs_folder = "SONG"
print("Building fingerprint database...")

# Process every song
for file in os.listdir(songs_folder):
    if file.endswith(".mp3"):
        path = os.path.join(songs_folder, file)
        peaks, hashes = process_song(path)
        add_song_to_database(file, hashes)
        print(
            f"{file}  |  Peaks: {len(peaks)}  |  Hashes: {len(hashes)}"
        )

# Save database
with open("database.pkl", "wb") as f:
    pickle.dump(database, f)

print("\nDatabase saved successfully as database.pkl")
print("Total unique fingerprints:", len(database))


# In[ ]:




