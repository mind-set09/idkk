# Imports
import hikari
import lightbulb
import miru

import sqlalchemy
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

# Bot setup
bot = lightbulb.BotApp(token=TOKEN)
bot.load_extensions_from("./extensions")

# Load bot token from environment variable
bot_token = os.environ["BOT_TOKEN"]

# Database 
Base = declarative_base()

class Ticket(Base):
  __tablename__ = 'tickets'
  
  id = Column(Integer, primary_key=True)
  title = Column(String)
  status = Column(String)
  
# Persistent view for ticket creation  
@bot.command
@lightbulb.command('tickets', 'Ticket system commands')
@lightbulb.implements(lightbulb.SlashCommandGroup)
async def tickets(ctx):

  persistent_view = miru.View()
  persistent_view.add_item(
    miru.Button(label="Create Ticket", custom_id="create_ticket")
  )
  await ctx.respond(views=persistent_view)
  
# Modal for ticket creation  
@bot.component()
async def create_ticket_modal(ctx):

  modal = miru.Modal("Create Ticket")
  
  title_input = miru.TextInput(label="Title")
  desc_input = miru.TextInput(label="Description")
  
  modal.add_input(title_input)
  modal.add_input(desc_input)
  
  await ctx.respond(modal=modal)
  
# Ticket created embed   
@bot.component()  
async def ticket_created(ctx):

  embed = hikari.Embed(title=TITLE, description=DESC)
  
  await ctx.edit_response(embed=embed)
  
# Approval buttons 
approve_button = miru.Button(label="Approve")
deny_button = miru.Button(label="Deny")

await ctx.edit_response(components=[approve_button, deny_button])

# Logging
import logging

logger = logging.getLogger('bot')
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler('bot.log')
logger.addHandler(file_handler) 

logger.info("Bot started")

bot.run()
