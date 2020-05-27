# -*- coding: utf-8 -*-
"""
Created on Tue May 26 15:10:59 2020

@author: smika
@purpose:
    This is a discord bot for handling input withing 'guilds'
"""

#import discord
import discord
from discord.ext import commands
from discord.utils import get
import datetime
import logging
import os
import youtube_dl

#put log data to console
#logging.basicConfig(level=logging.INFO)

#set debug mode and get logger
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

#ensure we get a new file name
filename = 'logs/JaKobePyBot'
buffer = ''
buffer_count = 0
extension =  '.log'
while os.path.exists(filename+buffer+extension):
    buffer = '_' + str(buffer_count)
    buffer_count = buffer_count + 1

fn = filename+buffer+extension

#create the log file
handler = logging.FileHandler(filename=fn, encoding='utf-8', mode='w')

#format the messages
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



#create the client for the bot
client = discord.Client()

#create the VoiceChannel
global voice
voice = None

#announce to console the bot connected to the server
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#on the event of a message
@client.event
async def on_member_join(member):
    for channel in member.server.channels:
        if str(channel).lower() == "general":
            await member.channel.send(f"Welcome to the Server {member.mention}!")

#on the event of a message
@client.event
async def on_message(message):
    #print the message author and content to console
    #print(message.author.name, message.author.id, message.author.discriminator)

    #ignore our messages
    if message.author == client.user:
        return
    
    #COMMANDS FOR ME/CREATOR ONLY
    if str(message.author.id) == my_id:
        if str(message.author.name) == my_name:
            if str(message.author.discriminator) == my_discriminator:

                #if I want to print to console
                if message.content.startswith(">print"):
                    print(message.content.split(' ', 1)[1])
                
                #if I want to close the bot.
                if message.content.startswith(">end"):
                    await client.logout()
    
    #COMMANDS FOR EVERYONE

    #list out commands
    if message.content.startswith('>commands'):
        commands_c =    ">commands - Direct Messages the Commands Currently Supported\n"
        hello_c =    ">hello     - Responds with Hello!.\n"
        online_c =  ">online   - Direct Messages the Count of Online Members in the server.\n"
        date_c =    ">date     - Direct Messages the current Date to the bot.\n"
        time_c =    ">time     - Direct Messages the current Time to the the bot.\n"
        help_text = "Commands: \n" + commands_c + hello_c + date_c + time_c + online_c
        await message.author.send(help_text)
    
    #say hello!
    if message.content.startswith('>hello'):
        await message.channel.send('Hello!')
    
    #give the user the current time for the bot
    if message.content.startswith('>time'):
        now = datetime.datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
        await message.author.send(f'The Current Time is: {current_time}')
    
    #give the user the current date for the bot
    if message.content.startswith('>date'):
        current_time = datetime.date.today()
        await message.author.send(f'The Date is: {current_time}')
    
    #give the user the current count of members of the server for the bot
    if message.content.startswith('>online'):
        guild = client.get_guild(guild_id)
        current_time = datetime.date.today()
        await message.author.send(f'The Count of Online Members is: {guild.member_count}')
    
    if message.content.startswith(">join"):
        channel = message.author.voice.channel
        global voice

        if voice and voice.is_connected():
            voice = await voice.move_to(channel)
            await message.channel.send(f"Moved to {channel}")
        else:
            voice = await channel.connect()
            await message.channel.send(f"Joined {channel}")
        
        print(f"The bot has connected to {channel}\n")
    
    if message.content.startswith(">leave"):
        channel = message.author.voice.channel
        if voice != None and voice.is_connected():
            await voice.disconnect()
            await message.channel.send(f"Left {channel}")
        else:
            await message.channel.send("Not Connected")
#run the bot
client.run(token)
