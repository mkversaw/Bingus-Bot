import discord
from discord.ext import commands
import os
import io
import random
import json
from dotenv import load_dotenv

load_dotenv() # get secret environment variables

description = "A simple bot for posting cute cat pictures"

bingusFileList = os.listdir("images/bingus") # use listdir to get list of image names for the bingus directory
floppaFileList = os.listdir("images/floppa") # use listdir to get list of image names for the floppa directory

intents = discord.Intents.all() # enable (all) privileged gateway intents
bot = commands.Bot(intents = intents, command_prefix = '$bingus ', description = description) # create the bot object, commands start with '$bingus '


# ? ensure that bot starts up
@bot.event # register a new event
async def on_ready():
	if not os.path.exists("levels.json"): # * if levels File does note exist, create it and fill it with '{}'
		print("levels.json not found, creating it...")
		with open("levels.json", "w") as levelsFile:
			levelsFile.write("{}")
		levelsFile.close()
	print('Logged in as user: {0.user}'.format(bot)) # prints on (successful) bot start up

# ? whenever a non-bot user sends a message
bot.experienceToAdd = 2
@bot.event
async def on_message(message):
	if not message.author.bot: # don't count messages from the bot
		with open("levels.json", "r") as levelsFile:
			userJSON = json.load(levelsFile)
		await checkNewUser(userJSON, message.author,message.guild)
		await updateExperience(userJSON, message.author, bot.experienceToAdd, message.guild)
		await updateLevel(userJSON, message.author,message.channel, message.guild)

		with open("levels.json","w") as levelsFile:
			json.dump(userJSON, levelsFile)

		if message.author.id == 163753207405871104: # id of user to react to
			await message.add_reaction("🤓") # reaction emoji
	await bot.process_commands(message)

# ? check if user and/or server exist in json file, if not update the file accordingly
async def checkNewUser(data, user, server): 
	userID = str(user.id) # cast to string for usage with JSON
	serverID = str(server.id)
	if not serverID in data: # if no data exists for current server
		data[serverID] = {} # make new empty json object for holding data for that server
		if not userID in data[serverID]: # if no data exists for user for current server
			data[serverID][userID] = {} # make new empty json object for holding data for that user
			data[serverID][userID]["experience"] = 0 # set the user's initial exp and lvl to 0
			data[serverID][userID]["level"] = 1
	elif not userID in data[serverID]: # if data exists for current server, but none for current user
		data[serverID][userID] = {} # make new empty json object for holding data for that user
		data[serverID][userID]["experience"] = 0 # set the user's initial exp and lvl to 0
		data[serverID][userID]["level"] = 1

# ? add experience to some user for some server
async def updateExperience(data, user, exp, server):
	data[str(user.guild.id)][str(user.id)]["experience"] += exp # add the experience

# ? check if user has enough experience to level up
async def updateLevel(users, user, channel, server):
	userID = str(user.id) # cast to string for usage with JSON
	serverID = str(server.id)

	experience = users[serverID][userID]['experience']
	lvlStart = users[serverID][userID]['level']
	lvlEnd = int(experience ** (0.25)) # what experience level user needs to reach to level up

	if lvlStart < lvlEnd:
		embed = discord.Embed(title = 'Comrade {} is now level {}!'.format(user.name, lvlEnd) , color = discord.Color.red())
		embed.set_author(name = user.name, icon_url = user.avatar_url)
		embed.set_footer(text = "Glory to Bingustan")
		embed.set_thumbnail(url = user.avatar_url)
		await channel.send(embed = embed)
		
		users[serverID][userID]["level"] = lvlEnd

@bot.command(aliases = ["rank","lvl","credit","socialcredit"], brief = "Check exp", description = "Check how much experience you, or another user has")
async def level(ctx,member: discord.Member = None):
	if not member: # get the user who called the command's data
		user = ctx.message.author
	else: # otherwise, get the data for the specified user
		user = member

	userID = str(user.id) # cast to string for usage with JSON
	serverID = str(ctx.guild.id)
	

	with open("levels.json","r") as levelsFile:
		userJSON = json.load(levelsFile)
	level = userJSON[serverID][userID]["level"]
	experience = userJSON[serverID][userID]['experience']
	expToNextLevel = ( (level + 1)**4 ) - experience # calculate remaining exp to level up
	embed = discord.Embed(title = 'Citizen Level {}'.format(level), description = f"{experience} Social Credit Points " ,color = discord.Color.red())
	embed.set_author(name = user.name, icon_url = user.avatar_url)
	embed.add_field(name = "Points to next level", value = str(expToNextLevel) + " 元")
	embed.set_footer(text = "Glory to Bingustan")
	file = discord.File("./images/bingusflag.jpg", filename = "image.png") # FILENAME MUST BE IMAGE.PNG
	embed.set_thumbnail(url = "attachment://image.png")
	await ctx.reply(file = file , embed = embed)

@level.error
async def levelError(ctx, error):
	if isinstance(error, commands.errors.MemberNotFound):
		if(error.argument == "@everyone" or error.argument == "@here"):
			guild = ctx.guild # get the specific guild command is being called from
			memberList = guild.members # get list of that guild's channel members
			for member in memberList: # iterate through members
				if(member != bot.user):
					await level(ctx,member)
		else:
			await ctx.reply(":x: No user found :(")

# ? display a random picture of bingus
bot.lastRolledBingus = None
@bot.command(name = "bingus", brief = "Posts a bingus") # create new command, pass 'name' keyword argument into the decorator
async def postImage(ctx):
	if(bot.lastRolledBingus == None): # no previous image of bingus rolled
		fileNameChoice = "images/bingus/" + random.choice(bingusFileList) # get a random file name from list
		bot.lastRolledFloppa = fileNameChoice # update previous image holder var
	else:
		fileNameChoice = "images/bingus/" + random.choice(bingusFileList) # get a random file name from list
		while(fileNameChoice == bot.lastRolledFloppa): # roll until no repeat (shouldn't take long)
			fileNameChoice = "images/bingus/" + random.choice(bingusFileList) # get a random file name from list
			bot.lastRolledFloppa = fileNameChoice # update previous image holder var
	await ctx.reply(file = discord.File(fileNameChoice)) # post the image

# ? display a random picture of floppa
bot.lastRolledFloppa = None
@bot.command(name = "floppa", brief = "Posts a floppa") # create new command, pass 'name' keyword argument into the decorator
async def postImage(ctx):
	if(bot.lastRolledFloppa == None):
		fileNameChoice = "images/floppa/" + random.choice(floppaFileList) # get a random file name from list
		bot.lastRolledFloppa = fileNameChoice
	else:
		fileNameChoice = "images/floppa/" + random.choice(floppaFileList) # get a random file name from list
		while(fileNameChoice == bot.lastRolledFloppa):
			fileNameChoice = "images/floppa/" + random.choice(floppaFileList) # get a random file name from list
			bot.lastRolledFloppa = fileNameChoice
	await ctx.reply(file = discord.File(fileNameChoice))
	

# ? display the songs a user is listening, or every user if no input param is received
@bot.command(aliases = ['listening'], brief = "See whose listening to what on Spotify")
async def listen(ctx, user: discord.Member = None):
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
					embed.set_footer(text = "Song started at {} UTC".format(activity.created_at.strftime("%H:%M")))
					await ctx.reply(embed = embed)
	else: # get spotify activity for specific user
		for activity in user.activities: # iterate through the given users activities
			if isinstance(activity, discord.Spotify):
				foundResult = True
				embed = discord.Embed(description = "Listening to *{}* ".format(activity.title), color = activity.color)
				embed.set_image(url = activity.album_cover_url)
				embed.set_author(name = f"{user.name}'s Spotify", icon_url = user.avatar_url)
				embed.add_field(name = "Artist", value = activity.artist)
				embed.add_field(name = "Album", value = activity.album)
				embed.set_footer(text = "Song started at {} UTC".format(activity.created_at.strftime("%H:%M")))
				await ctx.reply(embed = embed)
	if(not foundResult): # no results found
		embed = discord.Embed(title = "Couldn't find anyone listening to music :(")
		embed.set_image(url = "https://c.tenor.com/BCqVPaQdwBsAAAAC/bingus-binguscord.gif") # error image
		await ctx.reply(embed = embed)

@listen.error
async def listenError(ctx, error):
	if isinstance(error, commands.errors.MemberNotFound):
		if(error.argument == "@everyone" or error.argument == "@here"):
			await listen(ctx, None)
		else:
			await ctx.reply(":x: No user found :(")

bot.run(os.getenv('TOKEN')) # run the bot using the 'TOKEN' environment variable