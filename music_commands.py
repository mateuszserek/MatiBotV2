import discord
from discord.ext import commands
from init import bot, servers
from song import Song
from youtubesearchpython import VideosSearch
import yt_dlp
from discord import FFmpegOpusAudio
from pytubefix import YouTube


def gen_music_functions():

    def get_guild_queue(guild_id):
        for i in servers:
            if i.id == guild_id:
                return i.music_queue

    @bot.tree.command(name = "play", description = "play some music")
    @discord.app_commands.describe(query = "your request")
    async def play(interaction: discord.Interaction, query: str):

        song_info = find_info_from_yt(query)

        song = Song(query, "niewazne", interaction.user.name)
        guild_queue = get_guild_queue(interaction.guild.id)
        guild_queue.append(song)
        download_audio_from_youtube(song_info["link"], interaction.guild.id)

        vc = interaction.user.voice.channel 
        await vc.connect()
        src = FFmpegOpusAudio(f"audio/{interaction.guild.id}.mp3")
        vc.play(src, after = lambda e: print("piwo"))
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
        # yt = YouTube(link, allow_oauth_cache = True, use_po_token = True)
        # video = yt.streams.filter(only_audio=True).first()
        # destination = f"audio/{guild_id}.mp3"
        # out_file = video.download(output_path=destination)


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
            