import csv
import sqlite3
from argparse import ArgumentParser
import os.path

parser = ArgumentParser(description='Imports CSV file in the format supplied by OpenAddresses into the SQLite DB.')
parser.add_argument('INPUT_CSV', metavar='input.csv', help='Input CSV file')
args = parser.parse_args()

try:
    input = open(args.INPUT_CSV, "r")
except OSError as error:
    print("Input file " + args.INPUT_CSV + " does not exist.")
    sys.exit(1)

try:
    output = open("addresses.db")
except OSError as error:
    print("SQLite database addresses.db not found. Creating...")
    connection = sqlite3.connect('addresses.db')
    cursor = connection.cursor()

    create_table = '''CREATE TABLE `addresses` (
                    `id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT ,
                    `lon` decimal(10,7) DEFAULT NULL,
                    `lat` decimal(9,7) DEFAULT NULL,
                    `number` TEXT DEFAULT NULL,
                    `street` TEXT DEFAULT NULL,
                    `unit` TEXT DEFAULT NULL,
                    `city` TEXT DEFAULT NULL,
                    `district` TEXT DEFAULT NULL,
                    `region` TEXT DEFAULT NULL,
                    `postcode` TEXT DEFAULT NULL,
                    `hash` TEXT DEFAULT NULL,
                    `availabilityStatus` TEXT DEFAULT NULL,
                    `lightGig` tinyINTEGER  DEFAULT NULL,
                    `time` INTEGER  DEFAULT NULL,
                    `updated` timestamp NULL DEFAULT NULL
                    );'''
    
    cursor.execute(create_table)

    connection.commit()
    connection.close()

connection = sqlite3.connect('addresses.db')
cursor = connection.cursor()

input = open(args.INPUT_CSV, "r")

contents = csv.reader(input)
next(contents)

insert_records = "INSERT INTO addresses (lon, lat, number, street, unit, city, district, region, postcode, hash) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

cursor.executemany(insert_records, contents)

select_all = "SELECT * FROM addresses"
rows = cursor.execute(select_all).fetchall()

for r in rows:
    print(r)

connection.commit()
connection.close()