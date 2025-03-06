import discord
import os
import yt_dlp
import sys
from discord.ext import commands
from dotenv import load_dotenv
from collections import deque

# Load Opus library based on the OS
if sys.platform == "darwin":  # macOS
    discord.opus.load_opus("/opt/homebrew/lib/libopus.dylib")
elif sys.platform == "win32":  # Windows
    discord.opus.load_opus("opus.dll")
elif sys.platform == "linux":  # Linux
    discord.opus.load_opus("/usr/lib/libopus.so")

# Create .env file in your Folder and Type "DISCORD_TOKEN=<your_bot_token>" inside the .env file.
load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

# Set bot command prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

# Song queue
song_queue = deque()
loop_mode = False
volume_level = 1.0

@bot.event
async def on_ready():
    print(f"✅ Logged in as {bot.user}")

@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        await channel.connect()
        await ctx.send(f"Joined `{channel.name}` ✅")
    else:
        await ctx.send("❌ You need to be in a voice channel!")

@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("Left the voice channel ❌")
    else:
        await ctx.send("I'm not in a voice channel!")

async def play_next(ctx):
    global loop_mode, volume_level
    if loop_mode and ctx.voice_client and ctx.voice_client.source:
        ctx.voice_client.stop()
        ctx.voice_client.play(ctx.voice_client.source, after=lambda e: bot.loop.create_task(play_next(ctx)))
        return
    
    if song_queue:
        next_url, next_title = song_queue.popleft()
        voice_client = ctx.voice_client
        source = discord.FFmpegPCMAudio(next_url, **FFMPEG_OPTIONS)
        voice_client.play(discord.PCMVolumeTransformer(source, volume_level), after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f"🎵 Now playing: `{next_title}`")

@bot.command()
async def play(ctx, url: str = None):
    global volume_level
    if url is None:
        await ctx.send("❌ Please provide a YouTube URL!")
        return

    voice_client = ctx.voice_client
    
    if not voice_client:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            await channel.connect()
            voice_client = ctx.voice_client
        else:
            await ctx.send("You need to be in a voice channel to play music.")
            return

    ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        url2 = info['url']
        title = info['title']

    if voice_client.is_playing():
        song_queue.append((url2, title))
        await ctx.send(f"🎵 Added to queue: `{title}`")
    else:
        source = discord.FFmpegPCMAudio(url2, **FFMPEG_OPTIONS)
        voice_client.play(discord.PCMVolumeTransformer(source, volume_level), after=lambda e: bot.loop.create_task(play_next(ctx)))
        await ctx.send(f"🎵 Now playing: `{title}`")

@bot.command()
async def stop(ctx):
    song_queue.clear()
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
    await ctx.send("⏹️ Music stopped and queue cleared.")

@bot.command()
async def skip(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("⏭️ Skipped song.")
    else:
        await ctx.send("No song is currently playing!")

@bot.command()
async def queue_list(ctx):
    if not song_queue:
        await ctx.send("📭 The queue is empty!")
    else:
        queue_text = "\n".join([f"{i+1}. {title}" for i, (_, title) in enumerate(song_queue)])
        await ctx.send(f"🎵 **Current Queue:**\n{queue_text}")

@bot.command()
async def volume(ctx, volume: int):
    global volume_level
    if 0 <= volume <= 100:
        volume_level = volume / 100
        if ctx.voice_client and ctx.voice_client.source:
            ctx.voice_client.source.volume = volume_level
        await ctx.send(f"🔊 Volume set to {volume}%")
    else:
        await ctx.send("❌ Volume must be between 0 and 100!")


@bot.command()
async def commands(ctx):
    command_list = "\n".join([f"!{command}" for command in bot.commands])
    await ctx.send(f"📜 **Available Commands:**\n{command_list}")

# Run the bot
if TOKEN:
    bot.run(TOKEN)
else:
    print("❌ DISCORD_TOKEN not found in .env file!")
