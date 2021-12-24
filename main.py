import discord
from discord.ext import commands
import os
import io
import random
from dotenv import load_dotenv

load_dotenv() # get secret environment variables

description = "A simple bot for posting cute cat pictures"
fileList = os.listdir("images/") # use listdir to get list of image names

bot = commands.Bot(command_prefix = '$', description = description) # create the bot object, commands start with $

@bot.event # register a new event
async def on_ready():
	print('Logged in as user: {0.user}'.format(bot)) # prints on (successful) bot start up

@bot.command(name = "bingus") # create new command, pass 'name' keyword argument into the decorator
async def postImage(ctx):
	fileNameChoice = "images/" + random.choice(fileList) # get a random file name from list
	await ctx.send(file = discord.File(fileNameChoice))

bot.run(os.getenv('TOKEN')) # run the bot using the token environment variable