import disnake
import psutil
import platform
from disnake.ext import commands
import datetime
import os
from flask import Flask, render_template, jsonify

app = Flask(__name__)

bot = commands.Bot(command_prefix="/")

@bot.slash_command()
async def botinfo(inter):
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

    memory_info = psutil.virtual_memory()
    embed.add_field(name="Memory Usage 🧠", value=f"{memory_info.percent}%")

    os_info = f"{platform.system()} {platform.release()}"
    embed.add_field(name="Operating System 🖥️", value=os_info)

    python_version = platform.python_version()
    embed.add_field(name="Python Version 🐍", value=python_version)

    await inter.response.send_message(embed=embed)

@app.route('/bot_stats')
def bot_stats():
    ping = round(bot.latency * 1000, 2)
    cpu_usage = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    os_info = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()

    return jsonify({
        'ping': ping,
        'cpu_usage': cpu_usage,
        'memory_usage': memory_usage,
        'os_info': os_info,
        'python_version': python_version
    })

if __name__ == "__main__":
    bot.run(os.environ["BOT_TOKEN"])
    app.run()
