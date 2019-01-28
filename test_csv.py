import csv
from collections import namedtuple

print("\n\n\n----------------------------\nCreating School Scripts\n----------------------------\n")

# path = '/Users/jdavis/Sites/CRDC_DATA/python/days.txt'
path = 'input.txt'

with open(path, 'r', encoding='LATIN-1') as f:
    reader = csv.reader(f, delimiter='\t', )
    for row in reader:
        print(row)
