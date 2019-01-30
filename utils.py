import os
import requests
import re
import zipfile
import datetime
import shutil


def create_directory(directory):
    try:
        if not os.path.isdir(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


def remove_directory(directory):
    try:
        if os.path.isdir(directory):
            shutil.rmtree(directory)
    except OSError:
        print('Error: Removing directory. ' + directory)


def fetch_file(url, directory, filename=None):
    r = requests.get(url)
    print(r)
    """
    SET FILENAME TO DOWNLOADED FILE NAME
    """
    # print('-> ', hasattr(r.headers, 'content-disposition'))
    if not (filename):
        if(hasattr(r.headers, 'content-disposition')):
            d = r.headers['content-disposition']
            filename = re.findall(
                "filename=(.+)", d)[0]
        else:
            filename = f"extract_file_{datetime.datetime.now().replace(microsecond=0).isoformat()}.zip"

    file_path = directory + filename
    with open(f"{file_path}", "wb") as code:
        code.write(r.content)

        return filename


def get_filename_from_url(url, type=".zip"):
    fn = url.split('/')
    fn.reverse()
    return fn[0] if fn[0].endswith(type) else None


def unzip(from_path, to_dir="."):
    with zipfile.ZipFile(from_path, 'r') as zip:
        zip.printdir()

        zip.extractall(path=to_dir)


def rename_files(files_list, src_dir, dest_dir):
    # print("rename_files", files_list, src_dir, dest_dir)
    for i, file in enumerate(files_list):
        src = src_dir+file['src_path']
        dest = dest_dir+file['dest_path']

        print('src/dst', src, dest)
        if os.path.exists(src):
            os.rename(src, dest)
