import os
from datetime import datetime

import disnake
from disnake import SlashCommandGroup, Option 
from disnake.ext import commands, tasks
import sqlite3

info_commands = SlashCommandGroup("info", "System information commands")

@info_commands.command()
async def system(ctx):

  cpu = psutil.cpu_percent()
  mem = psutil.virtual_memory()
  disk = psutil.disk_usage('/')
  net_io = psutil.net_io_counters()

  embed = disnake.Embed(title="System Information")

  embed.add_field(name="CPU", value=f"{cpu}% Usage")

  embed.add_field(name="RAM", value=f"{mem.used/1024**2:,.2f}MB Used")  

  embed.add_field(name="Disk", value=f"{disk.used/1024**2:,.2f}GB Used")

  embed.add_field(name="Network", 
                  value=f"Sent: {net_io.bytes_sent/1024**2:,.2f}MB Received: {net_io.bytes_recv/1024**2:,.2f}MB")

  if gpu := psutil.gpu():
    embed.add_field(name="GPU", value=gpu.name)
      
  view = disnake.ui.View()

  support_btn = disnake.ui.Button(
    label="Support Server", 
    url="https://discord.gg/WsGgGUyfTV"
  )

  view.add_item(support_btn)

  invite_btn = disnake.ui.Button(
    label="Invite Bot",
    url=f"https://discord.com/oauth2/authorize?client_id={bot.user.id}&scope=applications.commands%20bot" 
  )

  view.add_item(invite_btn)

  await ctx.respond(embed=embed, view=view)

bot.tree.add_command(info_commands)

class Ticket:
  def __init__(self, id, description, status, due_date=None):
    self.id = id
    self.description = description
    self.status = status
    self.due_date = due_date

  @classmethod
  def from_dict(cls, data):
    return cls(data['id'], data['description'], data['status'], data['due_date'])

class Database:
  def __init__(self):
    self.conn = sqlite3.connect('tickets.db')
    self.cur = self.conn.cursor()

  def create_tables(self):
    self.cur.execute("""
      CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY, 
        description TEXT,
        status TEXT, 
        due_date TEXT
      )
    """)

  async def create_ticket(self, ticket):
    self.cur.execute("INSERT INTO tickets VALUES (?, ?, ?, ?)", 
      (ticket.id, ticket.description, ticket.status, ticket.due_date))
    self.conn.commit()

  # Other database methods

  async def close(self):
    self.conn.close()

bot = commands.Bot(command_prefix='!')
db = Database()

ticket_commands = SlashCommandGroup("ticket", "Ticket commands")

@bot.event
async def on_ready():
  db.create_tables()
  print("Bot ready")

@ticket_commands.command()
async def create(ctx, description: str, due_date: Option(datetime, "Leave empty for none")):
  ticket = Ticket(len(db.get_tickets()) + 1, description, "open", due_date)
  await db.create_ticket(ticket)
  await ctx.respond(f"Ticket {ticket.id} created")

@ticket_commands.command() 
async def list(ctx):
  tickets = db.get_tickets()
  embed = disnake.Embed(title="Open Tickets")
  for ticket in tickets:
    embed.add_field(name=ticket.id, value=f"{ticket.description} - Due: {ticket.due_date}")
  await ctx.respond(embed=embed)

# Other commands

@tasks.loop(minutes=15)
async def check_tickets():

  now = datetime.now()

  tickets = db.get_tickets()

  for ticket in tickets:
    if ticket.status == "open" and ticket.due_date < now:
      ticket.status = "overdue"
      await db.update_ticket(ticket)

  await bot.get_channel(channel_id).send("Overdue tickets!")

@bot.event
async def on_slash_command_error(ctx, error):
  await ctx.send(f"Error: {error}")

bot.tree.add_command(ticket_commands)
bot.run(os.getenv("TOKEN"))
