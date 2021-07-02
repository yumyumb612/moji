import logging
import os
import platform
from datetime import datetime

import discord
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
    print("> booting")

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
                name="arising... pls w8",
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
        print("> setting up da logger")
        logger = logging.getLogger("discord")
        logger.setLevel(logging.DEBUG if self.settings["mode"] == "debug" else logging.INFO)
        handler = logging.FileHandler(filename=f"{tool.get_path()}/logs/session.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter(config.logging_format))
        logger.addHandler(handler)
        self.load_extension("utils.extensions.logger")
        print("done")

        # database
        print("> connecting to da database")
        client = pymongo.MongoClient(os.getenv("MONGODB_CONNECTION_STRING"), serverSelectionTimeoutMS=60000)
        self.db = client["mojidb"]
        self.configs = self.db["configs"]

        try:
            client.server_info()
            print("connected")
        except Exception as error:
            print(f"unable to connect: {error}")

        # load modules
        print("> loading modules")
        self.load_extension("utils.extensions.slash_manager")
        tool.load_modules(self)
        print(f"loaded {len(self.loaded_modules)} modules")

    async def on_resumed(self):
        self.disconnected = False

        print(f"\n-----[{self.user} got reconnected]-----\n")
        logger.activity.info(f"{self.user} got reconnected")

    async def on_connect(self):
        if not hasattr(self, "disconnected") or not self.disconnected:
            print(f"\n-----[{self.user} connected to discord]-----\n")
        else:
            print(f"\n-----[{self.user} got reconnected]-----\n")

    async def on_disconnect(self):
        if not hasattr(self, "disconnected"):
            self.disconnected_datetime, self.disconnected = datetime.now(), True

            print(f"\n-----[{self.user} got disconnected]-----\n")
            logger.activity.critical(f"{self.user} got disconnected")
        else:
            pass

    async def on_ready(self):
        await self.wait_until_ready()
        self.login_datetime = datetime.now()
        self.owner_object = self.get_user(self.owner_ids[0])

        data = reader.read_database("counts", "json")
        count = float(data["login_count"]) + 0.0001
        data.update({"login_count": count})
        reader.update_database("counts", data)

        self.login_count = str(reader.read_database("counts", "json", "login_count"))[2:6]
        self.session = f"{self.bot_version}.{self.login_count}"

        # if not hasattr(self, "disconnected"):
        self.boot_duration = str_format.number_noun(float((datetime.now() - self.boot_datetime).microseconds) / 1000000, "second", False)
        print(
            f"\n----------[{self.user} online]----------"
            f"\n id            : {self.user.id}"
            f"\n bot version   : {self.bot_version}"
            f"\n session       : {self.session}"
            f"\n boot duration : {self.boot_duration}"
            f"\n users         : {str(len(self.users))}"
            f"\n guilds        : {str(len(self.guilds))}"
            f"\n emojis        : {str(len(self.emojis))}"
        )

        logger.activity.info(f"moji online")

        await self.change_presence(
            status=discord.Status.online,
            activity=discord.Activity(
                name="cows fly", 
                type=discord.ActivityType.watching
            )
        )

if __name__ == "__main__":
    butt().run(os.getenv("TOKEN"))
