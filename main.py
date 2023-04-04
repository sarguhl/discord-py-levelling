import discord

from config.config import Token
from utility.bot import Bot
from discord.utils import get
from service.database_queries import queries

from utility.messages import Messages


intents = discord.Intents.all()
intents.guild_messages = True
intents.typing = True
intents.members = True
intents.messages = True
intents.message_content = True
intents.guilds = True
intents.guild_messages = True
intents.guild_typing = True

client = Bot("?", intents=intents)

@client.event
async def on_ready():
    client.logger.info(f"Logged in as {client.user.name} ({client.user.id})")
    print(discord.__version__)

    client.remove_command('help')

    meta = client.get_cog("Meta")
    await meta.set()

    guild_created = queries.Guild.create()

    
@client.event
async def on_guild_join(guild):
    queries.Guild.add(guild)
    meta = client.get_cog("Meta")
    await meta.set()

@client.event
async def on_guild_remove(guild):
    meta = client.get_cog("Meta")
    await meta.set()

if __name__ == "__main__":
    client.run(Token.bot())