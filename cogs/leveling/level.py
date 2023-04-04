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
from discord.utils import get
from service.database_requests import requests
from service.database_queries import queries
from utility.messages import Messages

import re
import sys
from .processing import Processing
from .commands import LevelCommands
print(sys.setrecursionlimit(2000))

class Exp(Cog):
    def __init__(self, bot):
        self.bot = bot

    
    @app_commands.command(name="rank")
    async def display_rank(self, interaction: discord.Interaction, target: Optional[Member]):
        """Display rank on the server."""
        if requests.Commands.check_enabled(interaction.guild.id, "1"):
            target = target or interaction.user

            if queries.check_db(interaction.guild.id):

                member_level, followed_rank = requests.Level.get_rank(interaction.guild.id, target.id)

                if member_level and member_level > 0:
                    followed_member_name = requests.Level.get_member_name(interaction.guild.id, followed_rank) if followed_rank is not None else "None"

                    embed = discord.Embed(
                        description=f"Your current rank is: **{member_level}**!",
                        color=target.color
                    )
                    embed.set_author(name=f"{target.name}#{target.discriminator}", icon_url=target.avatar.url)
                    embed.add_field(name="Followed by:", value=f"{followed_member_name}") if followed_rank is not None and followed_member_name is not None else None

                    await interaction.response.send_message(embed=embed)

                else:
                    await interaction.response.send_message(embed=Messages.error("Your rank is out of reach (consider that rank 200 is the max)"))
        else: await interaction.response.send(embed=Messages.error("This command has been disabled."))


    @app_commands.command(name="level")
    async def display_level(self, interaction: discord.Interaction, target: Optional[Member]):
        if requests.Commands.check_enabled(interaction.guild.id, "1"):
            target = target or interaction.user
            if queries.check_db(interaction.guild.id):

                member_level = Processing.fetch_xp(interaction.guild.id, target.id)

                if member_level:
                    xp = member_level[0]
                    lvl = member_level[1]
                    xp_required = member_level[2]
                    xp_to_lvl_up = 5 / 6 * (lvl+1) * (2 * (lvl+1) * (lvl+1) + 27 * (lvl+1) + 91)

                    xp_to_desired_level = member_level[3]
                    xp_of_current_level = member_level[4]
                    xp_needed = member_level[5]
                    embed = discord.Embed(
                        #title="Level Display",
                        color=interaction.user.color
                    )

                    bar, progress, value, total = Processing.return_bar(xp_to_desired_level-xp_of_current_level, xp-xp_of_current_level)
                    embed.add_field(name="Level", value=f"```{lvl}```")
                    embed.add_field(name="Progress", value=f"```[{bar}] | {progress}% | {int(value)}/{int(total)} XP```")
                    embed.set_author(name=target.name+target.discriminator, icon_url=target.avatar.url)
                    await interaction.response.send_message(embed=embed)
                
                else:
                    await interaction.response.send_message("No level has been detected yet. Please try again later.")
            else:
                await interaction.response.send_message(embed=Messages.error("Server has no level-setup yet."))
        else: await interaction.response.send_message(embed=Messages.error("This command has been disabled."))


    # @app_commands.command(name="leaderboard")
    # async def leaderboard_command(self, interaction: discord.Interaction):
    #     leaderboard = LevelCommands.leaderboard(interaction.guild.id)

    #     embed = discord.Embed(
    #         title=f"{interaction.guild.name} | Leaderboard",
    #         color=interaction.user.color
    #     )
    #     count = 1
    #     for member in leaderboard:
    #         bar, progress, value, total = Processing.return_bar(member[3], member[4], member[1])

    #         embed.add_field(name=f"{count}. {member[4]}", value=f"```Level: {member[2]} | XP: {member[1]}```\n```[{bar}] | {progress}% | {value}/{total}```", inline=False)
    #         count += 1
    #     await interaction.response.send_message(embed=embed)

    @Cog.listener()
    async def on_message(self, message):
        if not message.author.bot and requests.Commands.check_enabled(message.guild.id, "1"):
            await Processing.process_xp(message, message.guild.id, message.guild)

async def setup(bot: Bot) -> None:
    await bot.add_cog(Exp(bot))