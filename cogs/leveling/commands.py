from datetime import datetime, timedelta
from random import randint
from typing import Optional
import discord
import textwrap
from discord.ext import commands
from discord import app_commands
from utility.bot import Bot
from typing import List
from utility.functions import getEmojis
from utility.functions import split_message
from multiprocessing import Process

from discord import Member, Embed
from discord.ext.commands import Cog
from discord.ext.commands import CheckFailure
from discord.ext.commands import command, has_permissions
from db.db import get_db
from main import client
import re
import sys

class LevelCommands:
    @staticmethod
    def leaderboard(guild_id):
        if guild_id:
            db = get_db()
            db.execute("SELECT * FROM exp{} ORDER BY Experience DESC LIMIT 5".format(guild_id))
            db_loadout = db.fetchall()
            if db_loadout:
                leaderboard = []
                for user in db_loadout:
                    userId = user[0]
                    xp = user[1]
                    lvl = user[2]
                    xp_required = user[4]
                    user_name = user[6]
                    xp_to_lvl_up = 5 * (lvl ** 2) + (50 * lvl) + 100
                    leaderboard.append([userId, xp, lvl, xp_required, xp_to_lvl_up, user_name])
                return leaderboard
            else:
                return None
        
"""
CURRENTLY IN WORK
IGNORE PLEASE
"""