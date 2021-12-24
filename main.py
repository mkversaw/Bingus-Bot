import discord
from discord.ext import commands
import os
import io
import random
from dotenv import load_dotenv

load_dotenv() # get secret environment variables

description = "A simple bot for posting cute cat pictures"
fileList = os.listdir("images/") # use listdir to get list of image names

intents = discord.Intents.all() # enable (all) privileged gateway intents

bot = commands.Bot(intents = intents, command_prefix = '$bingus ', description = description) # create the bot object, commands start with $

@bot.event # register a new event
async def on_ready():
	print('Logged in as user: {0.user}'.format(bot)) # prints on (successful) bot start up

# ? display a random picture of bingus
@bot.command(name = "bingus") # create new command, pass 'name' keyword argument into the decorator
async def postImage(ctx):
	fileNameChoice = "images/" + random.choice(fileList) # get a random file name from list
	await ctx.send(file = discord.File(fileNameChoice))


# ? display the songs a user is listening, or every user if no input param is received
@bot.command(name = "listening")
async def listen(ctx, user: discord.Member = None):
	print("calling listen")
	foundResult = False
	if not user: # everybody in guild
		guild = ctx.guild # get the specific guild command is being called from
		memberList = guild.members # get list of that guild's channel members
		for member in memberList: # iterate through members
			for activity in member.activities: # iterate through each members activities
				if isinstance(activity, discord.Spotify):
					foundResult = True
					embed = discord.Embed(description = "Listening to *{}* ".format(activity.title), color = activity.color)
					embed.set_thumbnail(url = activity.album_cover_url)
					#embed.set_image(url = activity.album_cover_url)
					embed.set_author(name = f"{member.name}'s Spotify", icon_url = member.avatar_url)
					embed.add_field(name = "Artist", value = activity.artist)
					embed.add_field(name = "Album", value = activity.album)
					embed.set_footer(text = "*Song started at {} UTC*".format(activity.created_at.strftime("%H:%M")))
					await ctx.send(embed = embed)
	else: # get spotify activity for specific user
		for activity in user.activities: # iterate through the given users activities
			if isinstance(activity, discord.Spotify):
					foundResult = True
					embed = discord.Embed(description = "Listening to *{}* ".format(activity.title), color = activity.color)
					embed.set_image(url = activity.album_cover_url)
					embed.set_author(name = f"{user.name}'s Spotify", icon_url = user.avatar_url)
					embed.add_field(name = "Artist", value = activity.artist)
					embed.add_field(name = "Album", value = activity.album)
					embed.set_footer(text = "*Song started at {} UTC*".format(activity.created_at.strftime("%H:%M")))
					await ctx.send(embed = embed)
	if(not foundResult): # no results found
		embed = discord.Embed(title = "Couldn't find anyone listening to music :(")
		embed.set_image(url = "https://c.tenor.com/BCqVPaQdwBsAAAAC/bingus-binguscord.gif") # error image
		await ctx.send(embed = embed)

bot.run(os.getenv('TOKEN')) # run the bot using the token environment variable