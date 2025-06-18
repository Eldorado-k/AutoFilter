from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ForceReply, CallbackQuery
from info import URL, LOG_CHANNEL
from urllib.parse import quote_plus
from LucyBot.util.file_properties import get_name, get_hash, get_media_file_size
from LucyBot.util.human_readable import humanbytes
import humanize
import random

@Client.on_message(filters.private & filters.command("stream"))
async def stream_start(client, message):
    msg = await client.ask(message.chat.id, "**Envoyez-moi maintenant votre fichier/vidéo pour obtenir les liens de streaming et téléchargement**")
    if not msg.media:
        return await message.reply("**Veuillez envoyer un média pris en charge.**")
    if msg.media in [enums.MessageMediaType.VIDEO, enums.MessageMediaType.DOCUMENT]:
        file = getattr(msg, msg.media.value)
        filename = file.file_name
        filesize = humanize.naturalsize(file.file_size) 
        fileid = file.file_id
        user_id = message.from_user.id
        username =  message.from_user.mention 

        log_msg = await client.send_cached_media(
            chat_id=LOG_CHANNEL,
            file_id=fileid,
        )
        fileName = {quote_plus(get_name(log_msg))}
        stream = f"{URL}watch/{str(log_msg.id)}?hash={get_hash(log_msg)}"
        download = f"{URL}{str(log_msg.id)}?hash={get_hash(log_msg)}"
 
        await log_msg.reply_text(
            text=f"•• Lien généré pour l'ID #{user_id} \n•• Utilisateur : {username} \n\n•• Nom du fichier : {fileName}",
            quote=True,
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Téléchargement rapide 🚀", url=download),
                                                InlineKeyboardButton('🖥️ Voir en ligne 🖥️', url=stream)]])
        )
        rm=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Stream 🖥", url=stream),
                    InlineKeyboardButton('Télécharger 📥', url=download)
                ]
            ] 
        )
        msg_text = """<i><u>Vos liens ont été générés !</u></i>\n\n<b>📂 Nom du fichier :</b> <i>{}</i>\n\n<b>📦 Taille du fichier :</b> <i>{}</i>\n\n<b>📥 Téléchargement :</b> <i>{}</i>\n\n<b>🖥 Visionnage :</b> <i>{}</i>\n\n<b>🚸 Note : Le lien n'expirera pas tant que je ne le supprime pas</b>\n\nPar @BotZFlix"""

        await message.reply_text(text=msg_text.format(get_name(log_msg), humanbytes(get_media_file_size(msg)), download, stream), quote=True, disable_web_page_preview=True, reply_markup=rm)