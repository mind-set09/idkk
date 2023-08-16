import disnake
from disnake.ext import commands, tasks
from disnake import ApplicationCommandInteraction, SelectMenu, SelectOption, Button
import os

intents = disnake.Intents.all()
bot = commands.Bot(intents=intents)

class TicketStatus(disnake.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'

class TicketPriority(disnake.Enum):
    HIGH = 'High'
    MEDIUM = 'Medium'
    LOW = 'Low'

class Ticket:
    def __init__(self, priority, category, author_id, status=TicketStatus.OPEN):
        self.priority = priority
        self.category = category
        self.author_id = author_id
        self.status = status
    
    def to_embed(self):
        embed = disnake.Embed(
            title=f"Ticket Information",
            description=f"Priority: {self.priority}\nCategory: {self.category}\nStatus: {self.status}",
            color=disnake.Color.blurple()
        )
        
        embed.set_footer(text=f"Author ID: {self.author_id}")
        
        return embed

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

@bot.slash_command()
async def create(ctx):
    priority_select = SelectMenu(
        placeholder='Select priority...',
        options=[
            SelectOption(
                label='High',
                value=TicketPriority.HIGH
            ),
            SelectOption(
                label='Medium',
                value=TicketPriority.MEDIUM
            ),
            SelectOption(
                label='Low',
                value=TicketPriority.LOW
            )
        ]
    )

    category_select = SelectMenu(
        placeholder='Select category...',
        options=[
            SelectOption(
                label='Bug',
                value='bug'
            ),
            SelectOption(
                label='Feature Request',
                value='feature'
            ),
            SelectOption(
                label='Support',
                value='support'
            )
        ]
    )

    await ctx.send('Choose priority and category:',
                   components=[priority_select, category_select])

@bot.component()
async def priority_select(ctx, select):
    author_id = ctx.author.id
    priority = select.values[0]

    category_select = SelectMenu(
        placeholder='Select category...',
        options=[
            SelectOption(
                label='Bug',
                value='bug'
            ),
            SelectOption(
                label='Feature Request',
                value='feature'
            ),
            SelectOption(
                label='Support',
                value='support'
            )
        ]
    )

    await ctx.edit_origin(components=[category_select])

@bot.component()
async def category_select(ctx, select):
    author_id = ctx.author.id
    priority = ctx.message.components[0].values[0]
    category = select.values[0]

    ticket = Ticket(priority, category, author_id)

    # Implement ticket creation logic here
    # For example, you might want to save the ticket to a database
    # and send a confirmation message or embed
    
    # Placeholder confirmation message
    confirmation_message = f"Ticket created!\nPriority: {priority}\nCategory: {category}"
    await ctx.send(confirmation_message)

bot.run(os.environ['TOKEN'])
