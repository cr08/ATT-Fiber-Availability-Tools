import sqlite3
import csv
import sys

try:
    input = open("addresses.db")
except OSError as error:
    print("SQLite database addresses.db not found.")
    sys.exit(1)

connection = sqlite3.connect('addresses.db')
cursor = connection.cursor()

output = open("hasGig.csv", "w+", newline='')

cursor.execute("SELECT lon, lat FROM addresses WHERE lightGig = 1")

rows = cursor.fetchall()

writer = csv.writer(output)
csvheaders = ['latitude', 'longitude']
writer.writerow(csvheaders)

for row in rows:
    row_lon = str(row[0])
    row_lat = str(row[1])
    
    writer.writerow([row_lat, row_lon])

output.close()