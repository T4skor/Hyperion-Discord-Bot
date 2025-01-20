import discord
from discord.ext import commands
from discord import app_commands
import os
from tickets import send_ticket_menu
from whitelist import wl
from bienvenidas import send_welcome_message

intents = discord.Intents.default()
intents.members = True 

bot = commands.Bot(command_prefix="!", intents=intents)

# Función para cambiar los roles de un usuario
async def aceptar_rol(interaction: discord.Interaction, usuario: discord.User):
    """Función para cambiar los roles de un usuario específico."""
    # Verificar si el usuario que ejecuta el comando tiene permisos de administrador o el rol específico
    if not interaction.user.guild_permissions.administrator and not any(role.id == 1319924341328187454 for role in interaction.user.roles):
        await interaction.response.send_message("No tienes permisos para ejecutar este comando.", ephemeral=True)
        return

    # Obtiene el servidor (guild) donde se ejecutó el comando
    guild = interaction.guild
    
    # Define los roles por ID
    rol_quitar_id = 1317278752245415997
    rol_poner_id = 1313927020727636024

    # Obtiene los roles por ID
    rol_quitar = guild.get_role(rol_quitar_id)
    rol_poner = guild.get_role(rol_poner_id)

    if rol_quitar is None or rol_poner is None:
        await interaction.response.send_message("Uno de los roles no fue encontrado.", ephemeral=True)
        return

    # Intenta quitar el rol y poner el nuevo rol al usuario
    member = guild.get_member(usuario.id)
    if member:
        await member.remove_roles(rol_quitar)
        await member.add_roles(rol_poner)
        await interaction.response.send_message(f"El rol de {usuario.mention} ha sido actualizado correctamente.", ephemeral=True)

        # Enviar mensaje al canal de aceptación
        acceptance_channel = guild.get_channel(1314248677639848026)
        if acceptance_channel:
            await acceptance_channel.send(f"{usuario.mention} ha sido aceptado :white_check_mark:")
        else:
            await interaction.response.send_message("El canal de aceptación no se encontró.", ephemeral=True)

    else:
        await interaction.response.send_message("El usuario no se encuentra en el servidor.", ephemeral=True)

# Comando slash para ejecutar la función de cambiar roles
@bot.tree.command(name="wl-aceptar")
async def wl_aceptar(interaction: discord.Interaction, usuario: discord.User):
    """Comando para cambiar roles al usuario especificado."""
    await aceptar_rol(interaction, usuario)

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

    ticket_channel_id = 1313929987597930568
    whitelist_channel_id = 1314249120365543548
    ticket_channel = bot.get_channel(ticket_channel_id)
    whitelist_channel = bot.get_channel(whitelist_channel_id)

    if ticket_channel:
        file_path = "/home/container/logo.png"
        await send_ticket_menu(ticket_channel, file_path)  
    
    if whitelist_channel:
        await wl(whitelist_channel)
    else:
        print(f"Error: Canal de whitelist con ID {whitelist_channel_id} no encontrado.")

# Inicia el bot
bot.run(TOKEN)
