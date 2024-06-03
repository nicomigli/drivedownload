from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os

# Step 1: Authenticate and create the PyDrive client
gauth = GoogleAuth()
gauth.LocalWebserverAuth()

drive = GoogleDrive(gauth)

# Function to ensure directory exists
def ensure_directory_exists(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)

# Function to clean and create valid file paths
def clean_path(path):
    return path.strip().replace('/', '_').replace('\\', '_')

# Function to download files, handling non-downloadable files
def download_files(file_list, download_path):
    for file in file_list:
        print(f'Processing {file["title"]}...')
        # Clean the file and folder names to avoid directory issues
        file_title = clean_path(file['title'])
        file_path = os.path.join(download_path, file_title)
        
        if file['mimeType'] == 'application/vnd.google-apps.document':
            file.GetContentFile(file_path + '.docx', mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        elif file['mimeType'] == 'application/vnd.google-apps.spreadsheet':
            file.GetContentFile(file_path + '.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        elif file['mimeType'] == 'application/vnd.google-apps.presentation':
            file.GetContentFile(file_path + '.pptx', mimetype='application/vnd.openxmlformats-officedocument.presentationml.presentation')
        elif file['mimeType'] == 'application/vnd.google-apps.folder':
            folder_path = os.path.join(download_path, file_title)
            ensure_directory_exists(folder_path)  # Ensure directory exists
            download_all_files(drive, file['id'], folder_path)
        else:
            try:
                ensure_directory_exists(os.path.dirname(file_path))  # Ensure directory exists for the file
                file.GetContentFile(file_path)
            except Exception as e:
                print(f'Error downloading {file["title"]}: {e}')

# Function to list and download all files
def download_all_files(drive, parent_id='root', download_path='.'):
    query = f"'{parent_id}' in parents and trashed=false"
    file_list = drive.ListFile({'q': query}).GetList()
    download_files(file_list, download_path)

# Specify your download path here
download_path = './downloads'
ensure_directory_exists(download_path)
download_all_files(drive, 'root', download_path)

print('Download completed!')
