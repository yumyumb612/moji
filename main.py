import logging
import os
from datetime import datetime
from platform import python_version

import discord
import pymongo
from discord.ext import commands
from dotenv import load_dotenv

import configs.config as config

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "configs/.evn"), override=True)
class butt(commands.AutoShardedBot):
    def __init__(self):
        super().__init__(
            command_prefix= config.default_prefix,
            description= config.description,
            status= discord.Status.dnd,
            activity= discord.Game(
                name= "Vivifying. please wait",
                start= datetime.utcnow(),
                type= discord.ActivityType.unknown
            ),
            allowed_mentions= config.allowed_mentions,
            case_insensitive= True,
            intents= config.intents,
            owner_ids= config.owner_ids,
            strip_after_prefix= True
        )
        
        #   setting som attributes
        self.boot_datetime= datetime.utcnow()
        self.cwd: str= os.path.dirname(__file__)
        self.versions= {
            "bot": "7.0.0 alpha",
            "dpy": f"{discord.__version__} {discord.version_info.releaselevel}",
            "py": python_version()
        }
        self.modules= {
            "all": [],
            "loaded": []
        }

        #   logging
        print(f"{datetime.now()}: setting up logger...")
        # logging.basicConfig(level=logging.INFO)

        logger = logging.getLogger("discord")
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(filename= f"{self.cwd}/logs/discord.log", encoding="utf-8", mode="w")
        handler.setFormatter(logging.Formatter(config.logging_format))
        logger.addHandler(handler)
        print(f"{datetime.now()}: done setting up logger")

        # database
        print(f"{datetime.now()}: connecting to da database...")
        mongodb_client = pymongo.MongoClient(os.getenv("mongodb_connection_string"), serverSelectionTimeoutMS=20000)
        self.db = mongodb_client["mojidb"]
        # self.guild_info = collection(self.db, "guild_info")
        # self.features_data = collection(self.db, "features_data")
        try:
            mongodb_client.server_info()
            print(f"{datetime.now()}: connected to da database")
        except Exception as error:
            print(f"{datetime.now()}: {error}\n")
        
        #   modules
        print(f"{datetime.now()}: loading module(s)...")
        modules_paths = [f"{self.cwd}/modules/cogs", f"{self.cwd}/modules/events"]
        for path in modules_paths:
            for filename in os.listdir(path):
                if filename == "__pycache__":
                    continue
                else:
                    self.modules["all"].append(filename.replace(".py", ""))
                    if filename.endswith('.py') and not filename.startswith("_"):
                        if path == modules_paths[0]:
                            self.load_extension(f"modules.cogs.{filename.replace('.py', '')}")
                        else:
                            self.load_extension(f"modules.events.{filename.replace('.py', '')}")
                    else:
                        continue
        print(f"{datetime.now()}: loaded {len(self.modules['loaded'])}/{len(self.modules['all'])} module(s)")

if __name__ == "__main__":
    try:
        os.system("clear")
        print(f"{os.path.dirname(__file__)}/main.py\n")
        print(f"{datetime.now()}: booting...")
        butt().run(os.getenv("discord_token"))
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        butt().close()
    finally:
        print(f"\n{datetime.now()}: stoped")
