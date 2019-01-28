import pandas

# path = '/Users/jdavis/Sites/CRDC_DATA/python/days.txt'
path = 'input.txt'

df = pandas.read_csv(path,
                     delimiter='\t',
                     encoding='LATIN-1', escapechar='\\',
                     index_col='order',
                     header=0,
                     names=['order', 'excel_column',
                            'column_name', 'description', 'module']
                     )

# print(df['column_name'][0])
# print(type(df['column_name'][0]))
# print(df.head(20))
# print(df.describe()) #stats
# print(df.T) #transpose
# print(df.sort_values(by='module', ascending=False).head(20))
# print(df[1800:1825])

# for index, row in df.iterrows():
#     print(row['column_name'] + ' - ' + row['module'])

line_count = 0
for row in df.itertuples(index=True, name='Records'):
    if(line_count < 10):
        print(row)
        line_count += 1

        # print(getattr(row, "column_name"), getattr(row, "module"))
