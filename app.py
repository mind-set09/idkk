import disnake
import psutil
import platform
from disnake.ext import commands
import datetime
import os
from flask import Flask, render_template
import threading
import requests

# Flask app setup
app = Flask(__name__)

# Bot setup
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

    # Additional Information
    disk_usage = psutil.disk_usage("/")
    embed.add_field(name="Disk Usage 💾", value=f"{disk_usage.percent}%")

    boot_time = datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")
    embed.add_field(name="Boot Time ⏰", value=boot_time)

    # Add more fields as needed

    invite_button = disnake.ui.Button(
        label="Invite Bot 🤖",
        emoji="🤖",
        url=f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot",
        style=disnake.ButtonStyle.link
    )

    view = disnake.ui.View()
    view.add_item(invite_button)

    await inter.response.send_message(embed=embed, view=view)


# Flask route
@app.route("/")
def index():
    try:
        response = requests.get("http://localhost:5000/botinfo")
        bot_info = response.json()
    except requests.exceptions.RequestException as e:
        bot_info = {"error": str(e)}

    return render_template("index.html", bot_info=bot_info)

# Thread to run both Flask and bot
def run_bot():
    bot.run(os.environ["BOT_TOKEN"])

if __name__ == "__main__":
    thread = threading.Thread(target=run_bot)
    thread.start()
    
    app.run(debug=True)
