# Tiny-Meowth
![discord.py](https://img.shields.io/badge/discord.py-v0.16.6-green.svg)
![python](https://img.shields.io/badge/python-3.6-blue.svg)

A bot for Pokemon Go Discord servers - meant to assist the [Meowth](https://github.com/FoglyOgly/Meowth) Discord helper bot that is already in so many servers.

This was created for features that are hard to bake into the Meowth project.

## Features
- Updates directions for newly created raid channels

## Dependencies
- Python 3.6+
- [discord.py](https://github.com/Rapptz/discord.py) and its dependencies


## Setup
1. [Create your own Discord Bot](https://discordapp.com/developers/applications/me) and make note of the bot token.
2. Replace `YOUR TOKEN HERE` with your bot token:

```python
bot_token = 'YOUR TOKEN HERE'
```
3. (optional) By default, Tiny Meowth listens to the public version Meowth that can be invited to your server. If you are running your own instance of Meowth (or somehow the underlying ID changes), change the `mainMeowth_id` variable to reflect the new main Meowth ID:

```python
mainMeowth_id = '346759953006198784'
```

To get this ID, [enable developer view](https://support.discordapp.com/hc/en-us/articles/206346498-Where-can-I-find-my-User-Server-Message-ID-) in Discord, right click on Meowth, and select 'Copy ID'.

4. Run `__main__.py` and you should see your bot come online. It will being listening to Meowth!
