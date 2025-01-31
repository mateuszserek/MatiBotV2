from dotenv import load_dotenv
from os import getenv
from discord import Embed
from server import Server

def get_token(name: str) -> str:
    load_dotenv()
    return getenv(name)

def create_embed(new_title: str, new_description: str, new_color: int) -> Embed:  
    embed = Embed(
        color =  new_color,
        title = new_title,
        description = new_description
    )
    return embed

def get_guild_object(guild_id, servers) -> Server:
    for i in servers:
        if i.id == guild_id:
            return i

# def admin_only(user: Interaction.user) -> bool:
#     return user.guild_permissions.administrator
        