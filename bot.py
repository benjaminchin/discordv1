import discord
import youtube_dl
from discord.ext import commands
from discord import Game, Colour
import os

from discord.utils import get

players = {}
TOKEN = 'NjUzMjk4NjMxMTY3ODM2MTkw.Xe0-VA.f03hSp55IBfDGlY-Tn1VJsAOByU'
client = commands.Bot(command_prefix='.')
voice = ''


@client.event
async def on_ready():
    game = discord.Game(".commands for help")
    await client.change_presence(status=discord.Status.online, activity=game)
    print('Bot online; TOKEN', TOKEN)


@client.command(pass_context=True)
async def commands(ctx):
    channel = await ctx.message.author.create_dm()
    embed = discord.Embed(colour=Colour.green(), title='Commands List', description=".commands - Sends this "
                                                                                    "message\n.play <URL> - Uses "
                                                                                    "YouTube URL "
                                                                                    "to play audio. Also makes bot "
                                                                                    "join the current voice "
                                                                                    "channel\n.pause - Pauses current "
                                                                                    "audio\n.unpause - Unpauses "
                                                                                    "current audio\n.stop - Stops "
                                                                                    "current audio\n.join Makes bot "
                                                                                    "join current voice "
                                                                                    "channel\n.leave - Makes bot leave "
                                                                                    "the voice channel")

    await channel.send(embed=embed)
    user = ctx.message.author
    print(user)
    await ctx.send(user.mention + " Message sent to DMs! :christmas_tree:")


@client.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel
    await channel.connect()


@client.command(pass_context=True)
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    try:
        await ctx.guild.voice_client.disconnect()
    except AttributeError:
        await channel.connect()
        await ctx.guild.voice_client.disconnect()


@client.command(pass_context=True)
async def play(ctx, url: str):
    try:
        channel = ctx.message.author.voice.channel
        await channel.connect()
    except:
        print("OK lmao")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            print("Removed old song file.")
    except PermissionError:
        print("Trying to delete song file but it's being played.")
        await ctx.send("Something is already playing, you retard. Stop it before playing something else.")
        return

    await ctx.send("Chill bruh im getting it ready.")
    global voice
    voice = get(client.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }]
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now.\n")
        ydl.download([url])
    name = ""
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed File:{file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit("-", 2)
    print(nname)
    await ctx.send(f":musical_note: Playing: {nname[:-1]}")
    print("Playing")


@client.command(pass_context=True)
async def pause(ctx):
    global voice
    voice.pause()
    await ctx.send(":pause_button: Audio paused.")
    print("Paused")


@client.command(pass_context=True)
async def unpause(ctx):
    global voice
    voice.resume()
    await ctx.send(":play_pause: Audio unpaused.")
    print("Resumed")


@client.command(pass_context=True)
async def stop(ctx):
    global voice
    voice.stop()
    await ctx.send(":stop_button: Audio stopped.")
    print("Stopped")


client.run(TOKEN)
