import discord
from discord.ext import commands, tasks
from discord_components import *
import os

bot = commands.Bot(command_prefix='!')
DiscordComponents(bot)

class Ticket:
    def __init__(self, author_id, category):
        self.author_id = author_id
        self.category = category
        self.status = 'Open'
        self.created_at = datetime.datetime.now()
        self.comments = []

    def to_embed(self):
        embed = discord.Embed(title=f'Ticket #{len(tickets) + 1}', color=discord.Color.green())
        embed.add_field(name='Status', value=self.status, inline=True)
        embed.add_field(name='Category', value=self.category, inline=True)
        embed.add_field(name='Created At', value=self.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        if self.comments:
            comment_str = '\n'.join([f'**{comment[0]}**: {comment[1]}' for comment in self.comments])
            embed.add_field(name='Comments', value=comment_str, inline=False)

        return embed

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

tickets = []
categories = {}

@bot.event
async def on_ready():
    global categories
    categories = {'Bug Report': discord.Color.red(), 'Feature Request': discord.Color.blue()}

@bot.slash_command()
async def tickets(ctx):
    embed = discord.Embed(title='Ticket List', description='List of open tickets:', color=discord.Color.green())
    for i, ticket in enumerate(tickets):
        if ticket.status == 'Open':
            embed.add_field(name=f'Ticket #{i + 1}', value=f'Category: {ticket.category}\nStatus: {ticket.status}', inline=False)
    await ctx.send(embed=embed)

@bot.slash_command()
async def create(ctx):
    category_select = Select(
        placeholder='Select a category',
        options=[Option(label=category, value=category) for category in categories.keys()],
        custom_id='category_select'
    )
    await ctx.send('Choose a category for your ticket:', components=[category_select])

@bot.select_option()
async def category_select(int, select):
    author_id = int.author.id
    category = select.values[0]

    new_ticket = Ticket(author_id, category)
    tickets.append(new_ticket)

    embed = new_ticket.to_embed()
    await int.edit_origin(embed=embed, components=[])

@bot.command()
async def close(ctx, id: int):
    if 1 <= id <= len(tickets):
        ticket = tickets[id - 1]
        ticket.update(status='Closed')
        await ctx.send(f'Ticket #{id} has been closed.')
    else:
        await ctx.send('Invalid ticket ID.')

@bot.command()
async def comment(ctx, id: int, *, msg):
    if 1 <= id <= len(tickets):
        ticket = tickets[id - 1]
        ticket.comments.append((ctx.author.display_name, msg))
        await ctx.send(f'Comment added to ticket #{id}.')
    else:
        await ctx.send('Invalid ticket ID.')

@bot.component()
async def handle_button(int, btn):
    if btn.custom_id.startswith('ticket_'):
        ticket_id = int(btn.custom_id.split('_')[1])
        ticket = tickets[ticket_id - 1]
        
        if ticket.status == 'Open':
            ticket.update(status='In Progress')
        else:
            ticket.update(status='Open')
        
        await btn.edit_origin(embed=ticket.to_embed())

@tasks.loop(hours=12)
async def maintenance():
    for ticket in tickets:
        if ticket.status == 'In Progress':
            time_elapsed = datetime.datetime.now() - ticket.created_at
            if time_elapsed.days >= 1:
                ticket.update(status='Open')

@tasks.loop(minutes=30)
async def notifications():
    for ticket in tickets:
        if ticket.status == 'In Progress':
            assigned_user = None  # Get the assigned user for the ticket
            if assigned_user and assigned_user.status == discord.Status.online:
                await assigned_user.send(f'Reminder: You have an ongoing ticket: {ticket.category}')


bot.run(os.environ['TOKEN'])
