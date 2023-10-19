# att-fiber-map

Address data found on http://results.openaddresses.io/?runs=all#runs

**WARNING!**  - Use this at your own risk, especially the `process.py` script. During testing and development, ATT had blocked me entirely from every page/resource on att.com for a few days. I don't advise using extremely large datasets. I have added some additional headers to fake a normal browser client and I also added a randomized delay between checks to attempt and mitigate ATT blocking access. It is not guaranteed however.

## Getting Started

* Starting out, you need a source of addresses which can be retrieved in the correct format at the openaddresses link above. You can then review the individual scripts below which are ordered in the general order they should be run.

## Scripts

###### (optional) `openaddresses-selection.py` - Takes the raw CSV address database from openaddresses as well as decimal GPS coordinates making a polygonal area on a map. All addresses within the area will be written to a new CSV file.

    GPS coordinates must be supplied in decimal and on lat,lon order. This has been designed with Google Maps in mind. Right clicking a point on the map and selecting the top menu option copies the coords for that point in lat,lon order. Comma must be removed. This is a polygonal search so many points can be used. Minimum of 4 points are required.

    `python openaddresses-selection.py input.csv output.csv --coords lat[1] lon[1] lat[2] lon[2] lat[3] lon[3] lat[4] lon[4]`

    `example: python openaddresses-selection.py input.csv output.csv --coords 12.111 34.111 12.222 34.222 12.333 34.333 12.444 34.444`

###### `import.py` - Takes an input CSV file with desired addresses. A Hardcoded `addresses.db` SQLite database is only checked if the file exists and created with the required schema. If the file exists, it is assumed it contains the proper schema and will not be verified. Once created/if exists, the addresses from the provided CSV file will be imported.

    `python import.py input.csv`

###### `process.py` - Runs through all addresses stored in the `addresses.db` SQLite database and checks ATT's API if fiber is available and stores that status back in the database. Only addresses that have not been verified yet to have fiber will be checked/rechecked and least recently updated addresses are checked first. Addresses already verified to have fiber via this tool are skipped to save extra unneeded queries to ATT's API.

    `python process.py`

###### `make-csv.py` - Takes the results stored in the `addresses.db` SQLite database and writes them back out to a CSV file for use with the interactive map.

    `python make-csv.py`

###### `index.html` - Simple html file containing the interactive map. Sources the `hasGig.csv` file created via `make-csv.py` to display markers for addresses verified to have fiber. Due to modern browsers and CORS security, this cannot be done locally without using special browser configs to bypass said security. Hosting on any basic web server will work in its place. `mapview.py` listed below provides an alternate method.

###### `mapview.py` - Very barebones web server run in python to view the interactive map. Hosts locally on `localhost:3600`

    `python mapview.py`

## Todo

* Make the `index.html` read the `addresses.db` SQLite database directly, thus eliminating the `make-csv.py` script and extra steps to create the  `hasGig.csv` file
