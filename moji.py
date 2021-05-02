import logging
import platform
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import SlashCommand#, SlashCommandOptionType, SlashContext

import configs.config as config
import utils.tools as tool

##########################################################
##                                                      ##
##          moji the new whoelesome emoji/bot           ##
##                                                      ##
##########################################################

class butt(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix = tool.set_prefix,
            description = config.description,
            case_insensitive = True,
            reconnect = True,
            intents = config.intents,
            owner_id = config.owner_id,
            status=discord.Status.dnd,
            activity=discord.Game(
                name="Booting...",
                type=discord.ActivityType.playing)
            # help_command = None
        )

        self.version, self.defaultprefix, self.fuud, self.loaded_modules = "6.1.3", "moji.", "🍞", []
        logging.basicConfig(level=logging.INFO)
        self.load_extension("utils.manager")
        tool.load_modules(self)
        self.loop.create_task(self.ready())

    async def on_connect(self):
        print(f"""\n
        {tool.time}
        ____________________________
        {self.user.name} is awakening...
        bot version     : {self.version}
        websocket       : {self.ws}
        python version  : {platform.python_version()}
        discord version : {discord.__version__}
        """)

    async def on_resumed(self):
        print(f"""\n
        {tool.time}: reconnected
        \n""")

    async def ready(self):
        await self.wait_until_ready()
        self.login_time = datetime.now()

        print(f"""
            {self.user} online!
            id     : {self.user.id}
            users  : {str(len(self.users))}
            guilds : {str(len(self.guilds))}
            \n""")
        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="evryone", 
                type=discord.ActivityType.watching))

        slash = SlashCommand(self, sync_commands=True)
        op = [
            {
                "name": "x",
                "description": "!@#$%",
                "required": True,
                "type": 3,
            },
            {
                "name": "y",
                "description": "!@#$%",
                "required": False,
                "type": 4
            }
        ]
        @slash.slash(
            name="honk",
            description="honk, ur found a cookie.",
            guild_ids=[...],
            options=op)
        async def honk(ctx: SlashCommand, msg, time=None):
            if int(ctx.author.id) == int(self.owner_id):
                await ctx.channel.send(content=msg, delete_after=time)
            else:
                best_song="""
                    ||Never gonna give you up
                    Never gonna let you down
                    Never gonna run around and desert you
                    Never gonna make you cry
                    Never gonna say goodbye
                    Never gonna tell a lie and hurt you||"""
                await ctx.send(content=f"**sowy ur not allowd to use dis command!**\n{best_song}", hidden=True)

if __name__ == "__main__":
    butt().run(tool.classified("moji"))
