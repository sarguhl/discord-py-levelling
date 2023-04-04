from db.db import get_db

class LevelMod():
    async def reset_xp(self, user_id, guild_id):
        db = get_db()
        db.execute("UPDATE exp%s SET Experience = %s, Level = %s WHERE UserID = %s", (guild_id, 0, 0, user_id))

    async def delete_xp(self, user_id, guild_id, amount):
        db = get_db()
        db.execute("SELECT Experience, Level FROM exp%s WHERE UserID = %s", (guild_id, user_id))
        level_loadout = db.fetchall()
        xp = level_loadout[0][0]
        lvl = level_loadout[0][1]
        await self.del_mod_xp(user_id, xp, lvl, guild_id, amount)

    async def del_mod_xp(self, user_id, xp, lvl, guild_id, amount):
        db = get_db()
        xp_to_delete = amount
        new_lvl = int(((xp+xp_to_delete)//42) ** 0.55)
        db.execute("UPDATE exp%s SET Experience = Experience - %s, Level = LEVEL - %s WHERE UserID = %s", (guild_id, xp_to_delete, new_lvl, user_id))

    async def give_xp(self, user_id, guild_id, amount):
        db = get_db()
        db.execute("SELECT Experience, Level FROM exp%s WHERE UserID = %s", (guild_id, user_id))
        level_loadout = db.fetchall()
        xp = level_loadout[0][0]
        lvl = level_loadout[0][1]
        await self.add_mod_xp(user_id, xp, lvl, guild_id, amount)

    async def add_mod_xp(self, user_id, xp, lvl, guild_id, amount):
        db = get_db()
        xp_to_add = amount
        new_lvl = int(((xp+xp_to_add)//42) ** 0.55)
        db.execute("UPDATE exp%s SET Experience = Experience + %s, Level = LEVEL + %s WHERE UserID = %s", (guild_id, xp_to_add, new_lvl, user_id))