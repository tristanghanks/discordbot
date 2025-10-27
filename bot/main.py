import discord
from discord import errors
from discord.ext import commands
from discord.ext.commands import errors
import os

intents = discord.Intents.all()  # allows the bot client to access all "intents" that would normally be restricted.

client = commands.Bot(command_prefix = ';', intents = intents, case_insensitive=True)  # initializing the bot as "client"

print("\n[BOT] Readying up....\n")
'''
Each @client.listen is a "listener" for a @client.event, so that they can run asynchronously.
Normally, only one event is able to run at a time, and we'll see why this is not optimal later.
'''
@client.listen('on_connect')
async def on_connect():
    print("[BOT] Connected to Discord. {}ms\n".format(int(client.latency*1000)))

@client.listen('on_disconnect')
async def ondisconnect():
    print("[BOT] Disconnected from Discord.\n")

@client.listen('on_ready')  # When the bot has finished initializing.
async def onready():
    print("[BOT] Ready.\n")

@client.listen('on_resumed')
async def onresumed():
    print("[BOT] Resumed session.\n")

@client.listen('on_message')  
async def onmessage(message):
    print("[{}] {}".format(message.author, message.content))

for cog in os.listdir("D:/discord/bot/cogs"):
    '''
    Calling Cogs from the cogs folder. Cogs are a form of imports,
    But can run in modularity.  i.e, I can load a cog into the client
    session if I decide to create a new one while the bot is running,
    or make edits and update the session live without any downtime.
    '''
    try:
        if cog.endswith(".py"):
            client.load_extension(f"cogs.{cog[:-3]}")
            print("[BOT] Cog {} loaded\n".format(cog))

    except errors.ExtensionNotFound:
        print("[BOT] Failed to load Cog {}\n".format(cog))

'''
The client needs to call home to the discord AUTH so it can
actually run.
'''




client.run("TOKEN", reconnect=True)