import discord
from discord.ext import commands
from init import bot, servers

@bot.tree.command(name = "play", description = "play some music")
@discord.app_commands.describe(query = "your request")
async def play(interaction: discord.Interaction, query: str):
    await interaction.response.send_message("testujemy!")