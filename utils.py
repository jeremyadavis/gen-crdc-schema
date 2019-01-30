import os
import requests
import re
import zipfile
import datetime


def create_directory(directory):
    try:
        if not os.path.isdir(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)


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


def unzip_filepath(directory, filename):
    with zipfile.ZipFile(directory + filename, 'r') as zip:
        # printing all the contents of the zip file
        zip.printdir()

        # extracting all the files
        # print('Extracting all the files now...')
        zip.extractall(path=directory)
        # print('Done!')
