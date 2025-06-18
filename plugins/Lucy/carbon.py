import aiohttp
from io import BytesIO
from pyrogram import Client, filters



async def make_carbon(code):
    url = "https://carbonara.solopov.dev/api/cook"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json={"code": code}) as resp:
            image = BytesIO(await resp.read())
    image.name = "carbon.png"
    return image



@Client.on_message(filters.command("carbon"))
async def _carbon(client, message):
    replied = message.reply_to_message
    if not replied:
        await message.reply_text("**Répondez à un message texte pour créer un Carbon..**")
        return
    if not (replied.text or replied.caption):
        return await message.reply_text("**Répondez à un message texte pour créer un Carbon..**")
    text = await message.reply("Processing...")
    carbon = await make_carbon(replied.text or replied.caption)
    await text.edit("**Téléversement...**")
    await message.reply_photo(carbon)
    await text.delete()
    carbon.close()
