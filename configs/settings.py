import discord

owner_ids= [622733200917004309]
bot_version= "7.0.0 alpha"

default_prefix= "moji."
description= "Sir Moji of Honkburg."
home_guild_id= 811462348560007198

allowed_mentions= discord.AllowedMentions(
    everyone= True, 
    users= True, 
    roles= True, 
    replied_user= True
)
intents= discord.Intents.all()

#   Nord Polar Night and Snow Storm 
#   https://www.nordtheme.com/
colour= {
    "dark1": 0x2e3440,
    "dark2": 0x3b4252,
    "dark3": 0x434c5e,
    "dark4": 0x4c566a,

    "light1": 0xd8dee9,
    "light2": 0xe5e9f0,
    "light3": 0xeceff4,
}

timezone= "US/Eastern"
datetime_format= "%A %B %d, %Y %I:%M%p"
datetime_format_UTC= "%A %d, %B %Y %I:%M%p UTC"

logging_format= "%(asctime)s:%(levelname)s:%(name)s: %(message)s"
