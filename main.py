from datetime import datetime

from setup import setup_data
from data_maker import (
    wipe_schema,
    make_school_data,
    make_lea_data,
    make_database_views
)

from constants import OutputOption

input_directory = "./input/"
output_directory = "./output/"
output_type = OutputOption.ALL

start = datetime.utcnow()
print("\n\n\n============ BETTER CRDC ============")
print(f"\nStarting Program at {start}")

setup_data(input_directory)

wipe_schema()
make_school_data(input_directory, output_directory, output_type)
make_lea_data(input_directory, output_directory, output_type)

if(output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
    make_database_views(input_directory, output_directory)

print(f"Program Completed in {datetime.utcnow() - start}\n")
print("=====================================\n\n\n")
