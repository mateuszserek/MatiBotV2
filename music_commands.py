import discord
from discord.ext import commands
from init import bot, servers
from song import Song
from youtubesearchpython import VideosSearch
import yt_dlp
from discord import FFmpegOpusAudio
from server import Server


def gen_music_functions():

    def get_guild_object(guild_id) -> Server:
        for i in servers:
            if i.id == guild_id:
                return i

    @bot.tree.command(name = "play", description = "play some music")
    @discord.app_commands.describe(query = "your request")
    async def play(interaction: discord.Interaction, query: str):

        song_info = find_info_from_yt(query)

        song = Song(query, "niewazne", interaction.user.name)
        guild_object = get_guild_object(interaction.guild.id)
        guild_object.music_queue.append(song)

        if guild_object.is_playing_on_vc:
            await interaction.response.send_message("ups")
            return

        guild_object.is_playing_on_vc = True
        download_audio_from_youtube(song_info["link"], interaction.guild.id)

        vc = interaction.user.voice.channel
        await vc.connect()
        src = FFmpegOpusAudio(f"audio/{interaction.guild.id}.mp3")
        
        interaction.guild.voice_client.play(src, after = lambda e: print("piwo"))
        await interaction.response.send_message(f"jazda z patafianami")




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
            