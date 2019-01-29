from constants import TABLE_PREFIX
from helpers import (
    get_school_layout_file,
    create_folder,
    get_school_data_file
)
from datetime import datetime

start = datetime.utcnow()
print(f"Starting at {start}")

# ====== INPUT FILES
df_layouts = get_school_layout_file()
df_data = get_school_data_file()
print(f"Import took {datetime.utcnow() - start}")

# ====== OUTPUT FILES
output_dir = './output/schema_data/'
create_folder(output_dir)

# ====== CREATE FILENAME to COLUMN MAPPINGS
curr_table_name = ""
csv_dict = {}

for row in df_layouts.loc[:].itertuples():
    if(TABLE_PREFIX + row.table_name != curr_table_name):
        curr_table_name = TABLE_PREFIX + row.next_table_name
        csv_dict[curr_table_name] = []

    if row.column_name != "COMBOKEY":
        csv_dict[curr_table_name].append(row.column_name)

# ====== CREATE CSV FILES FOR EACH TABLENAME
for file_name, df_columns in csv_dict.items():
    # print(key, df_columns, '\n')
    test_df = df_data.loc[:, df_columns]
    test_df.to_csv(f"{output_dir}{file_name}.csv")
print(f"Process took {datetime.utcnow() - start}")
