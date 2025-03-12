import os
import streamlit as st
from torrentool.api import Torrent
import subprocess

# Path to aria2c executable
ARIA2C_PATH = r"C:\Users\yepuri manish\Downloads\aria2-1.37.0-win-64bit-build1\aria2-1.37.0-win-64bit-build1\aria2c.exe"
# Directory where downloads will be saved
DOWNLOAD_DIR = r"C:\temp"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

st.title("Torrent File Downloader")

# File uploader for torrent files
uploaded_file = st.file_uploader("Upload Torrent File (.torrent)", type=["torrent"])

if uploaded_file:
    # Save uploaded file to temp folder
    save_path = os.path.abspath(os.path.join("temp", uploaded_file.name))
    os.makedirs("temp", exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    st.success(f"Uploaded: {uploaded_file.name}")
    
    if st.button("Start Download"):
        try:
            # Read torrent file details
            torrent = Torrent.from_file(save_path)
            st.write(f"**Name:** {torrent.name}")
            st.write(f"**Size:** {torrent.total_size / (1024 * 1024):.2f} MB")

            # Display files included in torrent
            files = [f"{file.name} ({file.length / (1024 * 1024):.2f} MB)" for file in torrent.files]
            st.write("**Files:**")
            for file in files:
                st.write(f"- {file}")

            # Display trackers
            trackers = [tracker[0] for tracker in torrent.announce_urls]
            st.write(f"**Trackers:** {', '.join(trackers)}")

            # Start aria2c download
            st.info("Starting download...")

            # Escape the path using quotes and escape characters
            cmd = f'"{ARIA2C_PATH}" --dir "{DOWNLOAD_DIR}" --allow-overwrite=true --continue=true --disable-ipv6 "{save_path}"'
            st.write(f"**Running:** {cmd}")

            # Run the command using shell=True
            result = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                shell=True  # Let shell handle quotes and escape characters
            )

            # Display the output
            st.write(f"**stdout:**\n{result.stdout}")
            st.write(f"**stderr:**\n{result.stderr}")

            if result.returncode == 0:
                st.success("Download complete!")
            else:
                st.error(f"Failed to download:\n{result.stderr}")

        except Exception as e:
            st.error(f"Error: {e}")

    # Clean up the torrent file after use
    if os.path.exists(save_path):
        os.remove(save_path)
