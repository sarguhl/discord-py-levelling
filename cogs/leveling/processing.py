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
from service.database_queries import queries



class Processing():
    def return_bar(total, xp):
        value = xp
        total = total
        progress = int(value/total * 100)
        bar_length = 10
        filled_length = int(bar_length * progress // 100)
        bar = '🟩' * filled_length + '⬛' * (bar_length - filled_length)
        return bar, progress, value, total

    def fetch_xp(guild_id, member_id):
        db = get_db()
        db.execute("SELECT Experience, Level, TotalXPRequired FROM exp%s WHERE UserID = %s", (guild_id, member_id)) or (None, None)
        db_loadout = db.fetchall()
        if db_loadout:
            xp = db_loadout[0][0]
            lvl = db_loadout[0][1]
            xp_required = db_loadout[0][2]
            current_level = lvl
            desired_level = current_level + 1 
            current_xp = xp

            xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91)
            xp_of_current_level = 5 / 6 * current_level * (2 * current_level * current_level + 27 * current_level + 91)
            xp_needed = round(xp_to_desired_level - xp_of_current_level - current_xp)
            return [xp, lvl, xp_required, xp_to_desired_level, xp_of_current_level, xp_needed]
        else:
            return None


    async def process_xp(message, guild_id, guild):
        db = get_db()
        member = message.author
        if(bool(re.match('^[a-zA-Z0-9]*$',member.name))==True):
            new_member_name = member.name
        else:
            new_member_name = "!!! ERROR WITH MEMBER NAME !!!"

        if member.avatar == None:
            member_url = "https://external-preview.redd.it/4PE-nlL_PdMD5PrFNLnjurHQ1QKPnCvg368LTDnfM-M.png?auto=webp&s=ff4c3fbc1cce1a1856cff36b5d2a40a6d02cc1c3"
        else:
            member_url = member.avatar.url

        if queries.check_db(guild_id):
            db.execute("SELECT Experience, Level, XPLock, TotalXPRequired FROM exp%s WHERE UserID = %s", (guild_id, message.author.id))
            level_loadout = db.fetchall()
            if level_loadout:
                xp = level_loadout[0][0]
                lvl = level_loadout[0][1]
                xp_lock = level_loadout[0][2]
                total_xp_required = level_loadout[0][3]
            else:
                lvl = 0
                xp_required = 5 / 6 * lvl+1 * (2 * lvl+1 * lvl+1 + 27 * lvl+1 + 91)
                
                db.execute("INSERT INTO exp%s (UserID, TotalXpRequired, XPLock, AvatarUrl, MemberName, Experience, Level) VALUES (%s, %s, %s, %s, %s, 0, 0)", (guild_id, member.id, xp_required, datetime.utcnow(), member_url, new_member_name))
                return
        else:
            statement = "CREATE TABLE IF NOT EXISTS exp%s (UserID VARCHAR(45) PRIMARY KEY, Experience INT(11) DEFAULT 0, Level INT(11) DEFAULT 0, XPLock LONGTEXT, TotalXPRequired INT(11) DEFAULT 0, AvatarUrl LONGTEXT, MemberName LONGTEXT);"
            db.execute(statement, guild_id)
            db.execute("ALTER TABLE exp%s MODIFY MemberName VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;", guild_id)
            for member in guild.members:
                if member.avatar == None:
                    member_url = "https://external-preview.redd.it/4PE-nlL_PdMD5PrFNLnjurHQ1QKPnCvg368LTDnfM-M.png?auto=webp&s=ff4c3fbc1cce1a1856cff36b5d2a40a6d02cc1c3"
                else:
                    member_url = member.avatar.url
                
                lvl = 0
                desired_level = lvl + 1 

                xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91)
                xp_required = xp_to_desired_level
                db.execute("ALTER TABLE exp%s CONVERT TO CHARACTER SET utf8", guild_id)
                db.execute("INSERT INTO exp%s (UserID, TotalXpRequired, XPLock, AvatarUrl, MemberName, Experience, Level) VALUES (%s, %s, %s, %s, %s, 0, 0)", (guild_id, member.id, xp_required, datetime.utcnow(), member_url, member.name))

            db.execute("SELECT Experience, Level, XPLock, TotalXPRequired FROM exp%s WHERE UserID = %s", (guild_id, message.author.id))
            level_loadout = db.fetchall()
            if level_loadout:
                xp = level_loadout[0][0]
                lvl = level_loadout[0][1]
                xp_lock = level_loadout[0][2]
                total_xp_required = level_loadout[0][3]

        if xp_lock is None or datetime.utcnow() > datetime.fromisoformat(str(xp_lock)):
            await Processing.add_xp(message, xp, lvl, guild_id)
    
    async def add_xp(message, xp, lvl, guild_id):
        db = get_db()
        xp_to_add = randint(15, 25)

        desired_level = lvl + 1 

        xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91)

        if xp+xp_to_add >= xp_to_desired_level:
            desired_level += 1
            xp_to_desired_level = 5 / 6 * desired_level * (2 * desired_level * desired_level + 27 * desired_level + 91)
            db.execute("UPDATE exp%s SET Experience = Experience + %s, XPLock = %s, TotalXPRequired = %s, Level = Level + 1 WHERE UserID = %s", (guild_id, xp_to_add, (datetime.utcnow()+timedelta(seconds=60)).isoformat(),xp_to_desired_level, message.author.id))
            
            await message.channel.send(f"Congrats {message.author.name} - you reached level {lvl+1:,}!")
        else:
            db.execute("UPDATE exp%s SET Experience = Experience + %s, XPLock = %s WHERE UserID = %s", (guild_id, xp_to_add, (datetime.utcnow()+timedelta(seconds=60)).isoformat(), message.author.id))

