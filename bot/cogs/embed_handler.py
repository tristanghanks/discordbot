from discord import Embed
from discord.ext import commands
'''
A short cog which other cogs can .import for embed functionality.
Just here for QOL so other files are less messy.  They get really
messy...
'''
async def command_embed(message: None, emoji: None, color: None):
    embed = Embed(
                title="{}  {}".format(emoji, message),
                color=color )
    return embed

class EmbedHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(EmbedHandler(bot))
