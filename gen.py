import pandas
from helpers import make_meaningful_name, module_to_table_name

df_layouts = pandas.read_csv('data/school_layout.csv',
                             encoding='LATIN-1',
                             #  escapechar='\\',
                             #  index_col='column_name',
                             header=0,
                             names=['order', 'excel_column',
                                    'column_name', 'description', 'module']
                             )

df_ddl = pandas.read_csv('data/schoolform_ddl.txt',
                         delimiter="|",
                         index_col='column_name',
                         names=['column_name', 'type', 'extra']
                         )

output = open('create_scripts.sql', 'w')

# print(df_ddl.head())
# col = 'LEA_STATE'
# print(df_ddl.loc[col.lower(), 'type'])

# ------- HELPERS
# print(df_layouts.head())
# print(df_layouts['column_name'][0])
# print(type(df_layouts['column_name'][0]))
# print(df_layouts.head(20))
# print(df_layouts.describe()) #stats
# print(df_layouts.T) #transpose
# print(df_layouts.sort_values(by='module', ascending=False).head(20))
# print(df_layouts[1800:1825])
# for index, row in df_layouts.iterrows():
#     print(row['column_name'] + ' - ' + row['module'])
# print(getattr(row, "column_name"), getattr(row, "module"))
# modules = df.drop_duplicates(['module'])['module']

# ------- Tableify a table name from the module
df_layouts['table_name'] = df_layouts['module'].map(
    lambda m: module_to_table_name(m))
# Put the next rows table name with current row
df_layouts['next_table_name'] = df_layouts['table_name'].shift(-1)
# ------- print(df_layouts[['module', 'table_name', 'next_table_name']].head(20))

# ------- Make CREATE statements
num_table_columns = 0
tot_num_tables = 0
tot_num_columns = 0
curr_table_name = ""
table_prefix = "crdc1516_"

table_view_cleanup = ""
table_statement = ""
view_statement = ""

# print(df_layouts.loc[0:5])

for row in df_layouts.loc[:].itertuples():
    # --- Start Table Create
    if(table_prefix + row.table_name != curr_table_name):
        curr_table_name = table_prefix + row.next_table_name
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
        output.write(table_view_cleanup)
        output.write(table_statement + ');\n\n')
        output.write(view_statement)
        output.write(f"\tFROM\n\t\t{curr_table_name};\n\n")
        print(num_table_columns, "columns created")
        print("Done\n")
        num_table_columns = 0

print("GENERATION COMPLETE")
print(f" {tot_num_tables} tables created")
print(f" {tot_num_columns} columns created")
output.close()
