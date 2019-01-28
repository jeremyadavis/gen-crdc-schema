print("Hello world!")

# path = '/Users/jdavis/Sites/CRDC_DATA/python/days.txt'
path = 'days.txt'

days_file = open(path, 'r')

days = days_file.read()

title = 'Dayss of the Week\n'

new_path = 'new_days.txt'
new_days = open(new_path, 'w')

new_days.write(title)
print(title)

new_days.write(days)
print(days)

days_file.close()
new_days.close()
