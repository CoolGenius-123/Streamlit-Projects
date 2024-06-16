import os
import streamlit as st
import requests
import threading

# Define the downloads directory
downloads_dir = "downloads"
os.makedirs(downloads_dir, exist_ok=True)

# Initialize session state for thread tracking
if 'threads' not in st.session_state:
    st.session_state['threads'] = {}
if 'downloads' not in st.session_state:
    st.session_state['downloads'] = []

def download_file(url, file_path):
    try:
        response = requests.get(url, stream=True)
        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024  # 1 Kibibyte
        progress_size = 0

        with open(file_path, 'wb') as file:
            for data in response.iter_content(block_size):
                file.write(data)
                progress_size += len(data)
                st.session_state['current_progress'] = (progress_size / total_size_in_bytes) * 100

        if total_size_in_bytes != 0 and progress_size != total_size_in_bytes:
            st.session_state['downloads'].append((file_path, "ERROR, something went wrong"))
        else:
            st.session_state['downloads'].append((file_path, "File downloaded successfully"))
    except Exception as e:
        st.session_state['downloads'].append((file_path, f"An error occurred: {e}"))

def main():
    st.title("Downloader")
    url = st.text_input("Enter the URL of the file you want to download")
    file_name = st.text_input("Enter the name of the file you want to save it as")

    if st.button("Download"):
        if url and file_name:
            file_path = os.path.join(downloads_dir, file_name.strip())
            thread = threading.Thread(target=download_file, args=(url.strip(), file_path))
            thread.start()
            st.session_state['threads'][file_name.strip()] = thread

    for file_path, status in st.session_state['downloads']:
        st.write(f"{file_path}: {status}")
        if st.button(f"Delete {os.path.basename(file_path)}"):
            os.remove(file_path)
            st.session_state['downloads'] = [(path, stat) for path, stat in st.session_state['downloads'] if path != file_path]
            st.success(f"Deleted {os.path.basename(file_path)}")

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                st.download_button(
                    label=f"Download {os.path.basename(file_path)}",
                    data=file,
                    file_name=os.path.basename(file_path),
                    mime='application/octet-stream'
                )

if __name__ == "__main__":
    main()
