import discord
from discord.ext import commands
from functions import *
from server import Server

servers = []
  
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="/", intents = intents)
