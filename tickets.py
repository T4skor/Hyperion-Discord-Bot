import discord
from discord.ui import Button, View, Select
from discord import app_commands

ticket_count = {
    "soporte": 0,
    "donacion": 0,
    "negocio": 0,
    "devolucion": 0,
    "ilicito": 0,
    "staff": 0,
    "ems": 0,  
    "policia": 0,
    "playmaker": 0
}

async def send_ticket_menu(channel, file_path):
    embed = discord.Embed(
        description="Selecciona a tu preferencia qué ticket deseas abrir",
        color=discord.Color.yellow()
    )

    file = discord.File(file_path, filename="logo.png")
    embed.set_image(url="attachment://logo.png")

    select = Select(
        placeholder="Seleccionar opciones",
        min_values=1,
        max_values=1,
        options=[
            discord.SelectOption(label="🛠️ Soporte", value="soporte"),
            discord.SelectOption(label="💲 Donación", value="donacion"),
            discord.SelectOption(label="🍴 Negocio", value="negocio"),
            discord.SelectOption(label="🔄 Devolución", value="devolucion"),
            discord.SelectOption(label="💣 Ilícito", value="ilicito"),
            discord.SelectOption(label="👑 Postulación Staff", value="staff"),
            discord.SelectOption(label="🏥 Postulación EMS", value="ems"),
            discord.SelectOption(label="👮 Postulación Policía", value="policia"),
            discord.SelectOption(label="💻 Postulación PlayMaker", value="playmaker"),
        ]
    )

    async def select_callback(interaction: discord.Interaction):
        try:
            selected_value = select.values[0]
            guild = interaction.guild
            author = interaction.user
            category = discord.utils.get(guild.categories, name="Tickets")

            if not category:
                category = await guild.create_category("Tickets")

            if selected_value not in ticket_count:
                ticket_count[selected_value] = 0

            ticket_count[selected_value] += 1
            ticket_number = str(ticket_count[selected_value]).zfill(3)

            for channel in category.channels:
                if channel.name.startswith(f"ticket-{author.name.lower()}"):
                    return await interaction.response.send_message("Ya tienes un ticket abierto.", ephemeral=True)

            ticket_channel = await category.create_text_channel(
                f"ticket-{author.name.lower()}-{selected_value}-{ticket_number}",
                overwrites={
                    guild.default_role: discord.PermissionOverwrite(view_channel=False),
                    author: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                    guild.me: discord.PermissionOverwrite(view_channel=True, send_messages=True, read_message_history=True),
                }
            )

            close_button = Button(label="🔒 Cerrar Ticket", style=discord.ButtonStyle.danger)

            async def close_callback(interaction: discord.Interaction):
                if interaction.channel == ticket_channel:
                    await interaction.response.send_message("El ticket ha sido cerrado.", ephemeral=True)
                    await ticket_channel.delete()
                else:
                    await interaction.response.send_message("Este no es el canal del ticket.", ephemeral=True)

            close_button.callback = close_callback

            ticket_view = View(timeout=None)

            ticket_view.add_item(close_button)

            await ticket_channel.send(f"¡Hola {author.mention}! Enseguida alguien se ocupará de tu ticket. ¿Cuál es tu consulta?")

            embed_ticket = discord.Embed(
                description=" ",
                color=discord.Color.green()
            )

            embed_ticket.add_field(
                name="El soporte estará con usted en breve.",
                value="Para cerrar este ticket reacciona con 🔒",
                inline=False
            )

            await ticket_channel.send(
                embed=embed_ticket,
                view=ticket_view
            )

            await interaction.response.send_message(f"Se ha creado tu ticket para {selected_value} #{ticket_number}.", ephemeral=True)

        except Exception as e:
            print(f"Error en el callback: {e}")
            await interaction.response.send_message("Hubo un error al procesar tu solicitud.", ephemeral=True)

    select.callback = select_callback

    view = View(timeout=None)
    view.add_item(select)

    await channel.send(embed=embed, view=view, file=file)
