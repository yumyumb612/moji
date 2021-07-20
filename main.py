import logging
import os
from datetime import datetime
from platform import python_version

import discord
import pymongo
from discord.ext.commands import AutoShardedBot
# from discord_components import DiscordComponents
from discord_slash import SlashCommand
from dotenv import load_dotenv

import configs.settings as settings
import helpers.functions.loggers as logger
import helpers.functions.tools as tool
from helpers.database.mongodb import collection

cwd= tool.get_path()
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
        #   attributes
        self.boot_datetime= datetime.utcnow()
        self.start_datatime= start_datatime
        self.cwd: str= cwd
        self.mood= "cheeky"
        self.colours= settings.colours
        self.completed_commands, self.ran_commands, self.command_errors, self.moji_errors= 0, 0, 0, 0
        self.ignored_users, self.recent_users= [], []
        self.versions= {
            "bot": settings.bot_version,
            "dpy": f"{discord.__version__} {discord.version_info.releaselevel}",
            "py": python_version()
        }
        self.moji_cogs= {
            "all": [],
            "loaded": [],
            "commands": [],
            "listeners": []
        }

        #   interactions
        SlashCommand(self, sync_commands=True, sync_on_cog_reload=True, override_type=True)
        # DiscordComponents(self)

        #   logging
        print(f"{datetime.now()}: Setting up logger...")
        # logging.basicConfig(level=logging.INFO)

        discord_logger= logging.getLogger("discord")
        discord_logger.setLevel(logging.INFO)
        discord_handler= logging.FileHandler(filename= f"{self.cwd}/logs/discord.log", encoding= "utf-8", mode= "w")
        discord_handler.setFormatter(logging.Formatter(settings.logging_format))
        discord_logger.addHandler(discord_handler)

        self.butt_logger= logger.butt
        self.event_logger= logger.event
        self.command_logger= logger.command

        self.butt_logger.log(20, "[Started logging]")
        print(f"{datetime.now()}: Done setting logger")

        # database
        print(f"{datetime.now()}: Connecting to MongoDB database...")
        try:
            mongodb_client= pymongo.MongoClient(os.getenv("mongodb_connection_string"), serverSelectionTimeoutMS=20000)
            self.db= mongodb_client["testdb"]
            self.local_settings= collection(self.db, "local_settings")
            self.local_function_settings= collection(self.db, "local_function_settings")

            # mongodb_client.server_info()
            database= mongodb_client.list_database_names()
            print(f"{datetime.now()}: Connected to the database. Found {len(database)}")
            self.butt_logger.log(20, f"[Connected to MongoDB database] Databases: {database}")
        except Exception as error:
            print(f"{datetime.now()}: {error}\n")
            self.butt_logger.log(40, f"[MongoDB Error] {error}")

        #   cogs
        print(f"{datetime.now()}: Loading cog(s)...")
        cog_paths= [f"{self.cwd}/cogs/commands", f"{self.cwd}/cogs/listeners"]
        def load_check(filename):
            return filename.endswith('.py') and not filename.startswith("_")

        self.load_extension("helpers.managers.cog_manager")

        for path in cog_paths:
            for filename in os.listdir(path):
                if filename == "__pycache__":
                    continue
                else:
                    self.moji_cogs["all"].append(filename.replace(".py", ""))
                    if path == cog_paths[0]:
                        self.moji_cogs["commands"].append(filename.replace(".py", ""))
                        if load_check(filename):
                            self.load_extension(f"cogs.commands.{filename.replace('.py', '')}")
                        else:
                            continue
                    else:
                        self.moji_cogs["listeners"].append(filename.replace(".py", ""))
                        if load_check(filename):
                            self.load_extension(f"cogs.listeners.{filename.replace('.py', '')}")
                        else:
                            continue
        print(f"{datetime.now()}: Loaded {len(self.moji_cogs['loaded'])}/{len(self.moji_cogs['all'])} cog(s)")
        self.butt_logger.log(20, f"[Cog] All: `{len(self.moji_cogs['all'])}` Loaded: `{len(self.moji_cogs['loaded'])}` Commands: `{len(self.moji_cogs['commands'])}` Listeners: `{len(self.moji_cogs['listeners'])}`")

if __name__ == "__main__":
    try:
        os.system("clear")
        logger.butt.log(20, "[Script] Started running 'main.py'")
        print(f"{datetime.now()}: Running {cwd}/main.py")
        start_datatime= datetime.utcnow()
        butt().run(os.getenv("discord_token"))
    except KeyboardInterrupt:
        logger.butt.log(40, "[Script] KeyboardInterrupt")
        print(f"\n{datetime.now()}: Booting got cancelled")
        butt().close()
    except discord.errors.LoginFailure:
        print(f"\n{datetime.now()}: Improper token has been passed")
    finally:
        logger.butt.log(50, "[Script] Stoped running 'main.py'")
        print(f"\n{datetime.now()}: Closed all the loops. Client offline")
