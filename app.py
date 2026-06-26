#!/usr/bin/env python
# coding: utf-8

# In[2]:


import streamlit as st
import tempfile
import pickle
import pandas as pd
import tempfile
import os

from utils import (
    load_song,
    create_spectrogram,
    find_peaks,
    plot_spectrogram,
    plot_constellation,
    generate_hashes,
    match_query,
    plot_offset_histogram,
    database
)


st.set_page_config(
    page_title="Song Recognizer",
    page_icon="🎵",
    layout="wide"
)
try:
    with open("database.pkl", "rb") as f:
        database.clear()
        database.update(pickle.load(f))
except:
    st.error("database.pkl not found. Run database_builder.py first.")
    st.stop()

st.title("🎵 Song Recognizer by Audio Fingerprinting")
st.markdown("### Indian Institute of Technology Kanpur")
st.markdown("**Course:** Signals and Systems")
st.markdown("**Project:**  Audio Fingerprinting")
st.markdown("**Name:** Swayam Nirlipta")
st.markdown("**Roll No.:** 251109")
st.write("Upload an MP3 song to view its spectrogram and constellation map.")

uploaded_file = st.file_uploader(
    "Upload an MP3 File",
    type=["mp3"]
)

if uploaded_file is not None:
    st.success("File Uploaded Successfully!")
    st.audio(uploaded_file)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tmp.write(uploaded_file.read())
        temp_path = tmp.name

    with st.spinner("Processing Audio..."):

        y, sr = load_song(temp_path)

        S = create_spectrogram(y)

        peaks = find_peaks(S)
        query_hashes = generate_hashes(peaks)
        offset_votes = match_query(query_hashes)
        if len(offset_votes) == 0:
            st.error("No matching song found.")
            detected_song= "Song is not in my storage"
        else:
            song_scores = {}
            for (song, offset), votes in offset_votes.items():
                if song not in song_scores:
                    song_scores[song] = 0
                    song_scores[song] += votes
            detected_song = max(song_scores, key=song_scores.get)
    st.markdown(
    f"<h1 style='color:green;'>🎵 Recognized Song: {detected_song}</h1>",
    unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["📊Spectrogram","✨Constellation Map", "📈Offset Histogram"])


    with tab1:
        fig1 = plot_spectrogram(S)
        st.pyplot(fig1)
    with tab2:
        fig2 = plot_constellation(peaks)
        st.pyplot(fig2)
    with tab3:
        fig3 = plot_offset_histogram( offset_votes, detected_song)
        st.pyplot(fig3)

    st.write("Total Peaks :", len(peaks))
    st.write("Total Fingerprints :", len(query_hashes))
st.divider()

st.header("Batch Mode")
batch_files = st.file_uploader(
    "Upload Multiple MP3 Files",
    type=["mp3"],
    accept_multiple_files=True
)

if batch_files:
    results = []
    progress = st.progress(0)
    plot_data = {}

    for i, uploaded_file in enumerate(batch_files):
        with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".mp3"
        ) as tmp:
            tmp.write(uploaded_file.read())
            temp_path = tmp.name
        y, sr = load_song(temp_path)
        S = create_spectrogram(y)
        peaks = find_peaks(S)
        query_hashes = generate_hashes(peaks)
        offset_votes = match_query(query_hashes)
        if len(offset_votes) == 0:
            detected_song = "No Match"
        else:
            song_scores = {}
            for (song, offset), votes in offset_votes.items():
                if song not in song_scores:
                    song_scores[song] = 0
                song_scores[song] += votes
            detected_song = max(
                song_scores,
                key=song_scores.get
            )

        results.append({
            "Query File": uploaded_file.name,
            "Recognized Song": detected_song,
            "Peaks": len(peaks),
            "Fingerprints": len(query_hashes)
        })
        plot_data[uploaded_file.name] = {
            "S": S,
            "peaks": peaks,
            "offset_votes": offset_votes,
            "detected_song": detected_song
        }
        progress.progress((i + 1) / len(batch_files))
        os.remove(temp_path)
    st.success("Batch Processing Completed")
    df = pd.DataFrame(results)
    st.dataframe(df)
    selected_file = st.selectbox(
    "Select a Query File",
    list(plot_data.keys())
    )
    tab1, tab2, tab3 = st.tabs([
    "Spectrogram",
    "Constellation Map",
    "Offset Histogram"
    ])

    with tab1:
        st.pyplot( plot_spectrogram(plot_data[selected_file]["S"]) )

    with tab2:
        st.pyplot( plot_constellation( plot_data[selected_file]["peaks"]  ) )

    with tab3:
        st.pyplot( plot_offset_histogram( plot_data[selected_file]["offset_votes"],plot_data[selected_file]["detected_song"]))
    csv = df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "Download Results CSV",
        csv,
        "results.csv",
        "text/csv"
    )
  

