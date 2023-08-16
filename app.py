from flask import Flask, render_template
import psutil
import platform
import disnake
from disnake.ext import commands
import os

app = Flask(__name__)

# Initialize the bot
bot = commands.Bot(command_prefix="/")

@bot.slash_command()
async def botinfo(inter):
    embed = disnake.Embed(
        title="Bot Information 🤖",
        description="Here's some information about the bot!",
        color=0x7289DA
    )

    ping = round(bot.latency * 1000, 2)
    embed.add_field(name="Ping 📶", value=f"{ping} ms")

    cpu_usage = psutil.cpu_percent()
    embed.add_field(name="CPU Usage 💻", value=f"{cpu_usage}%")

    memory_usage = psutil.virtual_memory().percent
    embed.add_field(name="Memory Usage 🧠", value=f"{memory_usage}%")

    os_info = f"{platform.system()} {platform.release()}"
    embed.add_field(name="Operating System 🖥️", value=os_info)

    python_version = platform.python_version()
    embed.add_field(name="Python Version 🐍", value=python_version)

    # Additional bot info fields
    disk_usage = psutil.disk_usage("/").percent
    embed.add_field(name="Disk Usage 💽", value=f"{disk_usage}%")

    network_info = psutil.net_io_counters()
    embed.add_field(name="Network Info 🌐", value=f"Sent: {network_info.bytes_sent} B\nReceived: {network_info.bytes_recv} B")

    # Add more bot info fields here

    invite_button = disnake.ui.Button(
        label="Invite Bot 🤖",
        emoji="🤖",
        url=f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot",
        style=disnake.ButtonStyle.link
    )

    view = disnake.ui.View()
    view.add_item(invite_button)

    await inter.response.send_message(embed=embed, view=view)

@app.route('/server_info')
def server_info():
    server_count = len(bot.guilds)
    total_users = sum(guild.member_count for guild in bot.guilds)

    return jsonify({
        'serverCount': server_count,
        'totalUsers': total_users
    })

@app.route('/bot_stats')
def bot_stats():
    ping = round(bot.latency * 1000, 2)
    cpu_usage = psutil.cpu_percent()
    memory_info = psutil.virtual_memory().percent
    os_info = f"{platform.system()} {platform.release()}"
    python_version = platform.python_version()

    return jsonify({
        'ping': ping,
        'cpuUsage': cpu_usage,
        'memoryUsage': memory_info,
        'osInfo': os_info,
        'pythonVersion': python_version
    })
}

@app.route("/")
def index():
    return render_template("index.html", bot_info=bot_info)

if __name__ == "__main__":
    bot.run(os.environ["BOT_TOKEN"])
    app.run(debug=True)
