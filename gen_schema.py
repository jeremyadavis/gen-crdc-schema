import os
from constants import TABLE_PREFIX
from helpers import (
    make_meaningful_name,
    get_school_layout_file,
    get_school_form_ddl_file,
    create_folder
)

# ====== INPUT FILES
df_layouts = get_school_layout_file()
df_ddl = get_school_form_ddl_file()

# ====== OUTPUT FILES
output_dir = './output/'
create_folder(output_dir)
# directory = os.path.dirname("output")

create_output_file = open(f"{output_dir}create_scripts.sql", 'w')
drop_output_file = open(f"{output_dir}drop_scripts.sql", 'w')

# ====== Make CREATE statements
num_table_columns = 0
tot_num_tables = 0
tot_num_columns = 0
curr_table_name = ""

table_view_cleanup = ""
table_statement = ""
view_statement = ""

for row in df_layouts.itertuples():
    # ====== Start Table/view Create
    if(TABLE_PREFIX + row.table_name != curr_table_name):
        curr_table_name = TABLE_PREFIX + row.next_table_name
        curr_view_name = row.next_table_name
        tot_num_tables += 1
        print(f"Creating Table {curr_table_name} ...")
        table_view_cleanup = f"DROP VIEW IF EXISTS {curr_view_name};\n"
        table_view_cleanup += f"DROP TABLE IF EXISTS {curr_table_name};\n\n"

        table_statement = (f"CREATE TABLE {curr_table_name} (\n")
        table_statement += "\tCOMBOKEY character varying(12)\n"
        view_statement = (f"CREATE VIEW {row.table_name} AS\n\tSELECT\n")
        view_statement += "\t\tCOMBOKEY AS COMBOKEY\n"

    # ====== Create column names
    if row.column_name != "COMBOKEY":
        table_statement += f"\t{row.column_name}"
        table_statement += f" {df_ddl.loc[row.column_name.lower(), 'type']}"
        table_statement += f" {df_ddl.loc[row.column_name.lower(), 'extra']}" if type(
            df_ddl.loc[row.column_name.lower(), 'extra']) is str else ""
        # common or no comma depending of if last column or not
        table_statement += ",\n" if row.table_name == row.next_table_name else "\n"

        # ====== Create View Field Names
        view_field = make_meaningful_name(row.column_name, row.module)
        view_statement += f"\t\t{row.column_name} AS {view_field}\n"

        num_table_columns += 1
        tot_num_columns += 1

    # ====== Finish table/view create
    if(row.table_name != row.next_table_name):
        drop_output_file.write(table_view_cleanup)
        create_output_file.write(table_view_cleanup)
        create_output_file.write(table_statement + ');\n\n')
        create_output_file.write(view_statement)
        create_output_file.write(f"\tFROM\n\t\t{curr_table_name};\n\n")
        print(num_table_columns, "columns created")
        print("Done\n")
        num_table_columns = 0

print("GENERATION COMPLETE")
print(f" {tot_num_tables} tables created")
print(f" {tot_num_columns} columns created")
create_output_file.close()
drop_output_file.close()
