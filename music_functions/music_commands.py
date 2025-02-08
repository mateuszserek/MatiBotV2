import discord
from init import bot, servers
from music_functions.song import Song
from youtubesearchpython import VideosSearch
import yt_dlp
from discord import FFmpegOpusAudio
from asyncio import ensure_future
import os
from functions import get_guild_object, create_embed


def gen_music_functions():

    @bot.tree.command(name = "play", description = "play some music")
    @discord.app_commands.describe(query = "your request")
    async def play(interaction: discord.Interaction, query: str):        
        
        if interaction.user.voice is None:
            await interaction.response.send_message("You need to connect to vc")
            return 
        
        guild_object = get_guild_object(interaction.guild.id, servers)
        song_obj = add_song_to_queue(guild_object, query, interaction.user.name)
        embed = create_embed("Added to queue", f"Title: {song_obj.title} \nRequested by: {song_obj.requested_by}\nDuration: {song_obj.duration}", 0x222222)  
        
        await interaction.response.send_message(embed = embed)

        if guild_object.is_playing_on_vc:
            return

        guild_object.is_playing_on_vc = True
        vc = interaction.user.voice.channel
        text_channel = interaction.channel
        await vc.connect()
        await download_and_play(interaction.guild.voice_client, interaction.guild.id, text_channel)


    @bot.tree.command(name = "skip", description = "Skip current song")
    async def skip(interaction: discord.Interaction):
        await interaction.response.defer()
        vc = interaction.guild.voice_client
        if vc is None:
            return 
        
        guild_object = get_guild_object(interaction.guild.id, servers)
        if len(guild_object.music_queue) == 0:
            await interaction.followup.send("queue is already empty")
            return
        
        await interaction.followup.send("Skipping current song")
        vc.stop()


    @bot.event
    async def on_voice_state_update(member, before, after):
        if member == bot.user and member.voice is None:
            guild_id = before.channel.guild.id 
            guild_object = get_guild_object(guild_id, servers)
            guild_object.music_queue = []
            guild_object.is_playing_on_vc = False 


    async def download_and_play(voice_channel, guild_id, text_channel):
        guild_object = get_guild_object(guild_id, servers)
        song_obj = guild_object.music_queue[0]
        download_audio_from_youtube(guild_object.music_queue[0].url, guild_id)
        src = FFmpegOpusAudio(f"audio/{guild_id}.mp3")
        embed = create_embed("Playing", f"Title: {song_obj.title} \nRequested by: {song_obj.requested_by}\nDuration: {song_obj.duration}", 0x222222) 
        async_in_sync_function(lambda: text_channel.send(embed = embed)) 
        voice_channel.play(src, after = lambda e: after_song(voice_channel, guild_id, text_channel))
        

    def after_song(voice_channel, guild_id, text_channel):

        guild_object = get_guild_object(guild_id, servers)

        if not guild_object.music_queue:
            return 
        
        guild_object.music_queue.pop(0)
        os.remove(f"audio/{guild_id}.mp3")

        if not guild_object.music_queue:
            async_in_sync_function(voice_channel.disconnect)
            embed = create_embed("Queue empty", "It was the last song, use `/play` to add something", 0x222222)
            async_in_sync_function(lambda: text_channel.send(embed = embed))
            guild_object.is_playing_on_vc = False

        else:
            async_in_sync_function(lambda: download_and_play(voice_channel, guild_id, text_channel) ) 


    def add_song_to_queue(guild_object, query, username) -> Song:
        song_info = find_info_from_yt(query)
        song = Song(query,song_info["duration"], username, song_info["title"], song_info["link"])
        guild_object.music_queue.append(song)
        return song


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
        
    def async_in_sync_function(func):
        coro = func()
        fut = ensure_future(coro, loop = bot.loop)
        fut.add_done_callback(lambda t: t.result())

            
    # def check_correct_vc(bot_vc, user_vc) -> bool:
    #     if user_vc is None:
    #         return False 
        
    #     if user_vc != bot_vc:
    #         return False 
        
    #     return True 