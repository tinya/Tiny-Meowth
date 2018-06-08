#!/usr/bin/env python3

import discord
import asyncio
import logging
import re
import time

bot_token = 'YOUR TOKEN HERE'
mainMeowth_id = '346759953006198784'

mM_raid = re.compile('^Meowth!.*(Coordinate here!)')

logging.basicConfig(level=logging.INFO)

tinyMeowth = discord.Client()
loop = asyncio.get_event_loop_policy()


@tinyMeowth.event
async def on_message(message):
    if message.author == tinyMeowth.user:  # don't want bot to reply to self
        return

    if message.author.id == mainMeowth_id and mM_raid.match(message.content):
        raid_name = message.content.split(".")[0].split(":")[-1].lstrip()  # magic that parses the reported raid name
        print(raid_name)
        msg = 'google link'
        time.sleep(4)  # sleep, otherwise Meowth ignores me
        await tinyMeowth.send_message(message.channel, msg)


@tinyMeowth.event
async def on_ready():
    print('Logged in as ' + tinyMeowth.user.name + " with ID " + tinyMeowth.user.id)


tinyMeowth.run(bot_token)
