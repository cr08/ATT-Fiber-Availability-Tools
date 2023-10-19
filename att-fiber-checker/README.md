# ATT Fiber Availability Checker

Simple Python script that fetches the current AT&T Fiber availability for supplied addresses and posts the results to the terminal and optionally Slack and/or Discord.

Credit goes to [craig-rueda](https://github.com/craig-rueda) for the source this was forked from: [fiber-checker](https://github.com/craig-rueda/fiber-checker)

## Usage

0. Optionally setup a virtual env

```Bash
 virtualenv venv
 source ./venv/bin/activate
```

1. Install dependencies (slacker, argparse, discordwebhook, requests):

```Bash
 pip install argparse slacker discordwebhook requests
```

2. Copy and fill out `config.json.example` and `addresses.json.example`
   1. `config.json` contains Discord and Slack credentials. If you do not use one or the other, simply remove the block from the file. If you only intend to use this on the terminal, simply do not provide a `config.json` file.
      * A Slack API key can be acquired [here](https://api.slack.com/bot-users).
      * A Discord webhook URL is supplied by going to the settings of a channel on your server and viewing the Integrations tab.
   2. `addresses.json` contains addresses to be checked. There is no limit to how many can be included, though a large number could cause ATT to rate limit. I have not tested if they have any limits in place.
3. Run scraper.py

```Bash
 python scraper.py
```

 Additional command line options can be supplied per the help display:

```Bash
usage: scraper.py [-h] [-d] [-n]

Checks the configured addresses for availability of ATT Fiber and optionally posts the results to Slack and/or Discord

options:
  -h, --help     show this help message and exit
  -d, --debug    Enables debug logging to stdout and saves full json response file.
  -n, --nofiber  Send notification to Slack/Discord if no fiber is available.
```

## Configuration

 Configuration is done through two JSON files. One for the optional Slack/Discord credentials. The other is for the addresses to be checked.

`config.json`

```json
{
    "discord":
        {
            "webhook_url": "<Your Discord webhook URL>"
        },
    "slack":
        {
            "slack_key":"<Your bot's slack API key>",
            "slack_channel":"<The slack channel to post messages to>"
        }
}
```

`addresses.json`

```json
{
    "addresses": [
        {
            "addr_line": "123 my st.",
            "addr_zip": "12345"
        },
        {
            "addr_line": "123 my st.",
            "addr_zip": "12345"
        }
    ]
}
```
