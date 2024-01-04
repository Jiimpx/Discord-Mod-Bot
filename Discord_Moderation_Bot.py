#Discord Moderation Bot
#By James Anderton

import discord #Imports the discord module.
from discord.ext import commands #Imports discord extensions.
from discord.utils import get
import time
from datetime import datetime
import asyncio
from wordFilter import Swears


intents = discord.Intents.default()
intents.members = True
bot = commands.Bot(command_prefix='!', intents = intents)
print(discord.version_info)
#Stores the token for the bot
strToken = [your token here]
intLoggingChannel = 950389964556869683 #Variable to store the channel id for the logging channel
intStaffChannel = 933784909322002523 #Variable to store the channel id for the staff chat channel
intNewAccount = 604800 #Variable to store the amount of seconds in 7 days, 7 days being the amount of time discord flags an account as "new"
wordDetection = Swears()


wordDetection.load_censor_words_from_file("./bad_words.txt") # Loads in a text file containing a list of plain swear words (list taken from http://www.bannedwordlist.com/)p



#notifies when the bot is ready to be used, any commands used outside this time will not work
@bot.event
async def on_ready():
    print("Bot is ready to go!")
 
#Simple hello command to test if the bot is working, bot will reply in the channel the comamnd was invokated. No need for special permissions here as its a harmless command
@bot.command()
async def hello(ctx):
    await ctx.reply('Hello!')


#Bot will give a member role upon them joining

@bot.event
@commands.has_permissions(manage_roles = True) #The bot has to have the permission of being able to manage roles for it to add/remove them
async def on_member_join(member):

    #Automatically add a member role on joinng the server, users cannot interact without this role
    role = discord.utils.get(member.guild.roles, name="Member")
    await member.add_roles(role)
   
    #Account joining logging
    channel = bot.get_channel(intLoggingChannel)
    staffChannel = bot.get_channel(intStaffChannel)
    msg = str(member.mention) + 'Has joined with account age of  ' + member.created_at.strftime('%m/%d/%Y')
    await channel.send(msg)

    #If the account is brand new (7 days old or less) the account will be flagged in the staff channel as a suspicious account
    if time.time() - member.created_at.timestamp() < intNewAccount:
        #Notify staff members when the account is detected
        msg = str(member.mention)+ ' user has joined with a suspicious new account with a date of ' + member.created_at.strftime('%m/%d/%Y')
        await staffChannel.send(msg)



#Banning the User
@bot.command()
@commands.has_permissions(ban_members = True)
async def ban(ctx, member : discord.Member, *, reason):
    await member.ban(reason = reason)
    await ctx.reply('User has been banned')

#The below code unbans player.
@bot.command()
@commands.has_permissions(administrator = True) #Only admins are able to unban a user to help minimise the impact of a rogue moderator
async def unban(ctx, *, member):

    #Input has to be the users discord name (Jim) followed by a # as that is how discord seperates a name from their discriminator and then their discrimination such as 001
    #example command !unban Jim#0001 would be a valid input
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention}')
            return
        
#Basic error handling, this can be expanded on as more commands are made in the future and more errors will crop up        
@bot.event
async def on_command_error(ctx,error):
    #Will tell the user if they cant use the command and do not have the permissions to use it, this is important for commands like banning and unbanning a user
   if isinstance(error, commands.errors.MissingPermissions):
       await ctx.send("You do not have the required permissions to execute that command")
    #Will tell the user they're missing something such as a ban reason not being entered when using the command !ban
   if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send("please enter all the required arguments for the command")



#"Breather" (Mute) Command

@bot.command()
@commands.has_permissions(manage_roles = True) #User needs manage roles to be able to execute the command to prevent trolling and abuse of muting
async def mute(ctx, member: discord.Member):

    guild = ctx.guild
    perms = discord.Permissions(send_messages=False, read_messages=True, speak = False)

    if get(ctx.guild.roles, name = "Breather"): #Checks if the breather role already exists as we dont want hundreds of breather roles everytime someone is muted, will create the role if it doesnt exist though

        await ctx.send("Breather Already Exists, will not create a new one")
    else:
        await guild.create_role(name = "Breather",  permissions = perms)
    role = discord.utils.get(member.guild.roles, name="Breather")
    await member.add_roles(role)
    #Dms the now breathered member that they cannot interact with the server as muting them locks them out of channels
    await member.send("Hi there, you've been placed on a breather that restricts your access to the server. A moderator will be with you shortly")

#Unmute Command

@bot.command()
@commands.has_permissions(manage_roles = True) #Command can only be executed if the user has the right permissions, in this case manage roles
async def unmute(ctx, member: discord.Member):
    role_get = get(member.guild.roles, name = "Breather")  
    await member.remove_roles(role_get)
    await ctx.send("User has been unmuted from chat")


#Reminder command, anyone can use it as a reminder could be used by anyone in a given situation
#Can use days, hours,minutes and seconds with a maximum time of 90 days and a minimum of 5 minutes
#This command assumes the bot will be running for the entire time, turnning it off and on again will not have the reminder retained
@bot.command(case_insensitive = True, aliases = ["remind", "remindme", "remind_me"])
@commands.bot_has_permissions(attach_files = True, embed_links = True)
async def reminder(ctx, time, *, reminder):
    print(time)
    print(reminder)
    user = ctx.message.author
    embed = discord.Embed(color=0x55a7f7, timestamp=datetime.utcnow())
    seconds = 0
    if reminder is None:
        embed.add_field(name='Warning', value='Please specify what do you want me to remind you about.') # Error message
    if time.lower().endswith("d"):
        seconds += int(time[:-1]) * 60 * 60 * 24
        counter = f"{seconds // 60 // 60 // 24} days"
    if time.lower().endswith("h"):
        seconds += int(time[:-1]) * 60 * 60
        counter = f"{seconds // 60 // 60} hours"
    elif time.lower().endswith("m"):
        seconds += int(time[:-1]) * 60
        counter = f"{seconds // 60} minutes"
    elif time.lower().endswith("s"):
        seconds += int(time[:-1])
        counter = f"{seconds} seconds"
    if seconds == 0:
        embed.add_field(name='Warning',
                        value='Please specify a proper duration')
    elif seconds < 300:
        embed.add_field(name='Warning',
                        value='You have specified a too short duration!\nMinimum duration is 5 minutes.')
    elif seconds > 7776000:
        embed.add_field(name='Warning', value='You have specified a too long duration!\nMaximum duration is 90 days.')
    else:
        await ctx.send(f"Alright, I will remind you about {reminder} in {counter}.")
        await asyncio.sleep(seconds)
        await ctx.send(f"Hi, you asked me to remind you about {reminder} {counter} ago.")
        return
    await ctx.send(embed=embed)


# Word Filter and detecting people bypassing the filter

#Command adds a new word to the custom word list, the default list is untouched
@bot.command(case_insensitive = True, aliases = ["addswearword", "addsw", "blacklist", "addword"])
@commands.has_permissions(administrator = True) #Permissions restricted to administrator to prevent mod abuse
async def addswear(ctx, word):
    file = open("./bad_words.txt", "a")
    file.write( "\n" + word)
    file.close()
    wordDetection.load_censor_words_from_file("./bad_words.txt")
    await ctx.send("Word added")

#Command to whitelist a word from the bot, this will whitelist itfrom the custom wordlist and not the default
@bot.command(case_insensitive = True, aliases = ["delswearword", "delsw", "whitelist", "delword"]) #Permissions restricted to administrator to prevent mod abuse
@commands.has_permissions(administrator = True)
async def delswear(ctx, word):
    wordDetection.load_censor_words_from_file("./bad_words.txt", whitelist_words =[word]) #The given word will not be flagged again, will delete use of the command due to the order of operations but the bug isnt bot breaking
    await ctx.send("Word has been whitelisted")
                  
        
  
@bot.event
async def on_message(message):
   if not message.author.bot:
       #Uses the contains swears function from wordFilter.py. See the page for more details
        if wordDetection.contains_swears(message.content):
           await message.delete()
           await message.channel.send(message.author.mention +"You're not allowed to use this word here")
   await bot.process_commands(message) #This has to be included as on_message has priority over all commands so none will be executed

#Command will log all messages deleted, this is important with the slur filter to see what they deleted and check if it was a false positive or not
@bot.event
async def on_message_delete(message):
    channel = bot.get_channel(intLoggingChannel)
    msg = str(message.author.mention)+ ' deleted message in '+str(message.channel)+': '+str(message.content)
    await channel.send(msg)
    await bot.process_commands(message) #This has to be included as on_message has priority over all commands so none will be executed


bot.run(strToken) #Starts the bot


