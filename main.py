from functions import *
from init import *
import events
import music_functions.music_commands

music_functions.music_commands.gen_music_functions()
events.generate_bot_event_functions()

bot.run(get_token("DISCORD_TOKEN"))