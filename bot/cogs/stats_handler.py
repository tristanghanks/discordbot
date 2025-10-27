from discord.ext import commands
from discord import Embed
import json
import random
import datetime

# ! 5 * (lvl ^ 2) + 50 * lvl + 100

class Stats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_user(self, member):
        with open(rf'D:\discord\users\{member.id}.json') as userfile:
            self.userjson = json.load(userfile)

    async def save_user(self, member):
        with open(rf'D:\discord\users\{member.id}.json', 'w') as userfile:
            json.dump(self.userjson, userfile, indent=4)

    async def addvalues(self, member, channel):
        '''
        THE REAL MEAT AND POTATOES
        --------------------------

        We call this function every. single. message.
        This checks if the current time the message
        is sent, is 60 seconds greater than the 
        time since we last added experience to the user.
        
        If so, we add experience and "credits," and set
        the current time to the user's "lastmsg" time.

        If a user's xp upon that message exceeds the
        user's required experience, we subtract the
        required xp from the current xp and leave the difference.

        Then, we add one level to the user, therefore recaculating
        the new required xp.  Again, this is exponential.

        Once all that happens, we send an embedded message to the
        channel the user's last message was in, announcing that
        they levelled up, what level they were and what level they are. 
        '''
        await self.load_user(member)
        userstat = self.userjson
        if datetime.datetime.now() >= datetime.datetime.strptime(userstat['lastmsg'], '%B %d, %Y, %I:%M %p') + datetime.timedelta(minutes=1):
            userstat['creds'] += random.randint(1, 5)
            userstat['xp'] += random.randint(15,25)
            userstat['lastmsg'] = "{:%B %d, %Y, %I:%M %p}".format(datetime.datetime.now())
        if userstat['xp'] >= userstat['reqxp']:
            userstat['xp'] = userstat['xp'] - userstat['reqxp']
            userstat['lvl'] = userstat['lvl'] + 1
            userstat['reqxp'] = (5 * userstat['lvl'] ** 2 + 50 * userstat['lvl'] + 100)
            embed = await self.lvlup_embed(member)
            await channel.send(embed=embed, delete_after=10)
        await self.save_user(member)



def setup(bot):
    bot.add_cog(Stats(bot))