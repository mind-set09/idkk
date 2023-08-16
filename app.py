from discord import Interaction
from discord import Interaction, ButtonStyle
from discord.ext import commands, tasks
from discord_interactions import InteractionClient, Button, SelectMenu
import os

bot = commands.Bot(command_prefix="!")
DiscordComponents(bot)

active_tickets = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.command()
async def create_ticket(ctx):
    embed = discord.Embed(title="New Ticket", description="Click the button to create a new ticket.", color=discord.Color.blue())
    ticket_button = Button(style=ButtonStyle.blue, label="Create Ticket", custom_id="create_ticket")
    await ctx.send(embed=embed, components=[ticket_button])

@bot.event
async def on_button_click(ctx):
    if ctx.custom_id == "create_ticket":
        ticket_number = len(active_tickets) + 1
        active_tickets[ticket_number] = {
            "author_id": ctx.author.id,
            "status": "Open"
        }

        embed = discord.Embed(title=f"Ticket #{ticket_number}", description="Your ticket has been created.", color=discord.Color.green())
        embed.add_field(name="Status", value="Open", inline=True)
        embed.add_field(name="Assigned to", value="Unassigned", inline=True)
        embed.add_field(name="Description", value="No description provided.", inline=False)

        close_button = Button(style=ButtonStyle.red, label="Close Ticket", custom_id=f"close_ticket_{ticket_number}")
        assign_button = Button(style=ButtonStyle.grey, label="Assign to Me", custom_id=f"assign_ticket_{ticket_number}")

        await ctx.send(embed=embed, components=[close_button, assign_button])

@bot.event
async def on_button_click(ctx):
    if ctx.custom_id.startswith("close_ticket_"):
        ticket_number = int(ctx.custom_id.split("_")[2])
        ticket = active_tickets.get(ticket_number)

        if ticket and ticket["author_id"] == ctx.author.id:
            ticket["status"] = "Closed"
            await ctx.edit_origin(embed=generate_ticket_embed(ticket_number))
            await ctx.send("Ticket closed.")
        else:
            await ctx.send("You don't have permission to close this ticket.")

    elif ctx.custom_id.startswith("assign_ticket_"):
        ticket_number = int(ctx.custom_id.split("_")[2])
        ticket = active_tickets.get(ticket_number)

        if ticket:
            ticket["assigned_to"] = ctx.author.id
            await ctx.edit_origin(embed=generate_ticket_embed(ticket_number))
            await ctx.send("Ticket assigned to you.")
        else:
            await ctx.send("Ticket not found.")

def generate_ticket_embed(ticket_number):
    ticket = active_tickets.get(ticket_number)
    if not ticket:
        return None

    embed = discord.Embed(title=f"Ticket #{ticket_number}", color=discord.Color.green())
    embed.add_field(name="Status", value=ticket["status"], inline=True)
    
    assigned_to = bot.get_user(ticket.get("assigned_to", 0))
    embed.add_field(name="Assigned to", value=assigned_to.name if assigned_to else "Unassigned", inline=True)

    embed.add_field(name="Description", value="No description provided.", inline=False)
    return embed


bot.run(os.environ['TOKEN'])
