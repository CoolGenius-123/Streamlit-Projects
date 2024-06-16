import os
import requests
import threading
import streamlit as st

# Define the downloads directory
downloads_dir = "downloads"
os.makedirs(downloads_dir, exist_ok=True)

def download_file(url, file_path, progress_callback):
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_size = 0
        
        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_size += len(data)
                progress_callback(progress_size, total_size_in_bytes)
        
        if total_size_in_bytes != 0 and progress_size != total_size_in_bytes:
            st.error(f"ERROR, something went wrong with {file_path}")
        else:
            st.success(f"File downloaded successfully as {file_path}")
    except Exception as e:
        st.error(f"An error occurred while downloading {file_path}: {e}")

def create_download_thread(url, file_name):
    file_path = os.path.join(downloads_dir, file_name)
    
    def progress_callback(progress_size, total_size_in_bytes):
        progress_percentage = (progress_size / total_size_in_bytes) * 100
        st.write(f"Downloading {file_name}: {progress_percentage:.2f}%")
    
    thread = threading.Thread(target=download_file, args=(url, file_path, progress_callback))
    thread.start()

def main():
    st.title("Simple Downloader")
    url = st.text_input("Enter the URL of the file you want to download")
    file_name = st.text_input("Enter the name of the file you want to save it as")

    if st.button("Download"):
        if url and file_name:
            create_download_thread(url, file_name)
        else:
            st.error("Please provide both the URL and the file name")

if __name__ == "__main__":
    main()
