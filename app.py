import disnake
import psutil
import platform
from disnake.ext import commands
import datetime
import os

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

    invite_button = disnake.ui.Button(
        label="Invite Bot 🤖",
        emoji="🤖",
        url=f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&permissions=0&scope=bot",
        style=disnake.ButtonStyle.link
    )

    view = disnake.ui.View()
    view.add_item(invite_button)

    await inter.response.send_message(embed=embed, view=view)

if __name__ == "__main__":
    bot.run(os.environ["BOT_TOKEN"])
