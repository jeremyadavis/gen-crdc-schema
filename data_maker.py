from utils import (
    create_directory
)
from column_translator import make_meaningful_name, make_meaningful_lea_name
from helpers import (
    get_school_layout,
    get_school_data,
    get_lea_layout,
    get_lea_data,
    get_schema
)
from constants import (
    TABLE_PREFIX,
    DATABASE_URL,
    OutputOption
)
import sys
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.sql import text


def connect_to_db():
    try:
        engine = create_engine(DATABASE_URL)
        engine.connect()

        return engine
    # except DatabaseError as db_err:
    #     print("DB ERR", db_err)
    except Exception as e:
        print("ERROR! Unable to Connect to database with", DATABASE_URL)
        print(e)
        return False


"""
with engine.connect() as conn, conn.begin():
"""

SQLENGINE = connect_to_db()

"""
  Import School Data
  Create mapping from layout's generated table name to columns within that table for lookup against data file
  Slice dataframe by column to make more normalized table/dataframe
  Output sliced dataframe to CSV or DATABASE
"""


def make_school_data(input_dir, output_dir, output_type=OutputOption.CSV):
    print("--- STEP 2: CREATE SCHOOL DATA")

    data_output_dir = output_dir + "data/"
    scripts_output_dir = output_dir + "scripts/"
    school_table_prefix = TABLE_PREFIX + "school_"

    print("    * Starting Data File Imports")
    start = datetime.utcnow()
    df_school_layout = get_school_layout(input_dir)
    df_school_data = get_school_data(input_dir, 1000)
    print(f"        School Layout Shape", df_school_layout.shape)
    print(f"        School Data Shape", df_school_data.shape)
    print(f"    * Imports Completed (took {datetime.utcnow() - start})")

    # ====== CREATE FILENAME to COLUMN MAPPINGS
    curr_table_name = ""
    table_row_map = {}

    for row in df_school_layout.itertuples():
        if(school_table_prefix + row.table_name != curr_table_name):
            curr_table_name = school_table_prefix + row.next_table_name
            table_row_map[curr_table_name] = []

        # ====== COMBOKEY is the dataframe index and will be exported there
        if row.column_name != "combokey":
            table_row_map[curr_table_name].append(row.column_name)

    # ====== OUTPUT DATA FOR EACH TABLENAME
    print(f"    * Starting Data Output")
    database_cleanup = ""
    create_statements = ""
    num_tables = 0
    for file_name, df_columns in table_row_map.items():
        print(f"        Making {file_name}")
        num_tables += 1
        df_filtered = df_school_data.loc[:, df_columns]

        # CSV OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
            create_directory(data_output_dir)
            df_filtered.to_csv(data_output_dir + file_name + ".csv")

        # DATABASE OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
            create_directory(scripts_output_dir)
            if(SQLENGINE):
                drop_view(file_name, SQLENGINE)
                df_filtered.to_sql(file_name, SQLENGINE,
                                   if_exists="replace", method="multi")
            else:
                print(f"         !!!Unable to write to database!!!")
            database_cleanup += f"DROP TABLE IF EXISTS \"{file_name}\";\n\n"
            create_statements += f"{get_schema(df_filtered, file_name, SQLENGINE)}"

    print(f"        {num_tables} exports processed")
    if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
        print(f"    * School CSV Files Created In ", data_output_dir)

    if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
        if(SQLENGINE):
            print(f"    * School Database Tables Created In ", DATABASE_URL)
        create_tables_script = open(
            f"{scripts_output_dir}create_school_tables.sql", 'w')
        create_tables_script.write(create_statements)
        create_tables_script.close()
        drop_tables_script = open(
            f"{scripts_output_dir}drop_school_tables.sql", 'w')
        drop_tables_script.write(database_cleanup)
        drop_tables_script.close()
        print(f"    * Database Cleanup In ", scripts_output_dir)

    print(f"    * School Data Complete ")


def make_lea_data(input_dir, output_dir, output_type=OutputOption.CSV):
    print("--- STEP 3: CREATE LEA DATA")

    data_output_dir = output_dir + "data/"
    scripts_output_dir = output_dir + "scripts/"
    lea_table_prefix = TABLE_PREFIX + "lea_"

    print("    * Starting Data File Imports")
    start = datetime.utcnow()
    df_lea_layout = get_lea_layout(input_dir)
    df_lea_data = get_lea_data(input_dir, 1000)
    print(f"        LEA Layout Shape", df_lea_layout.shape)
    print(f"        LEA Data Shape", df_lea_data.shape)
    print(f"    * Imports Completed (took {datetime.utcnow() - start})")

    # # ====== CREATE FILENAME to COLUMN MAPPINGS
    curr_table_name = ""
    table_row_map = {}

    for row in df_lea_layout.itertuples():
        if(lea_table_prefix + row.table_name != curr_table_name):
            curr_table_name = lea_table_prefix + row.next_table_name
            table_row_map[curr_table_name] = []

        # ====== LEAID is the dataframe index and will be exported there
        if row.column_name != "leaid":
            table_row_map[curr_table_name].append(row.column_name)

    # ====== OUTPUT DATA FOR EACH TABLENAME
    print(f"    * Starting Data Output")
    database_cleanup = ""
    create_statements = ""
    num_tables = 0
    for file_name, df_columns in table_row_map.items():
        print(f"        Making {file_name}")
        num_tables += 1
        df_filtered = df_lea_data.loc[:, df_columns]

        # CSV OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
            create_directory(data_output_dir)
            df_filtered.to_csv(data_output_dir + file_name + ".csv")

        # DATABASE OUTPUT
        if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
            create_directory(scripts_output_dir)
            if(SQLENGINE):
                df_filtered.to_sql(file_name, SQLENGINE,
                                   if_exists="replace",
                                   method="multi")
            else:
                print(f"         !!!Unable to write to database!!!")
            create_statements += f"{get_schema(df_filtered, file_name, SQLENGINE)}"
            database_cleanup += f"DROP TABLE IF EXISTS \"{file_name}\";\n\n"

    print(f"        {num_tables} exports processed")
    if (output_type == OutputOption.ALL or output_type == OutputOption.CSV):
        print(f"    * LEA CSV Files Created In ", data_output_dir)

    if (output_type == OutputOption.ALL or output_type == OutputOption.DATABASE):
        if(SQLENGINE):
            print(f"    * LEA Database Tables Created In ", DATABASE_URL)
        create_tables_script = open(
            f"{scripts_output_dir}create_lea_tables.sql", 'w')
        create_tables_script.write(create_statements)
        create_tables_script.close()
        drop_tables_script = open(
            f"{scripts_output_dir}drop_lea_tables.sql", 'w')
        drop_tables_script.write(database_cleanup)
        drop_tables_script.close()
        print(f"    * LEA Database Cleanup In ", scripts_output_dir)

    print(f"    * LEA Data Complete ")


def make_database_views(input_dir, output_dir):
    print("--- STEP 3: CREATE DATABASE VIEWS")

    scripts_output_dir = output_dir + "scripts/"
    create_directory(scripts_output_dir)

    make_lea_views(input_dir, scripts_output_dir)
    make_schools_views(input_dir, scripts_output_dir)

    print(f"    * Database Views Complete ")


def make_lea_views(input_dir, scripts_output_dir):
    lea_table_prefix = TABLE_PREFIX + "lea_"

    drop_views_script = open(
        f"{scripts_output_dir}drop_lea_views.sql", 'w')
    create_views_script = open(
        f"{scripts_output_dir}create_lea_views.sql", 'w')

    print("    * Starting Data File Imports")
    start = datetime.utcnow()
    df_lea_layout = get_lea_layout(input_dir)
    print(f"        Lea Layout Shape", df_lea_layout.shape)
    print(f"    * Imports Completed (took {datetime.utcnow() - start})")

    print("    * Creating View Scripts")
    tot_num_views = 0
    num_fields = 1
    curr_table_name = ""
    curr_view_name = ""
    view_statement = ""
    database_cleanup = ""
    for row in df_lea_layout.itertuples():
        # ====== Start View Create
        if(lea_table_prefix + row.table_name != curr_table_name):
            curr_table_name = lea_table_prefix + row.next_table_name
            curr_view_name = row.next_table_name
            tot_num_views += 1
            print(f"        ", curr_view_name, end=" ")

            database_cleanup = f"DROP VIEW IF EXISTS \"{curr_view_name}\";\n"

            view_statement = (
                f"CREATE VIEW \"{row.table_name}\" AS\n\tSELECT\n")
            view_statement += "\t\tleaid AS leaid,\n"

        # ====== Create column names
        if row.column_name != "leaid":
            # ====== Create View Field Names
            view_field = make_meaningful_lea_name(row.column_name, row.module)
            # view_field = row.column_name
            view_statement += f"\t\t{row.column_name} AS {view_field}"
            view_statement += ",\n" if row.table_name == row.next_table_name else "\n"
            num_fields += 1

        # ====== Finish table/view create
        if(row.table_name != row.next_table_name):
            print(f"({num_fields} cols)")  # writes to end of previous print
            drop_views_script.write(database_cleanup)
            create_views_script.write(database_cleanup)

            view_statement = view_statement + \
                f"\tFROM\n\t\t\"{curr_table_name}\";\n\n"
            create_views_script.write(view_statement)
            add_view_to_database(database_cleanup, view_statement)

            num_fields = 0

    drop_views_script.close()
    create_views_script.close()


def make_schools_views(input_dir, scripts_output_dir):
    school_table_prefix = TABLE_PREFIX + "school_"

    drop_views_script = open(
        f"{scripts_output_dir}drop_school_views.sql", 'w')
    create_views_script = open(
        f"{scripts_output_dir}create_school_views.sql", 'w')

    print("    * Starting Data File Imports")
    start = datetime.utcnow()
    df_school_layout = get_school_layout(input_dir)
    print(f"        School Layout Shape", df_school_layout.shape)
    print(f"    * Imports Completed (took {datetime.utcnow() - start})")

    print("    * Creating View Scripts")
    tot_num_views = 0
    num_fields = 1
    curr_table_name = ""
    curr_view_name = ""
    view_statement = ""
    database_cleanup = ""
    for row in df_school_layout.itertuples():
        # ====== Start View Create
        if(school_table_prefix + row.table_name != curr_table_name):
            curr_table_name = school_table_prefix + row.next_table_name
            curr_view_name = row.next_table_name
            tot_num_views += 1
            print(f"        ", curr_view_name, end=" ")

            database_cleanup = f"DROP VIEW IF EXISTS \"{curr_view_name}\";\n"

            view_statement = (f"CREATE VIEW {row.table_name} AS\n\tSELECT\n")
            view_statement += "\t\tcombokey AS combokey,\n"

        # ====== Create column names
        if row.column_name != "combokey":
            # ====== Create View Field Names
            view_field = make_meaningful_name(row.column_name, row.module)
            view_statement += f"\t\t{row.column_name} AS {view_field}"
            view_statement += ",\n" if row.table_name == row.next_table_name else "\n"
            num_fields += 1

        # ====== Finish table/view create
        if(row.table_name != row.next_table_name):
            print(f"({num_fields} cols)")  # writes to end of previous print
            drop_views_script.write(database_cleanup)
            create_views_script.write(database_cleanup)

            view_statement = view_statement + \
                f"\tFROM\n\t\t{curr_table_name};\n\n"
            create_views_script.write(view_statement)
            add_view_to_database(database_cleanup, view_statement)

            num_fields = 0

    drop_views_script.close()
    create_views_script.close()


def wipe_schema():
    if(SQLENGINE):
        with SQLENGINE.connect() as conn:
            conn.execute(text('DROP SCHEMA public CASCADE;'))
            conn.execute(text('CREATE SCHEMA public;'))


def add_view_to_database(cleanup, create):
    if(SQLENGINE):
        with SQLENGINE.connect() as conn:
            conn.execute(text(cleanup))
            conn.execute(text(create))


def drop_view(name, engine):
    with SQLENGINE.connect() as conn:
        conn.execute(text(f"DROP VIEW IF EXISTS \"{name}\";\n"))
