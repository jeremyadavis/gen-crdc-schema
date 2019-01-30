from datetime import datetime

from setup import setup_data
from data_maker import make_school_data

from constants import OutputOption

input_directory = "./input/"
output_directory = "./output/"

start = datetime.utcnow()
print("\n\n\n============ BETTER CRDC ============")
print(f"\nStarting Program at {start}")

setup_data(input_directory)

make_school_data(input_directory, output_directory, OutputOption.ALL)