import discord
from discord.ext import commands
from init import bot, servers
from music_functions.song import Song
from youtubesearchpython import VideosSearch
import yt_dlp
from discord import FFmpegOpusAudio
from server import Server
from asyncio import ensure_future
import os
from functions import get_guild_object


def gen_music_functions():

    @bot.tree.command(name = "play", description = "play some music")
    @discord.app_commands.describe(query = "your request")
    async def play(interaction: discord.Interaction, query: str):        

        guild_object = get_guild_object(interaction.guild.id, servers)

        add_song_to_queue(guild_object, query, interaction.user.name)

        if guild_object.is_playing_on_vc:
            await interaction.response.send_message("dodano do kolejki (chyba)")
            return

        guild_object.is_playing_on_vc = True
        vc = interaction.user.voice.channel
        await vc.connect()
        download_and_play(interaction.guild.voice_client, interaction.guild.id)



    def download_and_play(voice_channel, guild_id):
        guild_object = get_guild_object(guild_id, servers)
        download_audio_from_youtube(guild_object.music_queue[0].url, guild_id)
        src = FFmpegOpusAudio(f"audio/{guild_id}.mp3")
        voice_channel.play(src, after = lambda e: after_song(voice_channel, guild_id))
        

    def after_song(voice_channel, guild_id):
        guild_object = get_guild_object(guild_id, servers)
        guild_object.music_queue.pop(0)
        os.remove(f"audio/{guild_id}.mp3")

        if len(guild_object.music_queue) == 0:
            coro = voice_channel.disconnect()
            fut = ensure_future(coro, loop = bot.loop)
            fut.add_done_callback(lambda t: t.result()) #tajemnicza koncepcja która poprostu działa, można kiedyś przerobć na funkcję
            guild_object.is_playing_on_vc = False

        else:
            download_and_play(voice_channel, guild_id)


    def add_song_to_queue(guild_object, query, username):
        song_info = find_info_from_yt(query)
        song = Song(song_info["title"], query, song_info["duration"], username, song_info["link"])
        guild_object.music_queue.append(song)



    def download_audio_from_youtube(link: str, guild_id: int) -> None: #dorobić try, except
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',  
            'preferredquality': '192',
        }],
        'outtmpl': f'audio/{guild_id}',
    }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])


    def find_info_from_yt(keyword: str) -> dict:  #do poprawyyy try, except
        video_info = VideosSearch(keyword, limit = 1).result()["result"][0]
        if video_info["type"] == "video":
            link = video_info["link"] 
            title = video_info["title"] 
            duration = video_info["duration"]
            return {
                "link": link,
                "title": title,
                "duration": duration
            }
            
    # def check_correct_vc(bot_vc, user_vc) -> bool:
    #     if user_vc is None:
    #         return False 
        
    #     if user_vc != bot_vc:
    #         return False 
        
    #     return True 