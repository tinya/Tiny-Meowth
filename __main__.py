#!/usr/bin/env python3

import discord
import logging
import re
import gspread
from oauth2client.service_account import ServiceAccountCredentials

bot_token = 'BOT TOKEN HERE'
gsheet_id = 'G SHEET ID HERE'
mainMeowth_id = '346759953006198784'
service_account_file = 'client-secret.json'
loc_list = ["your", "loc", "here"]  # ie orange county ca is ["orange", "county", "ca"]

mM_raid = re.compile('^Meowth!.*(Coordinate here!)')
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name(service_account_file,
                                                                 ['https://spreadsheets.google.com/feeds'])

logging.basicConfig(level=logging.INFO)

tinyMeowth = discord.Client()
gsheet_client = gspread.authorize(gsheet_creds)

def findGym(details):  # returns a gmaps link if the details are recognized. returns False otherwise
    try:
        # connect to google sheet
        sheet = gsheet_client.open_by_key(gsheet_id).sheet1

        # Extract the list of location nicknames & clean them
        gyms = [x.lower().strip() for x in sheet.col_values(1)]

        if details.lower().strip() in gyms:
            details = sheet.cell(gyms.index(details.lower().strip()) + 1, 2).value
        else:  # exit if we didn't find a match in the spreadsheet
            return False
    except Exception as err:
        print(err)

    # litterally stealing Meowths code to get another maps
    if "/maps" in details and "http" in details:
        mapsindex = details.find('/maps')
        newlocindex = details.rfind('http', 0, mapsindex)
        if newlocindex == (- 1):
            return
        newlocend = details.find(' ', newlocindex)
        if newlocend == (- 1):
            newloc = details[newlocindex:]
            return newloc
        else:
            newloc = details[newlocindex:newlocend + 1]
            return newloc
    details_list = details.split()
    # look for lat/long coordinates in the location details. If provided,
    # then channel location hints are not needed in the	maps query
    if re.match(r'^\s*-?\d{1,2}\.?\d*,\s+-?\d{1,3}\.?\d*\s*$',
                details):  # regex looks for lat/long in the format similar to 42.434546, -83.985195.
        return "https://www.google.com/maps/search/?api=1&query={0}".format('+'.join(details_list))

    return 'https://www.google.com/maps/search/?api=1&query={0}+{1}'.format('+'.join(details_list), '+'.join(loc_list))


@tinyMeowth.event
async def on_message(message):
    if message.author == tinyMeowth.user:  # don't want bot to reply to self
        return

    if message.author.id == mainMeowth_id and mM_raid.match(message.content):
        raid_name = message.content.split(".")[0].split(":")[-1].lstrip()  # magic that parses the reported raid name
        location = findGym(raid_name)
        if location:
            await tinyMeowth.send_message(message.channel, location)
        else:
            print(raid_name + ' location not found in sheet.')


@tinyMeowth.event
async def on_ready():
    print('Logged in as ' + tinyMeowth.user.name + " with ID " + tinyMeowth.user.id)


tinyMeowth.run(bot_token)
