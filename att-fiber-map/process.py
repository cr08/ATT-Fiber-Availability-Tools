import sqlite3
import requests
import json
import sys
import time
import random

try:
    input = open("addresses.db")
except OSError as error:
    print("SQLite database addresses.db not found. Please run the import.py script to generate an address database. Review the README.md for more information.")
    sys.exit(1)

connection = sqlite3.connect('addresses.db')
cursor = connection.cursor()

cursor.execute("SELECT * FROM addresses WHERE lightGig = 0 OR lightGig IS NULL ORDER BY updated ASC")

rows = cursor.fetchall()
totalcount = len(rows)

count = 0

for row in rows:
    try:

        row_id = str(row[0])
        row_lon = str(row[1])
        row_lat = str(row[2])
        row_streetnum = str(row[3])
        row_street = str(row[4])
        row_zip = str(row[9])
        row_fiberavail = str(row[12])
        row_availtime = str(row[13])
        row_updated = str(row[14])

        availability_url = 'https://www.att.com/services/shop/model/ecom/shop/view/unified/qualification/service' \
                    '/CheckAvailabilityRESTService/invokeCheckAvailability'

        json_data = {
            'userInputZip': row_zip,
            'userInputAddressLine1': row_streetnum + " " + row_street,
            'mode': 'fullAddress',
            'customer_type': 'Consumer',
            'dtvMigrationFlag': False
        }
        headers = {'Origin': 'https://www.att.com', 'Accept-Encoding': 'gzip, deflate, br', 'Accept-Language': 'en-US,en;q=0.9', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36', 'Content-Type': 'application/json', 'Accept': 'application/json', 'Referer': 'https://www.att.com/buy/broadband/plans', 'Authority': 'www.att.com'}
        
        fiber_avail = False
        count = count + 1
        
        print(str(count) + "/" + str(totalcount) + " Checking \033[1;33m" + row_streetnum + " " + row_street + ", " + row_zip + "\033[1;0m...  ", end="", flush=True)

        try:
            resp = requests.post(availability_url, data = json.dumps(json_data), headers = headers)
            resp_json = json.loads(resp.text)
            fiber_avail = resp_json['profile']['isGIGAFiberAvailable']
        except:
            print("Unexpected error:", sys.exc_info()[0])
            break

        if fiber_avail:
            print("\033[1;32mFiber IS available!\033[1;0m ", end="", flush=True)
            if row_fiberavail is False:
                curtime = str(time.time())
                cursor.execute("""UPDATE addresses SET lightgig = 1, time = ?, updated = ? WHERE id = ?;""", (curtime, curtime, row_id))
            else:
                curtime = str(time.time())
                cursor.execute("""UPDATE addresses SET lightgig = 1, updated = ? WHERE id = ?;""", (curtime, row_id))
        else:
            print("\033[1;31mFiber is NOT available.\033[1;0m ", end="", flush=True)
            curtime = str(time.time())
            cursor.execute("""UPDATE addresses SET lightgig = 0, updated = ? WHERE id = ?;""", (curtime, row_id))

        # Adding commit line to ensure the database is properly updated each check.
        connection.commit()
            
    except KeyboardInterrupt:
        print("Script cancelled. Writing and closing DB.")
        break
    
    delay = random.randint(5,60)
    print("Waiting " + str(delay) + " seconds before next check...")
    time.sleep(delay)

connection.commit()
print("DEBUG: End of script. DB commit finished.")
connection.close()
print("DEBUG: End of script. DB closed.")