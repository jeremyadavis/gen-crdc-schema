import pandas


def module_to_table_name(module): return module.replace(
    ' ', '_').replace('-', '_').lower()

"""
  Get School Layout CSV File
  Append generated table name from module column
  Append next row's table name for loop comparisons
"""


def get_school_layout(input_dir):
    df = pandas.read_csv(input_dir+"/school_layout.csv",
                         encoding='LATIN-1',
                         header=0,
                         names=['order', 'excel_column',
                                'column_name', 'description', 'module']
                         )

    df['table_name'] = df['module'].map(module_to_table_name)
    df['next_table_name'] = df['table_name'].shift(-1)

    return df


# def get_school_form_ddl_file():
#     return pandas.read_csv('data/schoolform_ddl.txt',
#                            delimiter="|",
#                            index_col='column_name',
#                            names=['column_name', 'type', 'extra']
#                            )


def get_school_data(input_dir, num_rows=None):
    # df_dtypes = pandas.read_csv(
    #     input_dir+"data/school_data_dtypes.csv",
    #     names=["column_name", "type"],
    #     index_col="column_name")

    # dtypes = {}

    # for row in df_dtypes.itertuples():
    #     dtypes[row.Index] = row.type

    # Using combokey as index so that it will always be first column for output
    # Might be useful to slice with as well
    df = pandas.read_csv(input_dir+"/school_data.csv",
                         encoding='LATIN-1',
                         index_col='COMBOKEY',
                         #  dtype=dtypes,
                         nrows=num_rows
                         )

    # =========== Make Data Types file from to speed up intial file load
    # df.dtypes.to_csv('./data/school_data_dtypes.csv')

    return df
