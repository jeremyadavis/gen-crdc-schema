import os
from utils import (
    create_directory,
    fetch_file,
    get_filename_from_url,
    unzip_filepath
)
from constants import CRDC_DATA_URL


def setup_data(input_directory="./input/"):
    print("--- STEP 1: SETUP DATA")
    extract_dir = f"{input_directory}extracts/"

    # create_directory(input_directory)
    create_directory(extract_dir)

    needed_files = {
        "lea_layout": "CRDC 2015-16 LEA Data Record Layout.csv",
        "lea_data": "CRDC 2015-16 LEA Data.csv",
        "school_layout": "CRDC 2015-16 School Data Record Layout.csv",
        "school_data": "CRDC 2015-16 School Data.csv"
    }
    curr_files = os.listdir(input_directory)

    # print(curr_files)
    """
    See if needed files currently exist in input directory.
    If not, retrieve and extract accordingly
    """
    needed_files_exists = set(list(needed_files.keys())).issubset(curr_files)
    if not(needed_files_exists):

        # if not(zip_file_name and os.path.isfile(zip_file_name)):
        print('    * Fetching CRDC Data From Public Website')

        zip_file_name = get_filename_from_url(CRDC_DATA_URL)
        zip_file_name = fetch_file(CRDC_DATA_URL, extract_dir, zip_file_name)

        print('    * Extracting Zip At ', extract_dir + zip_file_name)
        unzip_filepath(extract_dir, zip_file_name)

        print('    * Moving Files In Place ')
        # copy_and_rename(files=[current, new], current_path, new_path)

    print('    * Needed Files Are In Place')
