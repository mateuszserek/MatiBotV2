import discord
from discord.ext import commands
from functions import *
from init import *
from events import *

def main():
    bot.run(get_token("DISCORD_TOKEN"))

if __name__ == "__main__":
    main()