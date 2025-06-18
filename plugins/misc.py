import os
from pyrogram import Client, filters, enums
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant, MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from utils import extract_user, get_file_id, get_poster
from datetime import datetime
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

@Client.on_message(filters.command('id'))
async def showid(client, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        user_id = message.chat.id
        first = message.from_user.first_name
        last = message.from_user.last_name or ""
        username = message.from_user.username
        dc_id = message.from_user.dc_id or ""
        await message.reply_text(
            f"<b>➲ Prénom :</b> {first}\n<b>➲ Nom :</b> {last}\n<b>➲ Nom d'utilisateur :</b> {username}\n<b>➲ ID Telegram :</b> <code>{user_id}</code>\n<b>➲ Centre de données :</b> <code>{dc_id}</code>",
            quote=True
        )

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        _id = ""
        _id += (
            "<b>➲ ID du chat :</b> "
            f"<code>{message.chat.id}</code>\n"
        )
        if message.reply_to_message:
            _id += (
                "<b>➲ ID utilisateur :</b> "
                f"<code>{message.from_user.id if message.from_user else 'Anonyme'}</code>\n"
                "<b>➲ ID de l'utilisateur répondu :</b> "
                f"<code>{message.reply_to_message.from_user.id if message.reply_to_message.from_user else 'Anonyme'}</code>\n"
            )
            file_info = get_file_id(message.reply_to_message)
        else:
            _id += (
                "<b>➲ ID utilisateur :</b> "
                f"<code>{message.from_user.id if message.from_user else 'Anonyme'}</code>\n"
            )
            file_info = get_file_id(message)
        if file_info:
            _id += (
                f"<b>{file_info.message_type}</b>: "
                f"<code>{file_info.file_id}</code>\n"
            )
        await message.reply_text(
            _id,
            quote=True
        )

@Client.on_message(filters.command(["info"]))
async def who_is(client, message):
    status_message = await message.reply_text(
        "`Récupération des informations utilisateur...`"
    )
    await status_message.edit(
        "`Traitement des informations utilisateur...`"
    )
    from_user = None
    from_user_id, _ = extract_user(message)
    try:
        from_user = await client.get_users(from_user_id)
    except Exception as error:
        await status_message.edit(str(error))
        return
    if from_user is None:
        return await status_message.edit("aucun user_id / message valide spécifié")
    message_out_str = ""
    message_out_str += f"<b>➲ Prénom :</b> {from_user.first_name}\n"
    last_name = from_user.last_name or "<b>Aucun</b>"
    message_out_str += f"<b>➲ Nom :</b> {last_name}\n"
    message_out_str += f"<b>➲ ID Telegram :</b> <code>{from_user.id}</code>\n"
    username = from_user.username or "<b>Aucun</b>"
    dc_id = from_user.dc_id or "[L'utilisateur n'a pas de photo de profil valide]"
    message_out_str += f"<b>➲ Centre de données :</b> <code>{dc_id}</code>\n"
    message_out_str += f"<b>➲ Nom d'utilisateur :</b> @{username}\n"
    message_out_str += f"<b>➲ Lien utilisateur :</b> <a href='tg://user?id={from_user.id}'><b>Cliquez ici</b></a>\n"
    if message.chat.type in ((enums.ChatType.SUPERGROUP, enums.ChatType.CHANNEL)):
        try:
            chat_member_p = await message.chat.get_member(from_user.id)
            joined_date = (
                chat_member_p.joined_date or datetime.now()
            ).strftime("%Y.%m.%d %H:%M:%S")
            message_out_str += (
                "<b>➲ A rejoint ce chat le :</b> <code>"
                f"{joined_date}"
                "</code>\n"
            )
        except UserNotParticipant:
            pass
    chat_photo = from_user.photo
    if chat_photo:
        local_user_photo = await client.download_media(
            message=chat_photo.big_file_id
        )
        buttons = [[
            InlineKeyboardButton('🔐 Fermer', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=local_user_photo,
            quote=True,
            reply_markup=reply_markup,
            caption=message_out_str,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
        os.remove(local_user_photo)
    else:
        buttons = [[
            InlineKeyboardButton('🔐 Fermer', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text=message_out_str,
            reply_markup=reply_markup,
            quote=True,
            parse_mode=enums.ParseMode.HTML,
            disable_notification=True
        )
    await status_message.delete()

@Client.on_message(filters.command(["imdb", 'search']))
async def imdb_search(client, message):
    if ' ' in message.text:
        k = await message.reply('Recherche sur ImDB...')
        r, title = message.text.split(None, 1)
        movies = await get_poster(title, bulk=True)
        if not movies:
            return await message.reply("Aucun résultat trouvé")
        btn = [
            [
                InlineKeyboardButton(
                    text=f"{movie.get('title')} - {movie.get('year')}",
                    callback_data=f"imdb#{movie.movieID}",
                )
            ]
            for movie in movies
        ]
        await k.edit('Voici ce que j\'ai trouvé sur IMDb', reply_markup=InlineKeyboardMarkup(btn))
    else:
        await message.reply('Donnez-moi un nom de film/série')

@Client.on_callback_query(filters.regex('^imdb'))
async def imdb_callback(bot: Client, quer_y: CallbackQuery):
    i, movie = quer_y.data.split('#')
    imdb = await get_poster(query=movie, id=True)
    btn = [
            [
                InlineKeyboardButton(
                    text=f"{imdb.get('title')}",
                    url=imdb['url'],
                )
            ]
        ]
    message = quer_y.message.reply_to_message or quer_y.message
    if imdb:
         caption = f"""
<b>Requête : {imdb['title']}</b>

🏷 Titre : <a href="{imdb['url']}">{imdb['title']}</a>
🎭 Genres : {imdb.get('genres', 'N/A')}
📆 Année : <a href="{imdb['url']}/releaseinfo">{imdb['year']}</a>
🌟 Note : <a href="{imdb['url']}/ratings">{imdb['rating']}</a>/10
"""
    else:
        caption = "Aucun résultat"
    if imdb.get('poster'):
        try:
            await quer_y.message.reply_photo(photo=imdb['poster'], caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg")
            await quer_y.message.reply_photo(photo=poster, caption=caption, reply_markup=InlineKeyboardMarkup(btn))
        except Exception as e:
            logger.exception(e)
            await quer_y.message.reply(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
        await quer_y.message.delete()
    else:
        await quer_y.message.edit(caption, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=False)
    await quer_y.answer()