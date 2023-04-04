import discord
import textwrap
import datetime
from discord.ext import commands
from discord import Button, ButtonStyle, app_commands
from utility.bot import Bot
from typing import List
from utility.functions import getEmojis
from utility.functions import split_message
from multiprocessing import Process
from discord import ui
from utility.messages import Messages
from ast import literal_eval
from db.db import get_db
from service.database_queries import queries
from service.database_requests import requests
from time import sleep
import json

class Commands(commands.Cog):
    def __init__(self, bot: Bot) -> None:
        self.bot = bot
        self.cached_emojis: dict[int, dict[list, datetime.datetime]] = {}

    @app_commands.command()
    async def say(self, interaction: discord.Interaction, text: str):
        """Say something"""
        await interaction.response.send_message("text sent", ephemeral=True)
        await interaction.channel.send(text)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Commands(bot))