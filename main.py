import logging
import os
from datetime import datetime
from platform import python_version

import discord
import pymongo
from discord.ext.commands import AutoShardedBot
from discord_components import DiscordComponents
from discord_slash import SlashCommand
from dotenv import load_dotenv

import configs.settings as settings
import helpers.functions.loggers as logger
import helpers.functions.tools as tool
from helpers.database.mongodb import collection

cwd= os.path.dirname(__file__)
load_dotenv(dotenv_path=os.path.join(cwd, "configs/.evn"), override=True)
class butt(AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix= tool.set_prefix,
            description= settings.description,
            status= discord.Status.dnd,
            activity= discord.Game(
                name= "Vivifying. please wait",
                start= datetime.utcnow(),
                type= discord.ActivityType.unknown
            ),
            allowed_mentions= settings.allowed_mentions,
            case_insensitive= True,
            intents= settings.intents,
            owner_ids= settings.owner_ids,
            strip_after_prefix= True
        )
        #   interactions
        SlashCommand(self, sync_commands=True, sync_on_cog_reload=True, override_type=True)
        DiscordComponents(self)

        #   attributes
        self.boot_datetime= datetime.utcnow()
        self.cwd: str= cwd
        self.commands_completed= self.commands_run= self.command_errors= self.self_errors= 0
        self.blocked_users= self.recent_users= []
        self.versions= {
            "bot": settings.bot_version,
            "dpy": f"{discord.__version__} {discord.version_info.releaselevel}",
            "py": python_version()
        }
        self.cog_counts= {
            "all": [],
            "loaded": [],
            "commands": [],
            "listeners": []
        }

        #   logging
        print(f"{datetime.now()}: Setting up logging...")
        # logging.basicConfig(level=logging.INFO)

        discord_logger= logging.getLogger("discord")
        discord_logger.setLevel(logging.DEBUG)
        discord_handler= logging.FileHandler(filename= f"{self.cwd}/logs/discord.log", encoding= "utf-8", mode= "w")
        discord_handler.setFormatter(logging.Formatter(settings.logging_format))
        discord_logger.addHandler(discord_handler)

        self.butt_logger= logger.butt
        self.event_logger= logger.event
        self.command_logger= logger.command

        logger.butt.log(20, "Started logging")
        print(f"{datetime.now()}: Done setting logging")

        # database
        print(f"{datetime.now()}: Connecting to MongoDB database...")
        try:
            mongodb_client= pymongo.MongoClient(os.getenv("mongodb_connection_string"), serverSelectionTimeoutMS=20000)
            self.db= mongodb_client["mojidb"]
            self.guild_settings= collection(self.db, "guild_settings")

            # mongodb_client.server_info()
            print(f"{datetime.now()}: Connected to the database")
        except Exception as error:
            print(f"{datetime.now()}: {error}\n")

        #   cogs
        print(f"{datetime.now()}: Loading the cog(s)...")
        cog_paths= [f"{self.cwd}/cogs/commands", f"{self.cwd}/cogs/listeners"]
        def load_check(filename):
            return filename.endswith('.py') and not filename.startswith("_")
        
        self.load_extension("helpers.managers.cog_manager")

        for path in cog_paths:
            for filename in os.listdir(path):
                if filename == "__pycache__":
                    continue
                else:
                    self.cog_counts["all"].append(filename.replace(".py", ""))
                    if path == cog_paths[0]:
                        self.cog_counts["commands"].append(filename.replace(".py", ""))
                        if load_check(filename):
                            self.load_extension(f"cogs.commands.{filename.replace('.py', '')}")
                        else:
                            continue
                    else:
                        self.cog_counts["listeners"].append(filename.replace(".py", ""))
                        if load_check(filename):
                            self.load_extension(f"cogs.listeners.{filename.replace('.py', '')}")
                        else:
                            continue
        print(f"{datetime.now()}: Loaded {len(self.cog_counts['loaded'])}/{len(self.cog_counts['all'])} cog(s)")
        self.butt_logger

if __name__ == "__main__":
    try:
        os.system("clear")
        print(f"{datetime.now()}: Running {cwd}/main.py")
        butt().run(os.getenv("discord_token"))
    except KeyboardInterrupt:
        logger.butt.exception("Booting got cancelled")
        print(f"\n{datetime.now()}: Booting got cancelled")
        butt().close()
    finally:
        logger.butt.log(50, "Closed all running loops")
        print(f"\n{datetime.now()}: Closed all running loops")
