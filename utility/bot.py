import asyncio
import datetime
import time
import traceback
import logging


from service.database_queries import queries
import discord
from discord import app_commands
from discord.ext import commands
from config.config import ClientData
from db.db import get_db
from utility.messages import Messages

class Bot(commands.Bot):
    def __init__(self, command_prefix: str, intents: discord.Intents) -> None:
        super().__init__(
            command_prefix,
            intents=intents,
            allowed_mentions=discord.AllowedMentions(
                everyone=False, users=True, roles=False, replied_user=True
            ),
            application_id=ClientData.client_id(),
        )
        

        self._launch_date: int = round(time.time())

        logger = logging.getLogger("bot")
        logger.setLevel(logging.DEBUG)

        formatter = logging.Formatter(r"[%(name)s] %(message)s")

        file_handler = logging.FileHandler(
            filename="logs/bot.log", encoding="utf-8", mode="w+"
        )
        file_handler.setFormatter(formatter)

        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.addHandler(stream_handler)

        self.logger = logger

        self.required_permissions = discord.Permissions(8)
    
    @property
    def support_server(self) -> discord.Guild:
        raise NotImplementedError

    @property
    def support_invite(self) -> discord.Invite:
        raise NotImplementedError

    @property
    def launch_date(self) -> datetime.datetime:
        return datetime.datetime.fromtimestamp(self._launch_date, datetime.timezone.utc)

    def invite_url(
        self, guild_id: int = None, disable_guild_select: bool = False
    ) -> str:
        return discord.utils.oauth_url(
            self.application_id,
            permissions=self.required_permissions,
            guild=discord.Object(
                guild_id) if guild_id else discord.abc.MISSING,
            disable_guild_select=disable_guild_select,
        )

    async def setup_hook(self):

        extensions = ["cogs.leveling.level", "cogs.service_commands"]

        for cog in extensions:
            try:
                await self.load_extension(cog)
                self.logger.info(f"Loaded extension {cog}")
            except Exception:
                self.logger.error(
                    f"Failed to load extension {cog}:\n{traceback.format_exc()}"
                )
                
        sycned = await self.tree.sync()

        slash_commands = "\n".join(
            ["      /" + c.name for c in sycned if c.type is discord.AppCommandType.chat_input])
        user_context_menu = "\n".join(
            ["      " + c.name for c in sycned if c.type is discord.AppCommandType.user])
        message_context_menu = "\n".join(
            ["      " + c.name for c in sycned if c.type is discord.AppCommandType.message])

        if slash_commands:
            self.logger.debug(
                f"Slashcommands synced globally:\n{slash_commands}")
        if user_context_menu:
            self.logger.debug(
                f"Usercommands synced globally:\n{user_context_menu}")
        if message_context_menu:
            self.logger.debug(
                f"Messagecommands synced globally:\n{message_context_menu}")
        