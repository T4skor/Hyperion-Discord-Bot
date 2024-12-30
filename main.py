import discord
from discord.ext import commands
from discord import app_commands
import os
from tickets import send_ticket_menu
from whitelist import wl
from bienvenidas import send_welcome_message
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    """Llamada cuando un miembro se une al servidor."""
    await send_welcome_message(member)

@bot.event
async def on_ready():
    """Llamada cuando el bot está listo y conectado."""

    await bot.change_presence(activity=discord.Game(name="HyperionRP"))
    
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Error al sincronizar comandos slash: {e}")

    ticket_channel_id = 1322694316019290174
    whitelist_channel_id = 1322978279921156286
    ticket_channel = bot.get_channel(ticket_channel_id)
    whitelist_channel = bot.get_channel(whitelist_channel_id)

    if ticket_channel:
        file_path = "logo.png"
        await send_ticket_menu(ticket_channel, file_path)  
    
    if whitelist_channel:
        await wl(whitelist_channel)
    else:
        print(f"Error: Canal de whitelist con ID {whitelist_channel_id} no encontrado.")

bot.run(DISCORD_TOKEN)
