from init import bot, servers
import discord 

@bot.event
async def on_message(msg):
    if msg.author == bot.user:
        return 
    if msg.content.__contains__("hello"):
        await msg.channel.send("hello")

    await bot.tree.sync(guild = bot.get_guild(630115790460420096))