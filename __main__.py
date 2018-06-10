#!/usr/bin/env python3

import discord
import logging
import re
import gspread
import time
import json
from oauth2client.service_account import ServiceAccountCredentials


with open('config.json', 'r') as fd:
    config = json.load(fd)

mM_raid = re.compile('^Meowth!.*(Coordinate here!)')
gsheet_creds = ServiceAccountCredentials.from_json_keyfile_name(config['service_account_file'],
                                                                 ['https://spreadsheets.google.com/feeds'])

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='logs/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

tinyMeowth = discord.Client()
gsheet_client = gspread.authorize(gsheet_creds)


def getGsheetCreds():
    # Gets oauth2 credentials from gsheet
    try:
        print("Getting gsheet credentials")
        creds = gspread.authorize(gsheet_creds)
    except Exception as err:
        print("Exception getting gsheet credentials!")
        print(err)
        return
    return creds
    
def genGsheetDict(gc):
    for i in range(3):  # three tries to get spreadsheet
        try:
            print("opening gsheet")
            sheet = gc.open_by_key(config['gsheet_id']).sheet1  # connect to google sheet
        except Exception as err:
            print("Exception in opening gsheet!")
            print(err)
            gc = getGsheetCreds()
        else:
            break
    else:
        print("Failed getting spreadsheet three times")
        return

    gyms = [x.lower().strip() for x in sheet.col_values(1)]
    locations = sheet.col_values(2)
    
    return dict(zip(gyms, locations))
    
    
def findGymFromDict(gymDict, details):  # returns a gmaps link if the details are recognized in the cached gsheet info. returns False otherwise
    if details.lower().strip() in gymDict.keys():
        try:
            details = gymDict[details.lower().strip()]
        except KeyError:  # i don't know how we could end up with a keyerror.. but to be safe
            print("key error found. Returning a false match")
            return False
        # stealing Meowth's code to get another maps link
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
        # then channel location hints are not needed in the maps query
        if re.match(r'^\s*-?\d{1,2}\.?\d*,\s+-?\d{1,3}\.?\d*\s*$',
                    details):  # regex looks for lat/long in the format similar to 42.434546, -83.985195.
            return "https://www.google.com/maps/search/?api=1&query={0}".format('+'.join(details_list))

        return 'https://www.google.com/maps/search/?api=1&query={0}+{1}'.format('+'.join(details_list), config['loc_list'])

    else:  # exit if we didn't find a match in the spreadsheet
        return False


def findGym(gc, details):  # returns a gmaps link if the details are recognized from a direct poll of the gsheet. returns False otherwise
    for i in range(3):  # three tries to get spreadsheet
        try:
            print("opening gsheet")
            sheet = gc.open_by_key(config['gsheet_id']).sheet1  # connect to google sheet
        except Exception as err:
            print("Exception in opening gsheet!")
            print(err)
            gc = getGsheetCreds()
        else:
            break
    else:
        print("Failed getting spreadsheet three times")
        return False

    gyms = [x.lower().strip() for x in sheet.col_values(1)]  # Extract the list of location nicknames & clean them

    if details.lower().strip() in gyms:
        details = sheet.cell(gyms.index(details.lower().strip()) + 1, 2).value

        # stealing Meowth's code to get another maps link
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
        # then channel location hints are not needed in the maps query
        if re.match(r'^\s*-?\d{1,2}\.?\d*,\s+-?\d{1,3}\.?\d*\s*$',
                    details):  # regex looks for lat/long in the format similar to 42.434546, -83.985195.
            return "https://www.google.com/maps/search/?api=1&query={0}".format('+'.join(details_list))

        return 'https://www.google.com/maps/search/?api=1&query={0}+{1}'.format('+'.join(details_list), '+'.join(config['loc_list']))

    else:  # exit if we didn't find a match in the spreadsheet
        return False


@tinyMeowth.event
async def on_message(message):
    if message.author == tinyMeowth.user:  # don't want bot to reply to self
        return

    if message.author.id == config['mainMeowth_id'] and mM_raid.match(message.content):
        raid_name = message.content.split(".")[0].split(":")[-1].lstrip()  # magic that parses the reported raid name
        print("finding raid location")
        location = findGymFromDict(GsheetDict, raid_name)
        if location:
            print("GYM FOUND: " + raid_name)
            time.sleep(3)  # sleep for a short time so Meowth doesn't ignore us
            await tinyMeowth.send_message(message.channel, location)
        else:
            print("GYM NOT FOUND: " + raid_name)


@tinyMeowth.event
async def on_ready():
    print('Logged in as ' + tinyMeowth.user.name + " with ID " + tinyMeowth.user.id)

GsheetDict = genGsheetDict(getGsheetCreds())
tinyMeowth.run(config['bot_token'])
