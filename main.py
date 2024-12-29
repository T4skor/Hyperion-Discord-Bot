import discord
from discord.ext import commands
from discord import app_commands
import os
from tickets import send_ticket_menu  # Importamos la función de tickets.py
from bienvenidas import send_welcome_message  # Importamos la función de bienvenida

# Leer el token desde el archivo
with open(r"C:\Users\fanta\Desktop\Programas\Discord\Hyperion\token.txt", "r") as file:
    TOKEN = file.read().strip()

# Configuración de los intents
intents = discord.Intents.default()
intents.members = True  # Necesario para eventos relacionados con miembros

# Crear el bot
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_member_join(member):
    """Llamada cuando un miembro se une al servidor."""
    await send_welcome_message(member)

@bot.event
async def on_ready():
    """Llamada cuando el bot está listo y conectado."""
    # Cambiar el estado del bot
    await bot.change_presence(activity=discord.Game(name="HyperionRP"))
    
    # Sincronización de comandos slash
    try:
        synced = await bot.tree.sync()
        print(f"Comandos slash sincronizados: {len(synced)} comandos")
    except Exception as e:
        print(f"Error al sincronizar comandos slash: {e}")

    # Enviar el menú de tickets
    channel_id = 1322694316019290174  # ID del canal donde enviar el mensaje de tickets
    channel = bot.get_channel(channel_id)

    if channel:
        file_path = r"C:\Users\fanta\Desktop\Programas\Discord\Hyperion\logo.png"  # Ruta de la imagen
        await send_ticket_menu(channel, file_path)  # Llamamos a la función para enviar el menú
    else:
        print(f"Error: Canal con ID {channel_id} no encontrado.")

# Ejecutar el bot
bot.run(TOKEN)
