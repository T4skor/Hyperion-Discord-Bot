import discord
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps

async def send_welcome_message(member):
    """Envía un mensaje de bienvenida y la foto de perfil al canal de bienvenida"""
    welcome_channel_id = 1322734453679980625  # Reemplaza con el ID de tu canal de bienvenida
    role_id = 1322741281163841568  # ID del rol a asignar

    welcome_channel = member.guild.get_channel(welcome_channel_id)
    if welcome_channel:
        # Enviar mensaje de bienvenida
        await welcome_channel.send(f"Bienvenido {member.mention} a HYPΣɌIӨП  ɌP Esperamos que te guste!")
        
        # Descargar la foto de perfil
        avatar_url = member.avatar.url  # Obtener la URL de la foto de perfil
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar_url) as response:
                if response.status == 200:
                    avatar_bytes = await response.read()
                    avatar_image = Image.open(BytesIO(avatar_bytes))

                    # Imagen de fondo
                    background = Image.open(r"C:\Users\fanta\Desktop\Programas\Discord\Hyperion\hyperion_oficial_logo.png")  # Pon la ruta de la imagen de fondo aquí
                    background = background.resize((800, 600))  # Redimensiona la imagen de fondo según sea necesario

                    # Redimensiona la foto de perfil para el círculo
                    avatar_image = avatar_image.resize((200, 200))  # Redimensiona el avatar

                    # Crear un círculo para recortar el avatar
                    mask = Image.new("L", avatar_image.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, avatar_image.size[0], avatar_image.size[1]), fill=255)

                    # Aplicar la máscara al avatar para hacerlo circular
                    avatar_image.putalpha(mask)

                    # Crear una nueva imagen combinando el fondo y el avatar
                    background.paste(avatar_image, (300, 200), avatar_image)  # Pega el avatar en el fondo en la posición deseada

                    # Guardar la imagen combinada en un objeto BytesIO
                    output = BytesIO()
                    background.save(output, format="PNG")
                    output.seek(0)

                    # Enviar la imagen combinada
                    await welcome_channel.send(file=discord.File(output, filename="welcome_image.png"))

    # Asignar el rol por ID
    role = discord.utils.get(member.guild.roles, id=role_id)
    if role:
        await member.add_roles(role)
