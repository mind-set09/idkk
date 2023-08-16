import os
import disnake
from disnake.ext import commands
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import psutil
import platform

# Bot setup
intents = disnake.Intents.default()
bot = commands.Bot(command_prefix='!', intents=intents)

# Database setup
DATABASE_URL = "sqlite:///bot_database.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

# Ticket class
class Ticket(Base):
    __tablename__ = "tickets"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text)
    author_id = Column(Integer)
    status = Column(String, default="Open")

    comments = relationship("TicketComment", back_populates="ticket")

class TicketComment(Base):
    __tablename__ = "ticket_comments"
    id = Column(Integer, primary_key=True, index=True)
    ticket_id = Column(Integer, ForeignKey("tickets.id"))
    author_id = Column(Integer)
    content = Column(Text)
    
    ticket = relationship("Ticket", back_populates="comments")

Base.metadata.create_all(bind=engine)

# Command: New Ticket
@bot.command()
async def new(ctx):
    await ctx.send("Create a ticket!", view=create_view)

# In-memory storage for active views
active_views = {}

# Persistent create ticket view
class CreateTicketView(disnake.ui.View):
    def __init__(self):
        super().__init__()
        self.ticket_title = None
        self.ticket_description = None

    @disnake.ui.button(label="Create Ticket", custom_id="create_button")
    async def create(self, button, inter):
        self.ticket_title = self.ticket_title or "No title"
        self.ticket_description = self.ticket_description or "No description"

        modal = CreateTicketModal(title=self.ticket_title, description=self.ticket_description)
        await inter.response.send_message("Ticket details captured.", ephemeral=True)
        await inter.message.edit(view=modal)

class CreateTicketModal(disnake.ui.Modal):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    title = disnake.ui.TextInput(label="Title", custom_id="title_input")  # Add custom_id parameter
    description = disnake.ui.TextInput(label="Description", custom_id="desc_input")  # Add custom_id parameter

    async def callback(self, inter):
        title = self.title.value
        desc = self.description.value

        ticket = Ticket(title=title, description=desc, author_id=inter.author.id)
        session = Session()
        session.add(ticket)
        session.commit()
        session.close()

        await inter.send("Ticket created!")
        
# Command: List Tickets
@bot.command()
async def tickets(ctx):
    session = Session()
    all_tickets = session.query(Ticket).all()
    session.close()

    if not all_tickets:
        await ctx.send("No tickets found.")
        return

    ticket_list = "\n".join([f"{ticket.id}: {ticket.title} - {ticket.status}" for ticket in all_tickets])
    await ctx.send(f"Tickets:\n{ticket_list}")

# Slash Command: View Ticket Details
@bot.slash_command()
async def ticket(inter, ticket_id: int):
    session = Session()
    ticket = session.query(Ticket).get(ticket_id)

    if not ticket:
        await inter.response.send_message("Ticket not found.")
        return

    comments = "\n".join([f"{comment.author_id}: {comment.content}" for comment in ticket.comments])
    embed = disnake.Embed(
        title=f"Ticket #{ticket.id}: {ticket.title}",
        description=ticket.description,
        color=0x7289DA
    )
    embed.add_field(name="Status", value=ticket.status)
    embed.add_field(name="Comments", value=comments or "No comments")

    await inter.response.send_message(embed=embed)

# Slash Command: Close Ticket
@bot.slash_command()
async def close_ticket(inter, ticket_id: int):
    session = Session()
    ticket = session.query(Ticket).get(ticket_id)

    if not ticket:
        await inter.response.send_message("Ticket not found.")
        return

    ticket.status = "Closed"
    session.commit()
    session.close()

    await inter.response.send_message(f"Ticket #{ticket.id} has been closed.")

# Slash Command: Add Comment
@bot.slash_command()
async def add_comment(inter, ticket_id: int, content: str):
    session = Session()
    ticket = session.query(Ticket).get(ticket_id)

    if not ticket:
        await inter.response.send_message("Ticket not found.")
        return

    comment = TicketComment(ticket_id=ticket_id, author_id=inter.author.id, content=content)
    session.add(comment)
    session.commit()
    session.close()

    await inter.response.send_message("Comment added.")

# Slash Command: Bot Information
@bot.slash_command()
async def botinfo(inter):
    embed = disnake.Embed(
        title="Bot Information 🤖",
        description="Here's some detailed information about the bot!",
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

    # Adding more bot-specific info
    guild_count = len(bot.guilds)
    member_count = sum(len(guild.members) for guild in bot.guilds)
    command_count = len(bot.commands)

    embed.add_field(name="Guilds Count 👥", value=guild_count)
    embed.add_field(name="Members Count 👤", value=member_count)
    embed.add_field(name="Commands Count ⚙️", value=command_count)

    await inter.response.send_message(embed=embed)

# Bot start
if __name__ == "__main__":
    bot.run(os.environ["BOT_TOKEN"])
