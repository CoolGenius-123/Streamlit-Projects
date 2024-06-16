import os
import shutil
import streamlit as st
import requests

def main():
    st.title("Downloader")
    url = st.text_input("Enter the URL of the file you want to download")
    file_name = st.text_input("Enter the name of the file you want to save it as")

    # Define the downloads directory
    downloads_dir = "downloads"
    file_path = os.path.join(downloads_dir, file_name)

    if st.button("Download"):
        try:
            # Delete the directory and its contents if it exists
            if os.path.exists(downloads_dir):
                shutil.rmtree(downloads_dir)

            # Create the directory
            os.makedirs(downloads_dir, exist_ok=True)

            response = requests.get(url, stream=True)
            total_size_in_bytes= int(response.headers.get('content-length', 0))
            block_size = 1024 #1 Kibibyte
            progress_bar = st.progress(0)
            progress_size = 0
            download_text = st.empty()
            with open(file_path, 'wb') as file:
                for data in response.iter_content(block_size):
                    file.write(data)
                    progress_size += len(data)
                    progress_percentage = (progress_size / total_size_in_bytes) * 100
                    progress_bar.progress(progress_percentage / 100)
                    download_text.text(f"Downloaded: {progress_size}/{total_size_in_bytes} bytes ({progress_percentage}%)")
            if total_size_in_bytes != 0 and progress_size != total_size_in_bytes:
                st.error("ERROR, something went wrong")
            else:
                st.success(f"File downloaded successfully as {file_name} in the {downloads_dir} directory")
        except Exception as e:
            st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
