import discord
from discord.ext import commands

import config as MOJI

##########################################################
##                                                      ##
##          MOJI the new whoelesome emoji/bot           ##
##                                                      ##
##########################################################

#   moji
moji = commands.Bot(
    command_prefix=MOJI.get_prefix,
    description=MOJI.description,
    case_insensitive=True,
    intents=MOJI.intents,
    owner_id=MOJI.developer)

MOJI.log(moji)
MOJI.load_cogs(moji)

moji.run(MOJI.token())