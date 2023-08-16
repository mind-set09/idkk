import disnake
from disnake.ext import commands, tasks
from disnake.ui import View, Button

bot = commands.Bot(command_prefix='!')

class TicketStatus(disnake.Enum):
    OPEN = 'Open'
    IN_PROGRESS = 'In Progress'
    CLOSED = 'Closed'

class TicketCategory(disnake.Enum):
    BUG_REPORT = 'Bug Report'
    FEATURE_REQUEST = 'Feature Request'

class TicketPriority(disnake.Enum):
    LOW = 'Low'
    MEDIUM = 'Medium'
    HIGH = 'High'


class Ticket:
    def __init__(self, author_id, category, priority):
        self.id = len(tickets) + 1
        self.author_id = author_id
        self.category = category
        self.priority = priority
        self.status = TicketStatus.OPEN
        self.assigned_to = None
        self.created_at = disnake.utils.utcnow()
        self.comments = []
        self.tags = []

    def to_embed(self):
        embed = disnake.Embed(title=f'Ticket #{self.id}', color=disnake.Color.green())
        embed.add_field(name='Status', value=self.status.value, inline=True)
        embed.add_field(name='Category', value=self.category.value, inline=True)
        embed.add_field(name='Priority', value=self.priority.value, inline=True)
        embed.add_field(name='Assigned To', value=self.assigned_to.mention if self.assigned_to else 'Unassigned', inline=True)
        embed.add_field(name='Created At', value=self.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)

        if self.comments:
            comment_str = '\n'.join([f'**{comment[0]}**: {comment[1]}' for comment in self.comments])
            embed.add_field(name='Comments', value=comment_str, inline=False)

        if self.tags:
            tags_str = ', '.join(self.tags)
            embed.add_field(name='Tags', value=tags_str, inline=False)

        return embed

    def update(self, **kwargs):
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

tickets = []
categories = {}
moderator_role = None
automated_responses = {
    'help': 'Thank you for reaching out for help. We will assist you shortly.',
    'urgent': 'Your request has been marked as urgent. Please wait for our response.'
}

@bot.event
async def on_ready():
    global categories, moderator_role
    categories = {TicketCategory.BUG_REPORT: disnake.Color.red(), TicketCategory.FEATURE_REQUEST: disnake.Color.blue()}
    moderator_role = discord.utils.get(bot.guild.roles, name='Moderator')  # Replace 'Moderator' with your role name

@bot.slash_command()
async def tickets(ctx):
    embed = disnake.Embed(title='Ticket List', description='List of open tickets:', color=disnake.Color.green())
    for ticket in tickets:
        if ticket.status == TicketStatus.OPEN:
            embed.add_field(name=f'Ticket #{ticket.id}', value=f'Category: {ticket.category.value}\nStatus: {ticket.status.value}', inline=False)
    await ctx.send(embed=embed)

@bot.slash_command()
async def create(ctx):
    priority_select = Select(
        placeholder='Select priority',
        options=[Option(label=priority.value, value=priority.value) for priority in TicketPriority],
        custom_id='priority_select'
    )
    category_select = Select(
        placeholder='Select a category',
        options=[Option(label=category.value, value=category.value) for category in TicketCategory],
        custom_id='category_select'
    )
    await ctx.send('Choose a priority and category for your ticket:', components=[ActionRow(components=[priority_select, category_select])])

@bot.select_option()
async def priority_select(int, select):
    author_id = int.author.id
    priority = TicketPriority(select.values[0])
    int.data['priority'] = priority
    int.data['author_id'] = author_id
    category_select = Select(
        placeholder='Select a category',
        options=[Option(label=category.value, value=category.value) for category in TicketCategory],
        custom_id='category_select'
    )
    await int.edit(components=[ActionRow(components=[category_select])])

@bot.select_option()
async def category_select(int, select):
    author_id = int.data.get('author_id')
    priority = int.data.get('priority')
    category = TicketCategory(select.values[0])

    new_ticket = Ticket(author_id, category, priority)
    tickets.append(new_ticket)

    embed = new_ticket.to_embed()
    await int.edit_origin(embed=embed, components=[])

@bot.slash_command()
async def close(ctx, ticket_id: int):
    ticket = discord.utils.find(lambda t: t.id == ticket_id, tickets)
    if ticket:
        ticket.update(status=TicketStatus.CLOSED)
        await ctx.send(f'Ticket #{ticket_id} has been closed.')
    else:
        await ctx.send('Invalid ticket ID.')

@bot.slash_command()
async def comment(ctx, ticket_id: int, *, msg):
    ticket = discord.utils.find(lambda t: t.id == ticket_id, tickets)
    if ticket:
        if msg.lower() in automated_responses:
            await ctx.send(automated_responses[msg.lower()])
            return
        ticket.comments.append((ctx.author.display_name, msg))
        await ctx.send(f'Comment added to ticket #{ticket_id}.')
    else:
        await ctx.send('Invalid ticket ID.')

@bot.slash_command()
async def tag(ctx, ticket_id: int, *, tag):
    ticket = discord.utils.find(lambda t: t.id == ticket_id, tickets)
    if ticket:
        ticket.tags.append(tag)
        await ctx.send(f'Tag "{tag}" added to ticket #{ticket_id}.')
    else:
        await ctx.send('Invalid ticket ID.')

@bot.component()
async def handle_button(int, btn):
    if btn.custom_id.startswith('assign_'):
        ticket_id = int(btn.custom_id.split('_')[1])
        ticket = discord.utils.find(lambda t: t.id == ticket_id, tickets)
        
        if ticket:
            if moderator_role in int.author.roles:
                assigned_user = int.author
                ticket.update(assigned_to=assigned_user)
                await btn.edit_origin(embed=ticket.to_embed())
                await btn.send(f'Ticket #{ticket_id} has been assigned to you, {assigned_user.mention}.')
            else:
                await btn.send('You need to be a moderator to assign tickets.')

@tasks.loop(hours=12)
async def maintenance():
    for ticket in tickets:
        if ticket.status == TicketStatus.IN_PROGRESS:
            time_elapsed = disnake.utils.utcnow() - ticket.created_at
            if time_elapsed.days >= 1:
                ticket.update(status=TicketStatus.OPEN)

@tasks.loop(minutes=30)
async def notifications():
    for ticket in tickets:
        if ticket.status == TicketStatus.IN_PROGRESS and ticket.assigned_to and ticket.assigned_to.status == disnake.Status.online:
            await ticket.assigned_to.send(f'Reminder: You have an ongoing ticket: {ticket.category.value}')


bot.run(os.environ['TOKEN'])
