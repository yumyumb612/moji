import logging
import os
import platform
from datetime import datetime

import discord
from utils.database.mongodb import mongodb
import pymongo
from discord.ext import commands
from discord_slash import SlashCommand
from dotenv import load_dotenv

import configs.config as config
import utils.functions.loggers as logger
import utils.functions.readers as reader
import utils.functions.string_formaters as str_format
import utils.functions.tools as tool


load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "configs/.evn"), override=True)
class butt(commands.AutoShardedBot):

    class WarningEmbed(discord.Embed):
        def __init__(self, **kwargs):
            title= kwargs.pop("title", "MOJI WARNING ⚠️")
            timestamp = kwargs.pop("timestamp", datetime.now())
            colour = kwargs.pop("colour", config.colour["warning"])
            super().__init__(**kwargs, title=title, timestamp=timestamp, colour=colour)
    
    class TimeoutErrorEmbed(discord.Embed):
        def __init__(self, **kwargs):
            title= kwargs.pop("title", "Timeout Error")
            description = kwargs.pop("description", "Maximum given time was reached. Pls try again")
            timestamp = kwargs.pop("timestamp", datetime.now())
            colour = kwargs.pop("colour", config.colour["error"])
            super().__init__(**kwargs, title=title, description=description, timestamp=timestamp, colour=colour)

    class ErrorEmbed(discord.Embed):
        def __init__(self, **kwargs):
            title= kwargs.pop("title", "wooups❗ \nsmthn went terribly wrong")
            timestamp = kwargs.pop("timestamp", datetime.now())
            colour = kwargs.pop("colour", config.colour["error"])
            super().__init__(**kwargs, title=title, timestamp=timestamp, colour=colour)

    class DebugEmbed(discord.Embed):
        def __init__(self, **kwargs):
            title= kwargs.pop("title", "debug mode")
            timestamp = kwargs.pop("timestamp", datetime.now())
            colour = kwargs.pop("colour", config.colour["debug"])
            super().__init__(**kwargs, title=title, timestamp=timestamp, colour=colour)

    def __init__(self):
        super().__init__(
            command_prefix = tool.set_prefix,
            description = config.description,
            case_insensitive = True,
            reconnect = True,
            intents = config.intents,
            owner_ids = config.owner_ids,
            status=discord.Status.dnd,
            activity=discord.Game(
                name="waking up...",
                type=discord.ActivityType.playing
            )
            # help_command = None
        )

        # setting som things
        self.settings = {
            "mode": "normal",
            "mood": "cheeky"
        }
        self.colour = {
            "main": config.colour["main"],
            "error": config.colour["error"],
            "warning": config.colour["warning"],
            "mood": config.colour["main"]
        }
        self.emoji = {
            "moji": reader.read_emoji("moji"),
            "mojito": reader.read_emoji("mojito"),

            "discord": reader.read_emoji("discord"),

            "check_mark": reader.read_emoji("check_mark"),
            "x_mark": reader.read_emoji("x_mark"),
            "empty_mark": reader.read_emoji("empty_mark")
        }
        self.boot_datetime, self.loaded_modules =  datetime.now(), []
        self.bot_version, self.py_version, self.dpy_version = config.bot_version, platform.python_version(), f"{discord.__version__} {discord.version_info.releaselevel}"
        self.defaultprefix = config.defaultprefix
        SlashCommand(self, sync_commands=True, sync_on_cog_reload=True, override_type=True)

        # logging
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG if self.settings["mode"] == "debug" else logging.INFO)
        handler = logging.FileHandler(filename=f"{tool.get_path()}/logs/session.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter(config.logging_format))
        logger.addHandler(handler)
        self.load_extension("utils.extensions.logger")

        # database
        client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"), serverSelectionTimeoutMS=5000)
        db = client["mojidb"]
        self.collection = db["guildinfo"]
        
        try:
            print(client.server_info())
        except Exception:
            print("unable to connect to the server.")

        # load modules
        self.load_extension("utils.extensions.slash_manager")
        tool.load_modules(self)

        self.loop.create_task(self.ready())

    async def on_connect(self):
        print(f"""\n
        {tool.datetime_EDT_now}
        ___________________________________
        user               : {self.user}
        id                 : {self.user.id}
        bot version        : {self.bot_version}
        python version     : {self.py_version}
        discord.py version : {self.dpy_version}
        """)
    
    async def on_disconnect(self):
        self.disconnected_datetime, self.disconnected = datetime.now(), True
        uptime = tool.uptime(self, False)

        print(f"""\n
        {tool.datetime_EDT_now}
        ___________________________________
        {self.user} got disconnected
        bot uptime        : {uptime}
        """)
        logger.activity.critical(f"moji got disconnected, been up for {uptime}")

    async def on_resumed(self):
        reconnection_time = tool.datetime_delta(self.disconnected_datetime, datetime.now(), False)

        print(f"""\n
        {tool.datetime_EDT_now}
        ___________________________________
        {self.user} got reconnected, took {reconnection_time} to reconnect
        """)
        self.disconnected = False
        logger.activity.info(f"moji got reconnected, took {reconnection_time} to reconnect")

    async def ready(self):
        await self.wait_until_ready()
        self.login_datetime = datetime.now()
        self.owner_object = self.get_user(self.owner_ids[0])

        data = reader.read_database("counts", "json")
        count = float(data["login_count"]) + 0.0001
        data.update({"login_count": count})
        reader.update_database("counts", data)

        self.login_count = str(reader.read_database("counts", "json", "login_count"))[2:6]
        self.session = f"{self.bot_version}.{self.login_count}"

        if not hasattr(self, "disconnected"):
            self.disconnected = False
            self.boot_duration = str_format.number_noun(float((datetime.now() - self.boot_datetime).microseconds) / 1000000, "second", False)
            print(f"""
            session       : {self.session}
            boot duration : {self.boot_duration}
            users         : {str(len(self.users))}
            guilds        : {str(len(self.guilds))}
            emojis        : {str(len(self.emojis))}
            """)

            logger.activity.info(f"moji online")
        else:
            reconnection_time = tool.datetime_delta(self.disconnected_datetime, datetime.now(), False)

            print(f"""\n
            {tool.datetime_EDT_now}
            ___________________________________
            {self.user} got reconnected in {reconnection_time}
            """)
            self.disconnected = False
            logger.activity.info(f"moji got reconnected in {reconnection_time}")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="evryone", 
                type=discord.ActivityType.watching
            )
        )

if __name__ == "__main__":
    butt().run(os.getenv("TOKEN"))
