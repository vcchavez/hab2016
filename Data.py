import csv
def csv_to_list(filename):
    with open(filename) as csvfile: 
        csvreader = csv.reader(csvfile)
        rows = []
        for row in csvreader:
        	if not(row[0] == 'Store_Name'):
				rows.append(row)
    return rows

DATA = csv_to_list('ids.csv')