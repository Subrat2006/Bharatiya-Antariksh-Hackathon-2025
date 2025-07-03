import paramiko
import os
import time
from dotenv import load_dotenv

load_dotenv()

def download_latest_file():
    hostname = 'download.mosdac.gov.in'
    username = os.getenv('MOSDAC_SFTP_USERNAME')
    password = os.getenv('MOSDAC_SFTP_PASSWORD')
    remote_dir = '/Order'
    local_dir = './data'

    os.makedirs(local_dir, exist_ok=True)

    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    start = time.time()

    folders = sorted(
        [f for f in sftp.listdir_attr(remote_dir) if not f.filename.startswith('.')], 
        key=lambda f: f.st_mtime,
        reverse=True
    )

    latest_folder = folders[0]
    latest_folder_remote_path = f"{remote_dir}/{latest_folder.filename}"

    files = sorted(
        [f for f in sftp.listdir_attr(latest_folder_remote_path) if not f.filename.startswith('.')], 
        key=lambda f: f.st_mtime,
        reverse=True
    )

    file = files[0]
    file_remote_path = f"{latest_folder_remote_path}/{file.filename}"
    file_local_path = os.path.join(local_dir, file.filename)
    print(f"Downloading {file_remote_path} ...")
    if os.path.exists(file_local_path):
        print("File already exists\n")
    else:
        sftp.get(file_remote_path, file_local_path)
        end = time.time()
        print(str(latest_folder.filename) + ' -> ' + str(file.filename) + ' : ' + str(end - start) + ' sec download time\n')

    sftp.close()
    transport.close() 
    print("Download complete.\n")
    return file.filename

def download_all_files():
    hostname = 'download.mosdac.gov.in'
    username = os.getenv('MOSDAC_SFTP_USERNAME')
    password = os.getenv('MOSDAC_SFTP_PASSWORD')
    remote_dir = '/Order'
    local_dir = './data'

    os.makedirs(local_dir, exist_ok=True)

    transport = paramiko.Transport((hostname, 22))
    transport.connect(username=username, password=password)
    sftp = paramiko.SFTPClient.from_transport(transport)

    folders = sorted(
        [f for f in sftp.listdir_attr(remote_dir) if not f.filename.startswith('.')], 
        key=lambda f: f.st_mtime,
        reverse=True
    )

    for folder in folders:
        start = time.time()
        folder_remote_path = f"{remote_dir}/{folder.filename}"

        files = sorted(
            [f for f in sftp.listdir_attr(folder_remote_path) if not f.filename.startswith('.')], 
            key=lambda f: f.st_mtime,
            reverse=True
        )

        for file in files:
            file_remote_path = f"{folder_remote_path}/{file.filename}"
            file_local_path = os.path.join(local_dir, file.filename)
            print(f"Downloading {file_remote_path} ...")
            sftp.get(file_remote_path, file_local_path)
            end = time.time()
            print(str(folder.filename) + ' -> ' + str(file.filename) + ' : ' + str(end - start) + ' sec download time\n')
            start = end

    sftp.close()
    transport.close()

    print("Download complete.\n")