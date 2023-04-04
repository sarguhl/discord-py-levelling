import discord

from db.db import get_db

class Commands():
    def check_enabled(guild_id, command_name):
        db = get_db()
        db.execute("SELECT enabled FROM commands WHERE guildId = %s AND commandName = %s", (guild_id, command_name))
        result = db.fetchone()
        return True if result[0] == 1 else False

class Guild():
    def get_member_count(guild_id):
        return

class Level():
    def get_member_xp(guild_id, member_id):
        return
    
    def get_member_level(guild_id, member_id):
        return

    def get_member_level_xp(guild_id, mnember_id):
        return

    def get_member_name(guild_id, member_id):
        db = get_db()
        db.execute("SELECT MemberName FROM exp%s WHERE UserId = %s", (guild_id, member_id))
        member_name = db.fetchall()
        return member_name[0][0] if member_name is not None else None
    
    def get_rank(guild_id, member_id):
        db = get_db()
        db.execute("SELECT UserId FROM exp%s ORDER BY Experience DESC LIMIT 200", guild_id)
        ranks = db.fetchall()
        rank_position = 1
        for rank in ranks:
            if int(rank[0]) == member_id:
                if ranks[rank_position]:
                    followed_place = ranks[rank_position]
                    return rank_position, followed_place
                else:
                    return rank_position
            else:
                rank_position += 1
        
        return 0
