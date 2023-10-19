# ATT-Fiber-Availability-Tools

A few tools to have more detailed and (hopefully) current view of AT&T fiber service, sourcing their own database/API.

##### [att-fiber-checker](att-fiber-checker/)

    A 'single shot' fiber availability checker. Takes one or multiple addresses and will query ATT's API for fiber availability and displays the result to the terminal or optionally to a Slack or Discord channel.

##### [att-fiber-map](att-fiber-map/)

    A more involved tool that can take a database of addresses for a given geographical area, check and store the fiber availability status, then displays the results on an interactive map.

## Credits

att-fiber-checker: Original code by [craig-rueda](https://github.com/craig-rueda/) ([fiber-checker](https://github.com/craig-rueda/fiber-checker)) - Updated to allow multiple addresses and add Discord support

att-fiber-map: Original code by [brianherbert](https://github.com/brianherbert) ([att-fiber-map](https://github.com/brianherbert/att-fiber-map)) - Overhauled to do most of the work locally as self contained python scripts and an SQLite database, updated to use a new ATT API address.
