import datetime
import discord

from db.db import get_db

def check_db(db_name):
    db = get_db()
    db.execute("SHOW TABLES LIKE 'exp%s'", db_name)
    result = db.fetchone()
    return True if result else False

def check__for_db(db_name):
    db = get_db()
    db.execute("SHOW TABLES LIKE %s", db_name)
    result = db.fetchone()
    return True if result else False

class Guild():
    def add(guild: discord.Guild):
        db = get_db()
        db.execute("INSERT IGNORE INTO guilds (GuildID, GuildName, GuildMemberCount, GuildAvatarUrl) VALUES (%s, %s, %s, %s)", (guild.id, guild.name, guild.member_count, guild.icon.url))
    
    def remove(guild_id):
        db = get_db()
        db.execute("DELETE FROM guilds WHERE GuildID = %s", guild_id)

    def update(guild: discord.Guild):
        db = get_db()
        db.execute("SELECT * FROM guilds WHERE GuildID = %s", guild.id)
        guild_exists = db.fetchall()
        if not guild_exists:
            db.execute("INSERT IGNORE INTO guilds (GuildID, GuildName, GuildMemberCount, GuildAvatarUrl) VALUES (%s, %s, %s, %s)", (guild.id, guild.name, guild.member_count, guild.icon.url))
        else:
            db.execute("UPDATE guilds SET GuildName = %s, GuildMemberCount = %s, GuildAvatarUrl = %s WHERE GuildID = %s", (guild.name, guild.member_count, guild.icon.url, guild.id))
    
    def create():
        if not check__for_db("guilds"):
            db = get_db()
            statement = "CREATE TABLE IF NOT EXISTS guilds (GuildID BIGINT(11) PRIMARY KEY, GuildName LONGTEXT, GuildMemberCount LONGTEXT, GuildAvatarUrl LONGTEXT);"
            db.execute(statement)
            db.execute("ALTER TABLE guilds MODIFY GuildName VARCHAR(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci NOT NULL;")
            return "CREATED TABLE: guilds"
        else:
            return "Guild-Table already created."

class Level():
    def update_avatar_url(guild_id, member_id, avatar_url):
        db = get_db()
        db.execute("UPDATE exp%s SET AvatarUrl = %s WHERE UserID = %s", (guild_id, str(avatar_url), member_id))