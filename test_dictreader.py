import csv

print("\n\n\n----------------------------\nCreating School Scripts\n----------------------------\n")

# path = '/Users/jdavis/Sites/CRDC_DATA/python/days.txt'
path = 'input.txt'


with open(path, mode='r', encoding='LATIN-1') as csv_file:
    csv_reader = csv.DictReader(csv_file, delimiter='\t')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')

        print(
            f'\t{row["Field_Name"]} - {row["Field_Description"]} - {row["Module"]}')
        line_count += 1
        if line_count == 10:
            break
    print(f'Processed {line_count} lines.')
