import disnake
from disnake.ext import commands
import asyncio

from sqlalchemy import Column, Integer, String
from database import Base, Session

engine = create_engine('sqlite:///database.db') # or other DB connection string

db = SQLAlchemy(engine)

# Database models
class Ticket(Base):
  __tablename__ = 'tickets'

  id = Column(Integer, primary_key=True)
  title = Column(String)
  description = Column(String)
  author_id = Column(Integer)
  status = Column(String)

Base.metadata.create_all(engine) 
class Comment(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  ticket_id = db.Column(db.Integer, db.ForeignKey('ticket.id'))
  text = db.Column(db.String)
  
# Ticket creation 
create_view = CreateTicketView()

@bot.command()
async def new(ctx):
  await ctx.send("Create a ticket!", view=create_view)

# Persistent create ticket view  
class CreateTicketView(disnake.ui.View):

  @disnake.ui.button(label="Create Ticket")
  async def create(self, button, inter):
    
    modal = CreateTicketModal()
    await inter.response.send_modal(modal)
    
    await modal.callback(inter)

# Ticket creation modal
class CreateTicketModal(disnake.ui.Modal):
  title = disnake.ui.TextInput(label="Title")
  description = disnake.ui.TextInput(label="Description")

  async def callback(self, inter):
    title = self.title.value
    desc = self.description.value
    
    ticket = Ticket(title=title, desc=desc, author_id=inter.author.id)
    db.session.add(ticket)
    db.session.commit()
    
    await inter.send("Ticket created!")

# Ticket message    
@bot.event
async def on_ticket_create(ticket):

  embed = disnake.Embed(title=ticket.title, desc=ticket.desc)
  
  approve = disnake.ui.Button(label="Approve")
  deny = disnake.ui.Button(label="Deny")
  
  msg = await inter.channel.send(embed=embed, view=disnake.ui.View(approve, deny))
  
  # Callbacks
  @bot.component("approve")
  async def approve(inter):
    ticket.status = "Approved"
    db.session.commit()
   
  @bot.component("deny") 
  async def deny(inter):
    ticket.status = "Denied"
    db.session.commit()

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


if __name__ == "__main__":
    bot.run(os.environ["BOT_TOKEN"])
    app.run()
