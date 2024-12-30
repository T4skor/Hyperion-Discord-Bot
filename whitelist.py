import discord
from discord.ui import Button, View

ticket_count = {
    "whitelist": 0
}

async def wl(channel):
    """Función para crear un ticket de whitelist con un botón."""
    try:
        embed = discord.Embed(
            description="Haz clic en el botón para abrir una solicitud de whitelist",
            color=discord.Color.yellow()
        )

        button = Button(label="📝 Solicitar Whitelist", style=discord.ButtonStyle.primary)

        async def button_callback(interaction: discord.Interaction):
            try:
                guild = interaction.guild
                author = interaction.user
                category = discord.utils.get(guild.categories, name="Tickets")

                if not category:
                    category = await guild.create_category("Tickets")

                ticket_count["whitelist"] += 1
                ticket_number = str(ticket_count["whitelist"]).zfill(3)

                for channel in category.channels:
                    if channel.name.startswith(f"ticket-{author.name.lower()}"):
                        return await interaction.response.send_message("Ya tienes un ticket abierto.", ephemeral=True)

                ticket_channel = await category.create_text_channel(
                    f"ticket-{author.name.lower()}-whitelist-{ticket_number}",
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

                await ticket_channel.send(f"¡Hola {author.mention}! Enseguida alguien atenderá tu solicitud.")
                await ticket_channel.send(
                    embed=discord.Embed(
                        description="Usa el botón de abajo para cerrar este ticket cuando hayas terminado.",
                        color=discord.Color.green()
                    ),
                    view=ticket_view
                )

                await interaction.response.send_message(
                    f"Tu ticket de whitelist #{ticket_number} ha sido creado.", ephemeral=True
                )

            except Exception as e:
                print(f"Error: {e}")
                await interaction.response.send_message("Hubo un error al procesar tu solicitud.", ephemeral=True)

        button.callback = button_callback

        view = View(timeout=None)
        view.add_item(button)

        await channel.send(embed=embed, view=view)

    except Exception as e:
        print(f"Error al enviar el mensaje: {e}")
