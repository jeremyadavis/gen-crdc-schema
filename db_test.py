import pandas
from sqlalchemy import create_engine
engine = create_engine('postgresql://postgres:@localhost:5431/postgres')

file_name = 'crdc1516_advanced_mathematics'
df = pandas.read_csv(
    f'./output/schema_data/{file_name}.csv')

print(df.head())
print(engine)


df.to_sql(file_name, engine, if_exists="replace", index=False)
