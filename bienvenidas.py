import discord
import aiohttp
from io import BytesIO
from PIL import Image, ImageDraw, ImageOps

async def send_welcome_message(member):
    """Envía un mensaje de bienvenida y la foto de perfil a los canales especificados"""
    welcome_channel_ids = [1313876205052756050, 1319095292053815338]
    role_id = 1322741281163841568

    for channel_id in welcome_channel_ids:
        welcome_channel = member.guild.get_channel(channel_id)
        if welcome_channel:
            try:
                await welcome_channel.send(f"Bienvenido {member.mention} a HYPΣɌIӨП  ɌP. ¡Esperamos que te guste!")

                avatar_url = member.avatar.url
                async with aiohttp.ClientSession() as session:
                    async with session.get(avatar_url) as response:
                        if response.status == 200:
                            avatar_bytes = await response.read()
                            avatar_image = Image.open(BytesIO(avatar_bytes))

                            background = Image.open("/home/container/hyperion_oficial_logo.png")
                            background = background.resize((800, 600))

                            avatar_image = avatar_image.resize((200, 200))
                            mask = Image.new("L", avatar_image.size, 0)
                            draw = ImageDraw.Draw(mask)
                            draw.ellipse((0, 0, avatar_image.size[0], avatar_image.size[1]), fill=255)
                            avatar_image.putalpha(mask)

                            background.paste(avatar_image, (300, 200), avatar_image)

                            output = BytesIO()
                            background.save(output, format="PNG")
                            output.seek(0)
                            await welcome_channel.send(file=discord.File(output, filename="welcome_image.png"))
            except Exception as e:
                print(f"Error al procesar el mensaje de bienvenida: {e}")

    try:
        role = discord.utils.get(member.guild.roles, id=role_id)
        if role:
            await member.add_roles(role)
    except Exception as e:
        print(f"Error al asignar el rol: {e}")
