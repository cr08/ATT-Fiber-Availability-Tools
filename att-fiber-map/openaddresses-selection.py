import csv
import sys
from shapely.geometry import Point, Polygon
from argparse import ArgumentParser

parser = ArgumentParser(description='Takes an input CSV database from openaddresses.io and with provided coordinates for upper left and lower right bounds of a square will pare down addresses within that area.')
parser.add_argument('INPUT_CSV', metavar='input.csv', help='Input CSV file')
parser.add_argument('OUTPUT_CSV', metavar='output.csv', help='Output/trimmed CSV file')
parser.add_argument('--coords', metavar="Coordinates", nargs="+", type=float, required=True, help='Coordinates for desired search area in decimal')

args = parser.parse_args()

try:
    input = open(args.INPUT_CSV, "r")
except OSError as error:
    print("Input file " + args.INPUT_CSV + " does not exist.")
    sys.exit(1)
    
input = open(args.INPUT_CSV, "r")
output = open(args.OUTPUT_CSV, "w+", newline='')

coords = list(zip(args.coords[::2], args.coords[1::2]))

contents = csv.reader(input)
next(contents)

writer = csv.writer(output)
csvheaders = ['LON', 'LAT', 'NUMBER', 'STREET', 'UNIT', 'CITY', 'DISTRICT', 'REGION', 'POSTCODE', 'HASH']
writer.writerow(csvheaders)

for row in contents:
    row_lon = str(row[0])
    row_lat = str(row[1])
    row_streetnum = str(row[2])
    row_street = str(row[3])
    row_unit = str(row[4])
    row_city = str(row[5])
    row_district = str(row[6])
    row_region = str(row[7])
    row_zip = str(row[8])
    row_hash = str(row[9])
    
    point = Point(row_lat, row_lon)
    poly = Polygon(coords)
    
    result = point.within(poly)
    
    if result is True:
        print(row_streetnum + " " + row_street + " is within the selected area.")
        writer.writerow([row_lon, row_lat, row_streetnum, row_street, row_unit, row_city, row_district, row_region, row_zip, row_hash])
        
input.close()
output.close()