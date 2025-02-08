from init import bot, servers
from server import Server
from functions import get_guild_object

def generate_bot_event_functions():
    @bot.event 
    async def on_ready():
        print(f"logged in as {bot.user}")
        
        for guild in bot.guilds:
            servers.append(Server(guild.id))


    @bot.event
    async def on_message(msg):
        if msg.author == bot.user:
            return 
        if msg.content.__contains__("hello"):
            await msg.channel.send("hello")