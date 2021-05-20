import logging
import platform
from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import SlashCommand

import configs.config as config
import utils.functions.tools as tool

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
            owner_id = tool.read_config("bot_settings", "owner_id"),
            status=discord.Status.dnd,
            activity=discord.Game(
                name="waking up...",
                type=discord.ActivityType.playing)
            # help_command = None
        )

        self.emoji, self.colour, self.loaded_modules =  "<:moji:835960785158144050>", 0x6b9aba, []
        self.version, self.defaultprefix = config.bot_version, config.defaultprefix
        slash = SlashCommand(self, sync_commands=True)  #, override_type=True)

        logging.basicConfig(level=logging.INFO)
        self.load_extension("utils.extensions.logger")
        self.load_extension("utils.extensions.slash_manager")
        tool.load_modules(self)
        self.loop.create_task(self.ready())

    async def on_connect(self):
        print(f"""\n
        {tool.time}
        ___________________________________
        user            : {self.user}
        id              : {self.user.id}
        bot version     : {self.version}
        websocket       : {self.ws}
        python version  : {platform.python_version()}
        library version : {discord.__version__}
        """)
    
    async def on_disconnect(self):
        tool.logger.system.warning(f"CLIENT DISCONNECTED")
        self.disconnected_datetime = datetime.now()
        
        print(f"""\n
        {tool.time}
        ___________________________________
        {self.user} got disconnected
        bot uptime      : {tool.uptime(self, False)}
        """)

    async def on_resumed(self):
        reconnected_time = tool.time_delta(self.disconnected_datetime, False)
        tool.logger.system.warning(f"CLIENT RECONNECTED in {reconnected_time}")

        print(f"""\n
        {tool.time}
        ___________________________________
        {self.user} got reconnected in {reconnected_time}
        """)

    async def ready(self):
        await self.wait_until_ready()
        self.login_datetime = datetime.now()
        data = tool.read_database("counts")
        count = float(data["login_count"]) + 0.0001
        self.login_count = str(count + 0.0001)[2:6]
        data.update({"login_count": count})
        tool.update_database("counts", data)

        self.session = f"{self.version}.{self.login_count}"

        print(f"""
        bot session     : {self.session}
        bot users       : {str(len(self.users))}
        bot guilds      : {str(len(self.guilds))}
        """)
        tool.logger.system.info(f"CLIENT ONLINE")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="evryone", 
                type=discord.ActivityType.watching))

if __name__ == "__main__":
    butt().run(tool.classified(tool.read_config("bot_settings", "bot")))
