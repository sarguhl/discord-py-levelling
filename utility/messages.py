import discord

class CreateMessage():
    def create_embed(title=None, description=None, fields=None, color=None, author=None, footer=None, image_url=None):
        embed = discord.Embed(
            title=title if title is not None else None,
            description=description if description is not None else None,
            color=color if color is not None else None
        )
        if fields:
            for name, value, inline in fields:
                embed.add_field(name=name, value=value, inline=inline)
        
        if author:
            embed.set_author(name=author)
        
        if footer:
            embed.set_footer(text=footer)
        
        if image_url:
            embed.set_image(url=image_url)
        
        embed.description += "\n\nThis message was sent from Builder's Hub"

        return embed

class Messages():
    def error(message):
        embed = CreateMessage.create_embed(title="❌ | ERROR", description=message, color=0xe74c3c)
        return embed

    def information(message):
        embed = CreateMessage.create_embed(title="ℹ️ | INFORMATION", description=message, color=3426654)
        return embed

    def success(message):
        embed = CreateMessage.create_embed(title="✅ | SUCCESS", description=message, color=5763719)
        return embed

    def warning(message):
        embed = CreateMessage.create_embed(title="⚠️ | WARNING ", description=message, color=16776960)
        return embed

    def notification(message):
        embed = CreateMessage.create_embed(title="📥 | Inbox ", description=message, color=11027200)
        
        return embed