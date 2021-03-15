import discord
from discord.ext import commands

import utils.config as MOJI
import utils.tools as TOOLS

##########################################################
##                                                      ##
##          MOJI the new whoelesome emoji/bot           ##
##                                                      ##
##########################################################

#   moji
moji = commands.Bot(
    command_prefix=TOOLS.get_prefix,
    description=MOJI.description,
    case_insensitive=True,
    intents=MOJI.intents,
    owner_id=MOJI.developer)
 
TOOLS.log(moji)
TOOLS.load_cogs(moji)
TOOLS.load_manager(moji)

moji.run(MOJI.classified('token'))