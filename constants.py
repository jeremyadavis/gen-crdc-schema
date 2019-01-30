from enum import Enum


TABLE_PREFIX = "crdc1516_"

CRDC_DATA_URL = "https://www2.ed.gov/about/offices/list/ocr/docs/2015-16-crdc-data.zip"
# CRDC_DATA_URL = "https://codeload.github.com/fogleman/Minecraft/zip/master"

CRDC_DATA_FOLDER = "Data Files and Layouts/"

CRDC_FILES = [
    {
        "needed_file_name": "lea_layout.csv",
        "extracted_path": CRDC_DATA_FOLDER+"CRDC 2015-16 LEA Data Record Layout.csv"},
    {
        "needed_file_name": "lea_data.csv",
        "extracted_path": CRDC_DATA_FOLDER+"CRDC 2015-16 LEA Data.csv"},
    {
        "needed_file_name": "school_layout.csv",
        "extracted_path": CRDC_DATA_FOLDER+"CRDC 2015-16 School Data Record Layout.csv"},
    {
        "needed_file_name": "school_data.csv",
        "extracted_path": CRDC_DATA_FOLDER+"CRDC 2015-16 School Data.csv"}
]

DATABASE_URL = "postgresql://postgres:@localhost:5431/postgres"


class OutputOption(Enum):
    ALL = "ALL"
    CSV = "CSV"
    DATABASE = "DATABASE"
