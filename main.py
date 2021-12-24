import discord
from discord.ext import commands
import os
import io
from dotenv import load_dotenv

load_dotenv() # get secret environment variables

description = "A simple bot for posting cute cat pictures"

bot = commands.Bot(command_prefix = '$', description = description) # create the bot object, commands start with $

@bot.event # register a new event
async def on_ready():
    print('Logged in as user: {0.user}'.format(bot)) # prints on (successful) bot start up

@bot.command(name = "bingus") # create new command, pass 'name' keyword argument into the decorator
async def postImage(ctx):
    await ctx.send(file = discord.File("images/bingus.png"))

bot.run(os.getenv('TOKEN')) # run the bot using the token environment variable