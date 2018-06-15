# Tiny Meowth
![discord.py](https://img.shields.io/badge/discord.py-v1.0.0a-green.svg)
![python](https://img.shields.io/badge/python-3.6-blue.svg)

A bot for Pokemon Go Discord servers - meant to assist the [Meowth](https://github.com/FoglyOgly/Meowth) Discord helper bot that is already in so many servers.

This was created for features that are difficult to bake into the Meowth project.

## Features
- Updates directions for newly created raid channels

## Requirements
- Python 3.6+
- [discord.py](https://github.com/Rapptz/discord.py/tree/rewrite) `rewrite` branch and its dependencies
- [gspread](https://github.com/burnash/gspread) library
- [oauth2client](https://github.com/google/oauth2client/) library
- Google Spreadsheet

To install [discord.py (rewrite branch)](https://github.com/Rapptz/discord.py/tree/rewrite), use the following:
```
python3 -m pip install -U git+https://github.com/Rapptz/discord.py@rewrite
```
`pip` should take care of all other libraries.

## Restrictions
Because Meowth is programmed to _ignore_ commands from other bots, Tiny Meowth can only reply with Google Maps links in order to update raid locations.

## Setup
1. [Create your own Discord Bot](https://discordapp.com/developers/applications/me) and make note of the bot token.

2. Create and download a Service Account Key for the Google Sheets API. General procedure can be found in the [gspread documentation](http://gspread.readthedocs.io/en/latest/oauth2.html). Place the key JSON file in the same folder as the bot.

3. Create a new Google spreadsheet with the **FIRST** worksheet in the following format:
  - Column A: Gym name
  - Column B: Google Maps link, GPS coordinates, or street address of gym location

**HINT:** If your area requires driving to raids, you may want to use best parking location instead of actual gym location.

4. Create a **SECOND** worksheet in your Google spreadsheet for any Gym Aliases - ie, common names/mispellings people use for gyms other than the actual gym name. Use the same format as above:
  - Column A: Gym alias
  - Column B: Google Maps link, GPS coordinates, or street address of gym location

5. Open the Google Sheets Service Account Key and look for the `client_email` field. Share the Google spreadsheet with this email address, with a minimum of read access. Example of this field:
```json
  "client_email": "user@bot.iam.gserviceaccount.com",
```

6. Make a note of the spreadsheet ID. This can be found in the URL of the spreadsheet. Example:
`https://docs.google.com/spreadsheets/d/spreadsheet_ID/edit#gid=0`

7. Make a copy of `config_blank.json` and name it `config.json`. This will be where you change your settings. Open the JSON file and take the information noted in the previous steps and replace the strings in the following fields, then save:

```json
"bot_token": "yourtoken",
"service_account_file": "filename.json",
"gsheet_id": "your sheet id",
"loc_list": "orange+county+ca"
```
**NOTE**: Make sure your strings are enclosed by `"` and that your server location uses `+` to join multiple words!

8. (optional) By default, Tiny Meowth listens to the public version Meowth that can be invited to your server. If you are running your own instance of Meowth (or somehow the underlying ID changes), change the `mainMeowth_id` key to reflect the new main Meowth ID:

```json
"mainMeowth_id": 346759953006198784,
```
To get this ID, [enable developer view](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) in Discord, right click on Meowth, and select 'Copy ID'.

9. Run `__main__.py` and you should see your bot come online. It will be listening to Meowth and respond if necessary!
