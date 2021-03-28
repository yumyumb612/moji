import discord
from discord.ext import commands

import utils.config as MOJI
import utils.tools as TOOLS

##########################################################
##                                                      ##
##          MOJI the new whoelesome emoji/bot           ##
##                                                      ##
##########################################################

moji = commands.Bot(
    command_prefix=TOOLS.get_prefix,
    description=MOJI.description,
    case_insensitive=True,
    intents=MOJI.intents,
    owner_id=622733200917004309,
    status=discord.Status.idle,
    activity=discord.Activity(type=discord.ActivityType.watching, name="evryone"))

TOOLS.print_log(moji)
TOOLS.load_cogs(moji)
TOOLS.load_manager(moji)
TOOLS.load_errorhandler(moji)

moji.run(TOOLS.classified('token'))