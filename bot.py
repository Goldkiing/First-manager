import discord
from discord.ext import commands
import yt_dlp

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"✅ Bot is ready as {bot.user}")

@bot.command()
async def play(ctx, *, arg):
    if not arg.startswith("yt-audio:"):
        await ctx.send("❌ Use format: `/play yt-audio: <YouTube URL>`")
        return

    url = arg.replace("yt-audio:", "").strip()

    if ctx.author.voice is None:
        await ctx.send("🔇 Join a voice channel first.")
        return

    voice_channel = ctx.author.voice.channel
    vc = ctx.voice_client or await voice_channel.connect()

    if vc.is_playing():
        vc.stop()

    ydl_opts = {
        'format': 'bestaudio',
        'quiet': True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            info = ydl.extract_info(url, download=False)
            audio_url = info['url']
        except Exception as e:
            await ctx.send("⚠️ Error extracting audio.")
            print(e)
            return

    ffmpeg_opts = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }

    vc.play(discord.FFmpegPCMAudio(audio_url, **ffmpeg_opts))
    await ctx.send(f"🎧 Now playing: {info.get('title', 'Unknown')}")

@bot.command()
async def stop(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect()
        await ctx.send("⏹️ Disconnected.")
    else:
        await ctx.send("😴 Not connected.")

bot.run("YOUR_BOT_TOKEN")
