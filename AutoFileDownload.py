import paramiko
import os
import time
from dotenv import load_dotenv

load_dotenv()

hostname = 'download.mosdac.gov.in'
username = os.getenv('MOSDAC_SFTP_USERNAME')
password = os.getenv('MOSDAC_SFTP_PASSWORD')
remote_dir = '/Order'
local_dir = './data'

os.makedirs(local_dir, exist_ok=True)

transport = paramiko.Transport((hostname, 22))
transport.connect(username=username, password=password)
sftp = paramiko.SFTPClient.from_transport(transport)

for folder in sftp.listdir_attr(remote_dir):
    start = time.time()
    folder_remote_path = f"{remote_dir}/{folder.filename}"
    for file in sftp.listdir_attr(folder_remote_path):
        file_remote_path = f"{folder_remote_path}/{file.filename}"
        file_local_path = os.path.join(local_dir, file.filename)
        print(f"Downloading {file_remote_path} ...")
        sftp.get(file_remote_path, file_local_path)
    end = time.time()
    print('\n' + str(folder) + ':' + str(end - start))


sftp.close()
transport.close()

print("Download complete.")