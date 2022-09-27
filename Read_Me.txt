Hello!

This is James, making a little instruction set on how to use the bot when you come to test

The plan is to have the bot hosted on a cloud service, but failing that the visual studio sln file and .py files are attached in this zip file for you to extract and run


__Installing discord.py__

This is the only external library I've used, everything else should be included in the solution

You will need:

>visual studio or visual studio code, both should work

>a machine with python 3.8 or later installed on it. I have not tested older versions of python and I have been coding this in 3.8

>open the command prompt of the solution and enter "pip install discord.py" wait for it to download and you should be good to go


__Logging in__

I don't expect my tutors to make a discord account or use their personal one for this so I have created a test account for you

Details are:

login website: discord.com

Email: JAnderton2@uclan.ac.uk

Password: Ilovediscord2022

You should have the member role and the admin role already, this is so you can use the commands that are admin restricted.

If you would like to leave and rejoin the server again, you will need to copypaste this invite link discord.gg/A7GvNeAbKg

rejoining while the bot is on will only give you the member role so please be careful with commands, rejoining while the bot is off gives you no roles

This isnt the most secure but this is a burner account, I plan to delete it once the project has been completed


__Commands__

Here is a list of the commands along with what they do

Developer mode has been enabled for your account which allows you to copy their users id
(this is standard across discord server moderation)

To tag a user right click their profile picture and press "copy id", then type the message <@[copypasted id]>
and this should ping the user

e.g <@ 202154336191512576 > (without the spaces) will ping my personal discord account

The prefix for all of them is "!"

!hello - Bot will say hello to you

!mute (user ping) - Inputting this will mute a user from the server, restricting them to be able to talk

!unmute (user ping) - This will do the exact opposite of !mute

!ban (user ping), reasoning - Inputting a users tag and a reason will ban the user, failing to input a reasoning will give an error

!unban users full discord tag - This will unban the user and make sure they can come back to the server

#Input has to be the users discord name (Jim) followed by a # as that is how discord seperates a name from their discriminator and then their discrimination such as 0001
#example command !unban Jim#0001 would be a valid input

!remind time , whats the reminder reason - More details on the specifics of the command can be found in the code itself.

#Can use days, hours,minutes and seconds with a maximum time of 90 days and a minimum of 5 minutes
#This command assumes the bot will be running for the entire time, turnning it off and on again will not have the reminder retained
#!remind 10m hello bot - this would be a valid use of the command

!addswear word - adds a word to the txt file so the word filter will start looking for it

!delswear word - whitelists a word so that the bot will not delete your message for using it



The rest of the function of the bot are events, so when a specific thing happens there is no command for these.

**Please check the code for more details on these events**


**I will warn you that this bot deals with bad words: there are swears, homophobic, racist, sexist and transphobic words that the text file contains and some of the logging channels contain.
I do not endorse the use of these words but they needed to be tested as the bot would not be useful if it didnt catch them. Please do not judge the people who used the words harshly, they are a mix of my friends and family
who entered the words under my instruction to help test**


That should be all, enjoy using the bot
