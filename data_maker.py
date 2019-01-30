from datetime import datetime
from sqlalchemy import create_engine

from constants import (
    TABLE_PREFIX,
    DATABASE_URL,
    OutputOption
)

from helpers2 import (
    get_school_layout,
    get_school_data
)

from utils import (
    create_directory
)

SQLENGINE = create_engine(DATABASE_URL)

"""
  Import School Data
  Create mapping from layout's generated table name to columns within that table for lookup against data file
  Slice dataframe by column to make more normalized table/dataframe
  Output sliced dataframe to CSV or DATABASE
"""


def make_school_data(input_dir, output_dir, output_type=OutputOption.CSV):
    print("--- STEP 2: CREATE STUDENT DATA")

    data_output_dir = output_dir + "data/"
    scripts_output_dir = output_dir + "scripts/"

    print("    * Starting Data File Imports")
    start = datetime.utcnow()
    df_school_layout = get_school_layout(input_dir)
    df_school_data = get_school_data(input_dir, 1000)
    print(f"        School Layout Shape", df_school_layout.shape)
    print(f"        School Data Shape", df_school_data.shape)
    print(f"    * Imports Completed (took {datetime.utcnow() - start})")

    # ====== CREATE FILENAME to COLUMN MAPPINGS
    curr_table_name = ""
    csv_dict = {}

    for row in df_school_layout.itertuples():
        if(TABLE_PREFIX + row.table_name != curr_table_name):
            curr_table_name = TABLE_PREFIX + row.next_table_name
            csv_dict[curr_table_name] = []

        # ====== COMBOKEY is the dataframe index and will be exported there
        if row.column_name != "COMBOKEY":
            csv_dict[curr_table_name].append(row.column_name)

    # ====== OUTPUT DATA FOR EACH TABLENAME
    database_cleanup = ""
    for file_name, df_columns in csv_dict.items():
        df_filtered = df_school_data.loc[:, df_columns]

        # CSV OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
            create_directory(data_output_dir)
            df_filtered.to_csv(data_output_dir + file_name + ".csv")

        # DATABASE OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
            create_directory(scripts_output_dir)
            df_filtered.to_sql(file_name, SQLENGINE, if_exists="replace")
            database_cleanup += f"DROP TABLE IF EXISTS {file_name};\n\n"

    if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
        print(f"    * CSV Files Created In ", data_output_dir)

    if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
        print(f"    * Database Tables Created In ", DATABASE_URL)
        drop_tables_script = open(
            f"{scripts_output_dir}drop_school_tables.sql", 'w')
        drop_tables_script.write(database_cleanup)
        drop_tables_script.close()
        print(f"    * Database Cleanup In ", scripts_output_dir)
