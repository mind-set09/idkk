import disnake
from disnake.ext import commands
import psutil
import platform
import time
import datetime

intents = disnake.Intents.default()
intents.typing = False
intents.presences = False

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name} - {bot.user.id}")

@bot.slash_command()
async def botinfo(ctx):
    embed = disnake.Embed(
        title="Bot Information 🤖",
        description="Here's some information about the bot!",
        color=0x7289DA
    )

    embed.set_thumbnail(url=bot.user.avatar.url)

    ping = round(bot.latency * 1000, 2)
    embed.add_field(name="Ping 📶", value=f"{ping} ms")

    cpu_usage = psutil.cpu_percent()
    embed.add_field(name="CPU Usage 💻", value=f"{cpu_usage}%")

    memory = psutil.virtual_memory().percent
    embed.add_field(name="Memory Usage 🧠", value=f"{memory}%")

    server_count = len(bot.guilds)
    embed.add_field(name="Server Count 🌐", value=f"{server_count} servers")

    uptime = datetime.datetime.now() - bot.start_time
    uptime_str = f"{uptime.days} days, {uptime.seconds // 3600} hours, {(uptime.seconds // 60) % 60} minutes"
    embed.add_field(name="Uptime ⏲️", value=uptime_str)

    python_version = platform.python_version()
    embed.add_field(name="Python Version 🐍", value=python_version)

    await ctx.send(embed=embed)

def get_live_info():
    while True:
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        network_info = psutil.net_io_counters()
        python_version = platform.python_version()
        platform_info = platform.platform()

        live_info = {
            "CPU Usage": f"{cpu_percent}%",
            "Memory Usage": f"{memory.percent}%",
            "Network Sent": f"{network_info.bytes_sent / 1024:.2f} KB",
            "Network Received": f"{network_info.bytes_recv / 1024:.2f} KB",
            "Python Version": python_version,
            "Platform": platform_info
        }

        print("Live Bot Information:")
        for key, value in live_info.items():
            print(f"{key}: {value}")

        time.sleep(5)  # Update every 5 seconds

if __name__ == "__main__":
    bot.loop.create_task(get_live_info())
    bot.run("MTE0MTE4MjQ3MTQwOTUwNDMwNg.Gx68d-.SmdzQh2OC3fBmDaxb4fORptimR0hlrzjmtymZ8")
