from discord.ext import commands
import discord
from PIL import Image, ImageDraw, ImageFont
import io
import json

from discord.ext.commands.errors import MemberNotFound

class Stat(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def load_user(self, member):
        with open(rf'D:\discord\users\{member.id}.json') as userfile:
            self.userjson = json.load(userfile)

    async def gen_profile(self, ctx, member):
        await self.load_user(member)
        '''
        First, we load the member's file.  Then, we
        set the length of an XP bar that will be rendered in the future
        the length of the XP bar is XP / REQUIRED * LENGTH OF BASE BAR

        Then we open each asset we need, and convert the member's
        profile picture to an asset
        '''
        stat = self.userjson
        l = (stat['xp'] / stat['reqxp']) * 537
        xp = f"({stat['xp']} / {stat['reqxp']}) XP"
        level = "Lvl. {}".format(stat['lvl'])
        card = Image.open(r"D:\discord\bot\assets\card.png")
        stat_outline = Image.open(rf"D:\discord\bot\assets\statusoutline.png")
        stat = Image.open(rf"D:\discord\bot\assets\{member.status}.png")
        xpbar = Image.open(r"D:\discord\bot\assets\xpbar.png")
        
        avatar = member.avatar_url_as(format='png', size=128)

        av_buffer = io.BytesIO()  # We user buffers because this should be a temporary, non-saved image.
        await avatar.save(av_buffer)
        av_buffer.seek(0)

        avatar = Image.open(av_buffer)

        base = Image.new("RGBA", card.size)  # Creating a base blank canvas for other images to layer onto. Size is based off of the largest asset.

        data = ImageDraw.Draw(card)

        color = str(member.color).lstrip("#")  # Grabbing the member's role color which is in hex form, and we need it in RGB(A) form.
        newcolor = tuple(int(color[i:i+2], 16) for i in (0, 2, 4))
        newercolor = list(newcolor)
        newercolor.append(255)
        newercolor = newercolor
        xpcap = ImageDraw.Draw(xpbar)   # About to draw the current user XP!
        '''
        Here, I'm trying to scale the Member's name so it
        fits an appropriate width within the picture and
        avoids overflowing.
        '''
        text = "{}".format(member)
        fontsize = 1
        font = ImageFont.truetype(r'D:\discord\bot\assets\fonts\Roboto-Regular.ttf', fontsize)

        breakpoint = 400
        jumpsize = 75
        while True:
            if font.getsize(text)[0] < breakpoint:
                fontsize += jumpsize
            else:
                jumpsize = jumpsize // 2
                fontsize -= jumpsize
            font = ImageFont.truetype(r'D:\discord\bot\assets\fonts\Roboto-Regular.ttf', fontsize)
            if jumpsize <= 1:
                break
        
        data.text((178, 40), text, fill=(tuple(newercolor)), font=font)  # Drawing the name!
        font = ImageFont.truetype(r'D:\discord\bot\assets\fonts\Roboto-Regular.ttf', 24)
        

        data.text((20, 185), xp, fill=(255,255,255,255), font=font)
        data.text((280, 185), level, fill=(255,255,255,255), font=font)  # Drawing a text version of the current XP for readability.
        '''
        Here, we combine each layer in their respective positions.
        Images with alpha channels are designated to use their own
        alpha channels so everything looks smooth.
        '''
        base.paste(card)
        base.paste(avatar, (30, 30))
        base.paste(stat_outline, (138,138), stat_outline)
        base.paste(stat, (148,148), stat)
        #height = 25
        #width = 537
        
        xpcap.rectangle([0, 0, l, 25], fill=(tuple(newercolor)))  # Drawing the XP bar!

        base.paste(xpbar, (30, 228))

        if member.premium_since is not None:  # If a member has contributed monetarily, give them a neat icon.
            boosted = Image.open(r"D:\discord\bot\assets\booster.png")
            base.paste(boosted, (470, 198), boosted)

        buffer = io.BytesIO()  # Buffering the image

        base.save(buffer, format='PNG')

        buffer.seek(0)

        await ctx.send(file=discord.File(buffer, 'card.png'))  # Finally, putting it all together.

    @commands.command()
    async def rank(self, ctx, member: discord.Member = None):  # This is the command which calls all of that!
        if member is None:
            member = ctx.author
        elif member.bot:
            raise MemberNotFound(member)
        await self.gen_profile(ctx, member)

        

def setup(bot):
    bot.add_cog(Stat(bot))