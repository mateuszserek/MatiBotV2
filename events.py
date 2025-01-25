from init import bot 
import discord 

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return 
    if msg.content.__contains__("hello"):
        await msg.channel.send("hello")
