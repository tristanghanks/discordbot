import discord
from datetime import datetime
from discord import Embed
from discord.ext import commands
import json
import os
from .stats_handler import Stats

'''
A cog which handles Events such as a member joining the server,
or leaving the server.
'''

# ? Move the embed functions to embed handler?

class Events(commands.Cog):

    def __init__(self, bot):
        self.bot = bot 
        '''
        While I would love to use the command_embed function in embed_handler.py,
        that is meant for command confirmation, warnings and errors.
        I should still probably move these two embed functions into the embed_handler cog.
        '''
    async def join_embed(self, member):
        embed = Embed(title = f"{member.mention} has joined!",
                    description = f"\nPlease read the rules, and enjoy your time on {member.guild.name}",
                    color = 0x43b581)
        embed.set_thumbnail(url = member.avatar_url)

        return embed
    
    async def lvlup_embed(self, member):
        stat = self.userjson
        embed = Embed(title = f"{member} has leveled up!",
                    color = member.color)
        embed.description = "{}  **{} ⟶ {}**".format(member.mention, stat['lvl'] - 1, stat['lvl'])
        embed.set_thumbnail(url = member.avatar_url)

        return embed

    async def load_user(self, member):  # loads a user's file from their file ID.
        with open(rf'D:\discord\users\{member.id}.json') as userfile:
            self.userjson = json.load(userfile)

    async def save_user(self, member):  # commits changes to the user's file if there are any.
        with open(rf'D:\discord\users\{member.id}.json', 'w') as userfile:
            json.dump(self.userjson, userfile, indent=4)

    @commands.Cog.listener()
    async def on_member_join(self, member):  # upon a user joining, give them a file.
        with open(rf'D:\discord\users\{member.id}.json', 'w') as userfile:
            layout = {
                        "lvl": 0,
                        "xp": 0,
                        "reqxp": 5 * (0 ^ 2) + 50 * 0 + 100,  # exponential algorithm for level-based experience.
                        "creds": 0,
                        "isBoosting": False,
                        "lastmsg": "{:%B %d, %Y, %I:%M %p}".format(datetime.now()),
                        "joinedOn": "{:%B %d, %Y, %I:%M %p}".format(datetime.now())
                     }
            json.dump(layout, userfile, indent=4)
            userfile.close()
        embed = await self.join_embed(member)
        await member.guild.system_channel.send(embed=embed, delete_after=60)  # announcing a new member in the server.


    @commands.Cog.listener()
    async def on_member_remove(self, member):
        os.remove(rf"D:\discord\users\{member.id}.json")  # if a user leaves, delete their file.

    @commands.Cog.listener()
    async def on_message(self, message):
        if not message.author.bot:
            '''
            This is really the meat and potatoes of the bot.
            if multiple users are sending messages in multiple channels,
            we need to add to all of those users' stats, so we use a listener instead of an event.
            '''
            await Stats.addvalues(self, message.author, message.channel)


def setup(bot):
    bot.add_cog(Events(bot))