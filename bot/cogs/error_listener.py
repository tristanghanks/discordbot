import discord
import traceback
from discord import Colour
import sys
from discord.ext import commands
from .embed_handler import command_embed

error_emoji = ":x:"
warning_emoji = ":warning:"
confirmed_emoji = ":white_check_mark:"
error_color = 0xef4646
warning_color = 0xf9a61a
confirmed_color = 0x43b581

class ErrorListener(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        '''
        This is a cog built entirely to address any
        non-automatic errors and deliver one to the
        user if they fail to meet certain criteria.
        '''
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            embed = await command_embed("This command needs more arguments.", warning_emoji, warning_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.ArgumentParsingError):
            embed = await command_embed("Error Code 0.  Please let the the server owner know.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.PrivateMessageOnly):
            embed = await command_embed("This command only works in my DMs.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.NoPrivateMessage):
            embed = await command_embed("This command does not work in DMs.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.CheckFailure):
            embed = await command_embed("You don't have any priveleges for this command.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        #elif isinstance(error, commands.CheckAnyFailure):
        #    embed = await command_embed("You don't have all of the priveleges for this command.", error_emoji, error_color)
        #    await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.CommandNotFound):
            embed = await command_embed("This command doesn't exist.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.DisabledCommand):
            embed = await command_embed("This command has been disabled.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        #elif isinstance(error, commands.CommandInvokeError):
        #    embed = await command_embed("Error Code 1.  Please let the the server owner know.", error_emoji, error_color)
        #    await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.TooManyArguments):
            embed = await command_embed("You've given too many arguments.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.CommandOnCooldown):
            embed = await command_embed("This command is on cooldown.  Try again later.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.NotOwner):
            embed = await command_embed("You probably shouldn't.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.MemberNotFound):
            embed = await command_embed("I can't find that member.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.UserNotFound):
            embed = await command_embed("I can't find that user.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.ExtensionAlreadyLoaded):
            embed = await command_embed("That extension has already been loaded.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.ExtensionNotLoaded):
            embed = await command_embed("That extension was not loaded.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.NoEntryPointError):
            embed = await command_embed("That extension doesn't have a setup function.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.ExtensionNotFound):
            embed = await command_embed("I couldn't find an extension with that name.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.CommandRegistrationError):
            embed = await command_embed("This command can't work because more than one have the same name.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        elif isinstance(error, commands.BadArgument):
            embed = await command_embed("Please make sure you use the right type of argument.", error_emoji, error_color)
            await ctx.send(embed = embed, delete_after = 10)

        else:
            # All other Errors not returned come here. And we can just print the default TraceBack.
            print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
            traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)

def setup(bot):
    bot.add_cog(ErrorListener(bot))
