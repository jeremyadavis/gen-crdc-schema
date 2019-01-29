from constants import TABLE_PREFIX
from helpers import make_meaningful_name, module_to_table_name, get_school_layout_file, get_school_form_ddl_file, create_output_directory

# ====== INPUT FILES
df_layouts = get_school_layout_file()
df_ddl = get_school_form_ddl_file()  # ====== OUTPUT FILES

create_output_directory()


# ====== Make CREATE statements
num_table_columns = 0
tot_num_tables = 0
tot_num_columns = 0
curr_table_name = ""


table_view_cleanup = ""
table_statement = ""
view_statement = ""

# print(df_layouts.loc[0:5])

for row in df_layouts.loc[:].itertuples():
    # --- Start Table Create
    if(TABLE_PREFIX + row.table_name != curr_table_name):
        curr_table_name = TABLE_PREFIX + row.next_table_name
        curr_view_name = row.next_table_name
        tot_num_tables += 1
        print(f"Creating Table {curr_table_name} ...")
        table_view_cleanup = f"DROP VIEW IF EXISTS {curr_view_name};\n"
        table_view_cleanup += f"DROP TABLE IF EXISTS {curr_table_name};\n\n"

        table_statement = (f"CREATE TABLE {curr_table_name} (\n")
        view_statement = (f"CREATE VIEW {row.table_name} AS\n\tSELECT\n")

    # --- Create column names
    isLastColumn = row.table_name == row.next_table_name
    table_statement += f"\t{row.column_name}"
    table_statement += f" {df_ddl.loc[row.column_name.lower(), 'type']}"
    table_statement += f" {df_ddl.loc[row.column_name.lower(), 'extra']}" if type(
        df_ddl.loc[row.column_name.lower(), 'extra']) is str else ""
    table_statement += ",\n" if isLastColumn else "\n"

    view_field = make_meaningful_name(row.column_name, row.module)
    view_statement += f"\t\t{row.column_name} AS {view_field}\n"

    num_table_columns += 1
    tot_num_columns += 1

    # --- Finish table create
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
