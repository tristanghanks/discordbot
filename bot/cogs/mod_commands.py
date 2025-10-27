import discord
from discord.ext import commands
import asyncio
from .embed_handler import command_embed
import discord.utils

error_emoji = ":x:"
warning_emoji = ":warning:"
confirmed_emoji = ":white_check_mark:"
error_color = 0xef4646
warning_color = 0xf9a61a
confirmed_color = 0x43b581

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    '''
    The moderation cog.  This is where we designate commands
    based on permissions and command_embed is called a lot.
    '''

    @commands.command(help="deletes a specified amount of messages from the channel it is called in",
                      brief="deletes messages",
                      usage="[number] || defaults to 10",
                      aliases=["delete", "purge", "remove", "clean"])
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amt: int = 10):
        embed = await command_embed("Deleting {} messages, this may take a moment.".format(amt),
                                    warning_emoji,
                                    warning_color)
        await ctx.send(embed=embed, delete_after=5)
        if amt > 100:
            await asyncio.sleep(5)
        deleted = await ctx.channel.purge(limit=amt + 2)
        embed = await command_embed("Deleted {} messages.".format(len(deleted) - 2),
                                    confirmed_emoji,
                                    confirmed_color)
        await ctx.send(embed=embed, delete_after=5)


    @commands.command(help="kicks a member from the server",
                        brief="kicks a member",
                        usage="<member> [reason]")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = 'an undefined reason.'):
        embed = await command_embed("Kicked {} for {}".format(member, reason),
                                    confirmed_emoji,
                                    confirmed_color)
        await ctx.author.guild.kick(member, reason="{} kicked {} for {}".format(ctx.author, member, reason))
        await ctx.send(embed=embed, delete_after=10)


    @commands.command(help="bans a member from the server",
                        brief="bans a member",
                        usage="<member> [reason]")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = 'an undefined reason.'):
        embed = await command_embed("Banned {} for {}".format(member, reason),
                                    confirmed_emoji,
                                    confirmed_color)
        await ctx.author.guild.ban(member, reason="{} banned {} for {}".format(ctx.author, member, reason), delete_message_days=7)
        await ctx.send(embed=embed, delete_after=10)


    @commands.command(help="unbans a user from the server",
                        brief="unbans a user",
                        usage="<user> [reason]")
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.User, *, reason: str = 'an undefined reason.'):
        embed = await command_embed("Unbanned {} for {}".format(member, reason),
                                    confirmed_emoji,
                                    confirmed_color)
        await ctx.author.guild.unban(member, reason="{} unbanned {} for {}".format(ctx.author, member, reason))
        await ctx.send(embed=embed, delete_after=10)


    @commands.command(help="prevents a member from sending messages or speaking",
                        brief="mutes a member",
                        usage="<member> [reason]")
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason: str = 'an undefined reason.'):
        embed = await command_embed("Muted {} for {}".format(member, reason),
                                    confirmed_emoji,
                                    confirmed_color)
        if not discord.utils.get(ctx.guild.roles, name = "MUTED"):
            await ctx.guild.create_role(name="MUTED",
                                        permissions=discord.Permissions(send_messages=False, speak=False),
                                        color=discord.Colour(error_color),
                                        reason="Role did not exist.")
            for channel in ctx.guild.channels:
                await channel.set_permissions(discord.utils.get(ctx.guild.roles, name = "MUTED"), send_messages=False, speak=False)
        await member.add_roles(discord.utils.get(ctx.guild.roles, name = "MUTED"), reason="{} muted {} for {}".format(ctx.author, member, reason))
        await ctx.send(embed=embed, delete_after=10)

    
    @commands.command(help="unmutes a member",
                        brief="unmutes a member",
                        usage="<member> [reason]")
    @commands.has_permissions(manage_messages=True)    
    async def unmute(self, ctx, member: discord.Member, *, reason: str = 'an undefined reason.'):
        embed = await command_embed("Unmuted {} for {}".format(member, reason),
                                    confirmed_emoji,
                                    confirmed_color)
        await member.remove_roles(discord.utils.get(ctx.guild.roles, name = "MUTED"), reason="{} unmuted {} for {}".format(ctx.author, member, reason))
        await ctx.send(embed=embed, delete_after=10)
 
    
def setup(bot):
    bot.add_cog(Mod(bot))