import asyncio
import re
import ast
import math
import random
import pytz
from datetime import datetime, timedelta, date, time
lock = asyncio.Lock()
from database.users_chats_db import db
from database.refer import referdb
from pyrogram.errors.exceptions.bad_request_400 import MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty
from Script import script
import pyrogram
from database.connections_mdb import active_connection, all_connections, delete_connection, if_active, make_active, \
    make_inactive
from info import *
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, InputMediaPhoto, WebAppInfo
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait, UserIsBlocked, MessageNotModified, PeerIdInvalid
from utils import *
from fuzzywuzzy import process
from database.users_chats_db import db
from database.config_db import mdb
from database.ia_filterdb import Media, Media2, get_file_details, get_search_results, get_bad_files
from database.filters_mdb import (
    del_all,
    find_filter,
    get_filters,
)
from database.gfilters_mdb import (
    find_gfilter,
    get_gfilters,
    del_allg
)
import logging
from urllib.parse import quote_plus
from LucyBot.util.file_properties import get_name, get_hash, get_media_file_size
from database.config_db import mdb
logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

import requests
import string
import tracemalloc

tracemalloc.start()


TIMEZONE = "Africa/Lome"
BUTTON = {}
BUTTONS = {}
FRESH = {}
BUTTONS0 = {}
BUTTONS1 = {}
BUTTONS2 = {}
SPELL_CHECK = {}


def generate_random_alphanumeric():
    """Generate a random 8-letter alphanumeric string."""
    characters = string.ascii_letters + string.digits
    random_chars = ''.join(random.choice(characters) for _ in range(8))
    return random_chars
  
def get_shortlink_sync(url):
    try:
        rget = requests.get(f"https://{STREAM_SITE}/api?api={STREAM_API}&url={url}&alias={generate_random_alphanumeric()}")
        rjson = rget.json()
        if rjson["status"] == "success" or rget.status_code == 200:
            return rjson["shortenedUrl"]
        else:
            return url
    except Exception as e:
        print(f"Error in get_shortlink_sync: {e}")
        return url

async def get_shortlink(url):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, get_shortlink_sync, url)

@Client.on_message(filters.group & filters.text & filters.incoming)
async def give_filter(client, message):
    if EMOJI_MODE:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    await mdb.update_top_messages(message.from_user.id, message.text)
    if message.chat.id != SUPPORT_CHAT_ID:
        manual = await manual_filters(client, message)
        if manual == False:
            settings = await get_settings(message.chat.id)
            try:
                if settings['auto_ffilter']:
                    await auto_filter(client, message)
            except KeyError:
                grpid = await active_connection(str(message.from_user.id))
                await save_group_settings(grpid, 'auto_ffilter', True)
                settings = await get_settings(message.chat.id)
                if settings['auto_ffilter']:
                    await auto_filter(client, message) 
    else:
        search = message.text
        temp_files, temp_offset, total_results = await get_search_results(chat_id=message.chat.id, query=search.lower(), offset=0, filter=True)
        if total_results == 0:
            return
        else:
            return await message.reply_text(f"<b>Salut {message.from_user.mention},\n\nTa requête est disponible ✅\n\n📂 Fichiers Trouvé: {str(total_results)}\n Cherche :</b> <code>{search}</code>\n\n<b>‼️ Ceci est un <u>Groupe de support</u> Mais tu peux obtenir tes fichiers...\n\n📝 Recherche ici : 👇</b>",   
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("ᴊᴏɪɴ ᴀɴᴅ ꜱᴇᴀʀᴄʜ ʜᴇʀᴇ", url=GRP_LNK)]]))

@Client.on_message(filters.private & filters.text & filters.incoming)
async def pm_text(bot, message):
    bot_id = bot.me.id
    content = message.text
    user = message.from_user.first_name
    user_id = message.from_user.id
    if EMOJI_MODE:
        await message.react(emoji=random.choice(REACTIONS), big=True)
    if content.startswith(("/", "#")):
        return  
    try:
        await mdb.update_top_messages(user_id, content)
        pm_search = await db.pm_search_status(bot_id)
        if pm_search:
            await auto_filter(bot, message)
        else:
            await message.reply_text(
             text=f"<b>🙋 Yo {user} 😍 ,\n\n𝑽𝒐𝒖𝒔 𝒑𝒐𝒖𝒗𝒆𝒛 𝒓𝒆𝒄𝒉𝒆𝒓𝒄𝒉𝒆𝒓 𝒅𝒆𝒔 𝒇𝒊𝒍𝒎𝒔 𝒖𝒏𝒊𝒒𝒖𝒆𝒎𝒆𝒏𝒕 𝒅𝒂𝒏𝒔 𝒏𝒐𝒕𝒓𝒆 𝑮𝒓𝒐𝒖𝒑𝒆 𝒅𝒆 𝑭𝒊𝒍𝒎𝒔. 𝑽𝒐𝒖𝒔 𝒏'𝒆̂𝒕𝒆𝒔 𝒑𝒂𝒔 𝒂𝒖𝒕𝒐𝒓𝒊𝒔𝒆́ 𝒂̀ 𝒇𝒂𝒊𝒓𝒆 𝒅𝒆𝒔 𝒓𝒆𝒄𝒉𝒆𝒓𝒄𝒉𝒆𝒔 𝒔𝒖𝒓 𝒍𝒆 𝑩𝒐𝒕 𝑫𝒊𝒓𝒆𝒄𝒕. 𝑺𝒗𝒑, 𝒓𝒆𝒋𝒐𝒊𝒈𝒏𝒆𝒛 𝒏𝒐𝒕𝒓𝒆 𝒈𝒓𝒐𝒖𝒑𝒆 𝒆𝒏 𝒄𝒍𝒊𝒒𝒖𝒂𝒏𝒕 𝒔𝒖𝒓 𝒍𝒆 𝒃𝒐𝒖𝒕𝒐𝒏 𝑭𝑨𝑰𝑹𝑬 𝑼𝑵𝑬 𝑫𝑬𝑴𝑨𝑵𝑫𝑬 𝒄𝒊-𝒅𝒆𝒔𝒔𝒐𝒖𝒔 𝒆𝒕 𝒓𝒆𝒄𝒉𝒆𝒓𝒄𝒉𝒆𝒛 𝒗𝒐𝒔 𝒇𝒊𝒍𝒎𝒔 𝒑𝒓𝒆́𝒇𝒆́𝒓𝒆́𝒔 𝒍𝒂-𝒃𝒂𝒔. 👇</b>",   
             reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📝 Demande ici ", url=GRP_LNK)]])
            )
            await bot.send_message(
                chat_id=LOG_CHANNEL,
                text=f"<b>#𝐏𝐌_𝐌𝐒𝐆\n\n👤 Nom : {user}\n🆔 ID : {user_id}\n💬 Mᴇssᴀɢᴇ : {content}</b>"
            )
    except Exception as e:
        # Log the error
        print(f"An error occurred: {str(e)}")


@Client.on_callback_query(filters.regex(r"^reffff"))
async def refercall(bot, query):
    btn = [[
        InlineKeyboardButton('Lien d\'invitation', url=f'https://telegram.me/share/url?url=https://t.me/{bot.me.username}?start=reff_{query.from_user.id}&text=Hello%21%20Experience%20a%20bot%20that%20offers%20a%20vast%20library%20of%20unlimited%20movies%20and%20series.%20%F0%9F%98%83'),
        InlineKeyboardButton(f'⏳ {referdb.get_refer_points(query.from_user.id)}', callback_data='ref_point'),
        InlineKeyboardButton('Retour', callback_data='premium_info')
    ]]
    reply_markup = InlineKeyboardMarkup(btn)
    await bot.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/1a2e64aee3d4d10edd930.jpg")
        )
    await query.message.edit_text(
        text=f'Hey Voici Ton Lien de parrainage:\n\nhttps://t.me/{bot.me.username}?start=reff_{query.from_user.id}\n\nPartagez ce lien avec vos amis. Chaque fois qu\'ils rejoignent, vous recevrez 10 points de parrainage et après 100 points, vous obtiendrez 1 mois d\'abonnement premium.',
        reply_markup=reply_markup,
        parse_mode=enums.ParseMode.HTML
        )
    await query.answer()

@Client.on_callback_query(filters.regex(r"^next"))
async def next_page(bot, query):
    ident, req, key, offset = query.data.split("_")
    curr_time = datetime.now(pytz.timezone('Africa/Lome')).time()
    if int(req) not in [query.from_user.id, 0]:
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    try:
        offset = int(offset)
    except:
        offset = 0
    if BUTTONS.get(key)!=None:
        search = BUTTONS.get(key)
    else:
        search = FRESH.get(key)
    if not search:
        await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
        return

    files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=offset, filter=True)
    try:
        n_offset = int(n_offset)
    except:
        n_offset = 0

    if not files:
        return
    temp.GETALL[key] = files
    temp.SHORT[query.from_user.id] = query.message.chat.id
    settings = await get_settings(query.message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings['button']:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]


        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Selectionne L\'option ici ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [ 
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saison",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
           
        ])

    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Selectionne L\'option ici ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saison",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}") 
           
        ])

    try:
        if settings['max_btn']:
            if 0 < offset <= 10:
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - 10
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("ɴᴇxᴛ ⋟", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                        InlineKeyboardButton("Suivant ⋟", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
        else:
            if 0 < offset <= int(MAX_B_TN):
                off_set = 0
            elif offset == 0:
                off_set = None
            else:
                off_set = offset - int(MAX_B_TN)
            if n_offset == 0:
                btn.append(
                    [InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages")]
                )
            elif off_set is None:
                btn.append([InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"), InlineKeyboardButton("Suivant ⋟", callback_data=f"next_{req}_{key}_{n_offset}")])
            else:
                btn.append(
                    [
                        InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"),
                        InlineKeyboardButton(f"{math.ceil(int(offset)/int(MAX_B_TN))+1} / {math.ceil(total/int(MAX_B_TN))}", callback_data="pages"),
                        InlineKeyboardButton("Suivant ⋟", callback_data=f"next_{req}_{key}_{n_offset}")
                    ],
                )
    except KeyError:
        await save_group_settings(query.message.chat.id, 'max_btn', True)
        if 0 < offset <= 10:
            off_set = 0
        elif offset == 0:
            off_set = None
        else:
            off_set = offset - 10
        if n_offset == 0:
            btn.append(
                [InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages")]
            )
        elif off_set is None:
            btn.append([InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"), InlineKeyboardButton("Suivant ⋟", callback_data=f"next_{req}_{key}_{n_offset}")])
        else:
            btn.append(
                [
                    InlineKeyboardButton("⋞ Retour", callback_data=f"next_{req}_{key}_{off_set}"),
                    InlineKeyboardButton(f"{math.ceil(int(offset)/10)+1} / {math.ceil(total/10)}", callback_data="pages"),
                    InlineKeyboardButton("Suivant ⋟", callback_data=f"next_{req}_{key}_{n_offset}")
                ],
            )
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Africa/Lome')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()



@Client.on_callback_query(filters.regex(r"^spol"))
async def advantage_spoll_choker(bot, query):
    _, id, user = query.data.split('#')
    if int(user) != 0 and query.from_user.id != int(user):
        return await query.answer(script.ALRT_TXT.format(query.from_user.first_name), show_alert=True)
    
    movies = await get_poster(id, id=True)
    movie = movies.get('title')
    movie = re.sub(r"[:-]", " ", movie)
    movie = re.sub(r"s+", " ", movie).strip()
    
    await query.answer(script.TOP_ALRT_MSG)
    gl = await global_filters(bot, query.message, text=movie)
    
    if gl == False:
        k = await manual_filters(bot, query.message, text=movie)
        
        if k == False:
            files, offset, total_results = await get_search_results(query.message.chat.id, movie, offset=0, filter=True)
            
            if files:
                k = (movie, files, offset, total_results)
                await auto_filter(bot, query, k)
            else:
                reqstr1 = query.from_user.id if query.from_user else 0
                reqstr = await bot.get_users(reqstr1)
                
                if NO_RESULTS_MSG:
                    await bot.send_message(chat_id=BIN_CHANNEL, text=(script.NORSLTS.format(reqstr.id, reqstr.mention, movie)))
                
                # Create the button for contacting admin
                contact_admin_button = InlineKeyboardMarkup(
                    [[InlineKeyboardButton("𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 & 𝙛𝙖𝙞𝙩𝙚𝙨 𝙪𝙣𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙖𝙪𝙥𝙧𝙚̀𝙨 𝙙𝙪 𝙖𝙙𝙢𝙞𝙣", url=OWNER_LNK)]]
                )
                
                k = await query.message.edit(script.MVE_NT_FND, reply_markup=contact_admin_button)
                await asyncio.sleep(10)
                await k.delete()
                
#Qualities 
@Client.on_callback_query(filters.regex(r"^qualities#"))
async def qualities_cb_handler(client: Client, query: CallbackQuery):

    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    _, key = query.data.split("#")
    # if BUTTONS.get(key+"1")!=None:
    #     search = BUTTONS.get(key+"1")
    # else:
    #     search = BUTTONS.get(key)
    #     BUTTONS[key+"1"] = search
    search = FRESH.get(key)
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(QUALITIES)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=QUALITIES[i].title(),
                callback_data=f"fq#{QUALITIES[i].lower()}#{key}"
            ),
            InlineKeyboardButton(
                text=QUALITIES[i+1].title(),
                callback_data=f"fq#{QUALITIES[i+1].lower()}#{key}"
            ),
        ])

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="⇊ Choisis la qualité ⇊", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="↭ Retour au fichiers ↭", callback_data=f"fq#homepage#{key}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
 

@Client.on_callback_query(filters.regex(r"^fq#"))
async def filter_qualities_cb_handler(client: Client, query: CallbackQuery):
    _, qual, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Africa/Lome')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    baal = qual in search
    if baal:
        search = search.replace(qual, "")
    else:
        search = search
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    if qual != "homepage":
        search = f"{search} {qual}" 
    BUTTONS[key] = search

    files, offset, total_results = await get_search_results(chat_id, search, offset=0, filter=True)
    if not files:
        await query.answer("Aucun fichier Trouvé", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis L'option ici ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saison",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les Pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
           
        ])

    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis l'option ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saisons",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
           
        ])

    if offset != "":
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
    
            else:
                btn.append(
                    [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(query.message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="↭ ɴᴏ ᴍᴏʀᴇ ᴘᴀɢᴇꜱ ᴀᴠᴀɪʟᴀʙʟᴇ ↭",callback_data="pages")]
        )
    
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total_results, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()

#languages

@Client.on_callback_query(filters.regex(r"^languages#"))
async def languages_cb_handler(client: Client, query: CallbackQuery):
    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    _, key = query.data.split("#")
    # if BUTTONS.get(key+"1")!=None:
    #     search = BUTTONS.get(key+"1")
    # else:
    #     search = BUTTONS.get(key)
    #     BUTTONS[key+"1"] = search
    search = FRESH.get(key)
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(LANGUAGES)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=LANGUAGES[i].title(),
                callback_data=f"fl#{LANGUAGES[i].lower()}#{key}"
            ),
            InlineKeyboardButton(
                text=LANGUAGES[i+1].title(),
                callback_data=f"fl#{LANGUAGES[i+1].lower()}#{key}"
            ),
        ])

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="⇊ Choisis la langue ⇊", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="↭ Retour aux fichiers ​↭", callback_data=f"fl#homepage#{key}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))
    

@Client.on_callback_query(filters.regex(r"^fl#"))
async def filter_languages_cb_handler(client: Client, query: CallbackQuery):
    _, lang, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Africa/Lome')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    baal = lang in search
    if baal:
        search = search.replace(lang, "")
    else:
        search = search
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    if lang != "homepage":
        search = f"{search} {lang}" 
    BUTTONS[key] = search

    files, offset, total_results = await get_search_results(chat_id, search, offset=0, filter=True)
    if not files:
        await query.answer("Aucun fichiers trouvés", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis une option ici ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saisons",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
            
        ])

    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis une option ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saisons",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
            
        ])

    if offset != "":
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
    
            else:
                btn.append(
                    [InlineKeyboardButton("ᴘᴀɢᴇ", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(query.message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="ɴᴇxᴛ ⋟",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="↭ Plus de page dispo ↭",callback_data="pages")]
        )
    
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Africa/Lome')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        cap = await get_cap(settings, remaining_seconds, files, query, total_results, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except MessageNotModified:
            pass
    await query.answer()
    
    
    
@Client.on_callback_query(filters.regex(r"^seasons#"))
async def seasons_cb_handler(client: Client, query: CallbackQuery):
    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    _, key = query.data.split("#")
    # if BUTTONS.get(key+"2")!=None:
    #     search = BUTTONS.get(key+"2")
    # else:
    #     search = BUTTONS.get(key)
    #     BUTTONS[key+"2"] = search
    search = FRESH.get(key)
    BUTTONS[key] = None
    search = search.replace(' ', '_')
    btn = []
    for i in range(0, len(SEASONS)-1, 2):
        btn.append([
            InlineKeyboardButton(
                text=SEASONS[i].title(),
                callback_data=f"fs#{SEASONS[i].lower()}#{key}"
            ),
            InlineKeyboardButton(
                text=SEASONS[i+1].title(),
                callback_data=f"fs#{SEASONS[i+1].lower()}#{key}"
            ),
        ])

    btn.insert(
        0,
        [
            InlineKeyboardButton(
                text="⇊ Choisis la saison ⇊", callback_data="ident"
            )
        ],
    )
    req = query.from_user.id
    offset = 0
    btn.append([InlineKeyboardButton(text="↭ Retour au fichiers ​↭", callback_data=f"next_{req}_{key}_{offset}")])

    await query.edit_message_reply_markup(InlineKeyboardMarkup(btn))


@Client.on_callback_query(filters.regex(r"^fs#"))
async def filter_seasons_cb_handler(client: Client, query: CallbackQuery):
    _, seas, key = query.data.split("#")
    curr_time = datetime.now(pytz.timezone('Africa/Lome')).time()
    search = FRESH.get(key)
    search = search.replace("_", " ")
    sea = ""
    season_search = ["s01","s02", "s03", "s04", "s05", "s06", "s07", "s08", "s09", "s10", "season 01","season 02","season 03","season 04","season 05","season 06","season 07","season 08","season 09","season 10", "season 1","season 2","season 3","season 4","season 5","season 6","season 7","season 8","season 9"]
    for x in range (len(season_search)):
        if season_search[x] in search:
            sea = season_search[x]
            break
    if sea:
        search = search.replace(sea, "")
    else:
        search = search
    
    req = query.from_user.id
    chat_id = query.message.chat.id
    message = query.message
    try:
        if int(query.from_user.id) not in [query.message.reply_to_message.from_user.id, 0]:
            return await query.answer(
                f"⚠️ Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚....",
                show_alert=True,
            )
    except:
        pass
    
    searchagn = search
    search1 = search
    search2 = search
    search = f"{search} {seas}"
    BUTTONS0[key] = search
    
    files, _, _ = await get_search_results(chat_id, search, max_results=10)
    files = [file for file in files if re.search(seas, file.file_name, re.IGNORECASE)]
    
    seas1 = "s01" if seas == "season 1" else "s02" if seas == "season 2" else "s03" if seas == "season 3" else "s04" if seas == "season 4" else "s05" if seas == "season 5" else "s06" if seas == "season 6" else "s07" if seas == "season 7" else "s08" if seas == "season 8" else "s09" if seas == "season 9" else "s10" if seas == "season 10" else ""
    search1 = f"{search1} {seas1}"
    BUTTONS1[key] = search1
    files1, _, _ = await get_search_results(chat_id, search1, max_results=10)
    files1 = [file for file in files1 if re.search(seas1, file.file_name, re.IGNORECASE)]
    
    if files1:
        files.extend(files1)
    
    seas2 = "season 01" if seas == "season 1" else "season 02" if seas == "season 2" else "season 03" if seas == "season 3" else "season 04" if seas == "season 4" else "season 05" if seas == "season 5" else "season 06" if seas == "season 6" else "season 07" if seas == "season 7" else "season 08" if seas == "season 8" else "season 09" if seas == "season 9" else "s010"
    search2 = f"{search2} {seas2}"
    BUTTONS2[key] = search2
    files2, _, _ = await get_search_results(chat_id, search2, max_results=10)
    files2 = [file for file in files2 if re.search(seas2, file.file_name, re.IGNORECASE)]

    if files2:
        files.extend(files2)
        
    if not files:
        await query.answer("Aucun fichier touvée", show_alert=1)
        return
    temp.GETALL[key] = files
    settings = await get_settings(message.chat.id)
    pre = 'filep' if settings['file_secure'] else 'file'
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Selectionné encore", callback_data=f"seasons#{key}")
        ])
    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis l'option ici ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saison",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=plan"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
            
        ])
    
    offset = 0

    btn.append([
            InlineKeyboardButton(
                text="↭ Retour au fichier ↭",
                callback_data=f"next_{req}_{key}_{offset}"
                ),
    ])
    
    if not settings["button"]:
        cur_time = datetime.now(pytz.timezone('Africa/Lome')).time()
        time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
        remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
        total_results = len(files)
        cap = await get_cap(settings, remaining_seconds, files, query, total_results, search)
        try:
            await query.message.edit_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        except MessageNotModified:
            pass
    else:
        try:
            await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
        except MessageNotModified:
            pass
    await query.answer()

                              
@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    lazyData = query.data
    try:
        link = await client.create_chat_invite_link(int(REQST_CHANNEL))
    except:
        pass
    if query.data == "close_data":
        await query.message.delete()
    elif query.data == "gfiltersdeleteallconfirm":
        await del_allg(query.message, 'gfilters')
        await query.answer("ᴅᴏɴᴇ !")
        return
    elif query.data == "gfiltersdeleteallcancel": 
        await query.message.reply_to_message.delete()
        await query.message.delete()
        await query.answer("ᴘʀᴏᴄᴇꜱꜱ ᴄᴀɴᴄᴇʟʟᴇᴅ !")
        return
    elif query.data == "delallconfirm":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            grpid = await active_connection(str(userid))
            if grpid is not None:
                grp_id = grpid
                try:
                    chat = await client.get_chat(grpid)
                    title = chat.title
                except:
                    await query.message.edit_text("Mᴀᴋᴇ sᴜʀᴇ I'ᴍ ᴘʀᴇsᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ!!", quote=True)
                    return await query.answer(MSG_ALRT)
            else:
                await query.message.edit_text(
                    "I'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs !\nCʜᴇᴄᴋ /connections ᴏʀ ᴄᴏɴɴᴇᴄᴛ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘs.",
                    quote=True
                )
                return await query.answer(MSG_ALRT)

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            title = query.message.chat.title

        else:
            return await query.answer(MSG_ALRT)

        st = await client.get_chat_member(grp_id, userid)
        if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
            await del_all(query.message, grp_id, title)
        else:
            await query.answer("Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ʙᴇ Gʀᴏᴜᴘ Oᴡɴᴇʀ ᴏʀ ᴀɴ Aᴜᴛʜ Usᴇʀ ᴛᴏ ᴅᴏ ᴛʜᴀᴛ !", show_alert=True)
    elif query.data == "delallcancel":
        userid = query.from_user.id
        chat_type = query.message.chat.type

        if chat_type == enums.ChatType.PRIVATE:
            await query.message.reply_to_message.delete()
            await query.message.delete()

        elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            grp_id = query.message.chat.id
            st = await client.get_chat_member(grp_id, userid)
            if (st.status == enums.ChatMemberStatus.OWNER) or (str(userid) in ADMINS):
                await query.message.delete()
                try:
                    await query.message.reply_to_message.delete()
                except:
                    pass
            else:
                await query.answer("Ce n'est pas pour toi!!", show_alert=True)
    elif "groupcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        act = query.data.split(":")[2]
        hr = await client.get_chat(int(group_id))
        title = hr.title
        user_id = query.from_user.id

        if act == "":
            stat = "ᴄᴏɴɴᴇᴄᴛ"
            cb = "connectcb"
        else:
            stat = "ᴅɪꜱᴄᴏɴɴᴇᴄᴛ"
            cb = "disconnect"

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"{stat}", callback_data=f"{cb}:{group_id}"),
             InlineKeyboardButton("ᴅᴇʟᴇᴛᴇ", callback_data=f"deletecb:{group_id}")],
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="backcb")]
        ])

        await query.message.edit_text(
            f"Gʀᴏᴜᴘ Nᴀᴍᴇ : **{title}**\nGʀᴏᴜᴘ ID : `{group_id}`",
            reply_markup=keyboard,
            parse_mode=enums.ParseMode.MARKDOWN
        )
        return await query.answer(MSG_ALRT)
    elif "connectcb" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title

        user_id = query.from_user.id

        mkact = await make_active(str(user_id), str(group_id))

        if mkact:
            await query.message.edit_text(
                f"Cᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text('Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!', parse_mode=enums.ParseMode.MARKDOWN)
        return await query.answer(MSG_ALRT)
    elif "disconnect" in query.data:
        await query.answer()

        group_id = query.data.split(":")[1]

        hr = await client.get_chat(int(group_id))

        title = hr.title
        user_id = query.from_user.id

        mkinact = await make_inactive(str(user_id))

        if mkinact:
            await query.message.edit_text(
                f"Dɪsᴄᴏɴɴᴇᴄᴛᴇᴅ ғʀᴏᴍ **{title}**",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif "deletecb" in query.data:
        await query.answer()

        user_id = query.from_user.id
        group_id = query.data.split(":")[1]

        delcon = await delete_connection(str(user_id), str(group_id))

        if delcon:
            await query.message.edit_text(
                "Sᴜᴄᴄᴇssғᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ ᴄᴏɴɴᴇᴄᴛɪᴏɴ !"
            )
        else:
            await query.message.edit_text(
                f"Sᴏᴍᴇ ᴇʀʀᴏʀ ᴏᴄᴄᴜʀʀᴇᴅ!!",
                parse_mode=enums.ParseMode.MARKDOWN
            )
        return await query.answer(MSG_ALRT)
    elif query.data == "backcb":
        await query.answer()

        userid = query.from_user.id

        groupids = await all_connections(str(userid))
        if groupids is None:
            await query.message.edit_text(
                "Tʜᴇʀᴇ ᴀʀᴇ ɴᴏ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴs!! Cᴏɴɴᴇᴄᴛ ᴛᴏ sᴏᴍᴇ ɢʀᴏᴜᴘs ғɪʀsᴛ.",
            )
            return await query.answer(MSG_ALRT)
        buttons = []
        for groupid in groupids:
            try:
                ttl = await client.get_chat(int(groupid))
                title = ttl.title
                active = await if_active(str(userid), str(groupid))
                act = " - ACTIVE" if active else ""
                buttons.append(
                    [
                        InlineKeyboardButton(
                            text=f"{title}{act}", callback_data=f"groupcb:{groupid}:{act}"
                        )
                    ]
                )
            except:
                pass
        if buttons:
            await query.message.edit_text(
                "Yᴏᴜʀ ᴄᴏɴɴᴇᴄᴛᴇᴅ ɢʀᴏᴜᴘ ᴅᴇᴛᴀɪʟs ;\n\n",
                reply_markup=InlineKeyboardMarkup(buttons)
            )

    elif "gfilteralert" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_gfilter('gfilters', keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)

    elif "alertmessage" in query.data:
        grp_id = query.message.chat.id
        i = query.data.split(":")[1]
        keyword = query.data.split(":")[2]
        reply_text, btn, alerts, fileid = await find_filter(grp_id, keyword)
        if alerts is not None:
            alerts = ast.literal_eval(alerts)
            alert = alerts[int(i)]
            alert = alert.replace("\\n", "\n").replace("\\t", "\t")
            await query.answer(alert, show_alert=True)
        
    if query.data.startswith("file"):
        clicked = query.from_user.id
        try:
            typed = query.from_user.id
        except:
            typed = query.from_user.id
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Nᴏ sᴜᴄʜ ғɪʟᴇ ᴇxɪsᴛ.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        pre_user = await db.has_premium_access(clicked)
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"

        try:
            if settings['is_shortlink'] and not pre_user:
                if clicked == query.from_user.id:
                    temp.SHORT[clicked] = query.message.chat.id
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=short_{file_id}")
                    return
                else:
                    await query.answer(f"Hey {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚. !", show_alert=True)
            else:
                if clicked == query.from_user.id:
                    await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
                    return
                else:
                    await query.answer(f"Salut {query.from_user.first_name},\n𝘾𝙚𝙘𝙞 𝙣'𝙚𝙨𝙩 𝙥𝙖𝙨 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙙𝙚 𝙛𝙞𝙡𝙢,\n𝙛𝙖𝙞𝙩𝙚𝙨 𝙡𝙖 𝙫𝙤̂𝙩𝙧𝙚. !", show_alert=True)
        except UserIsBlocked:
            await query.answer('Débloque le bot l\'ami !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
        except Exception as e:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start={ident}_{file_id}")
  
    elif query.data.startswith("sendfiles"):
        clicked = query.from_user.id
        ident, key = query.data.split("#")
        pre_user = await db.has_premium_access(clicked)
        settings = await get_settings(query.message.chat.id)
        try:
            if settings.get('is_shortlink') and not pre_user:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles1_{key}")
                return
            else:
                await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=allfiles_{key}")
                return
        except UserIsBlocked:
            await query.answer('Débloque le bot l\'ami !', show_alert=True)
        except PeerIdInvalid:
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles3_{key}")
        except Exception as e:
            logger.exception(e)
            await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=sendfiles4_{key}")
    

    elif query.data.startswith("del"):
        ident, file_id = query.data.split("#")
        files_ = await get_file_details(file_id)
        if not files_:
            return await query.answer('Fichier non existant.')
        files = files_[0]
        title = files.file_name
        size = get_size(files.file_size)
        f_caption = files.caption
        settings = await get_settings(query.message.chat.id)
        if CUSTOM_FILE_CAPTION:
            try:
                f_caption = CUSTOM_FILE_CAPTION.format(file_name='' if title is None else title,
                                                       file_size='' if size is None else size,
                                                       file_caption='' if f_caption is None else f_caption)
            except Exception as e:
                logger.exception(e)
            f_caption = f_caption
        if f_caption is None:
            f_caption = f"{files.file_name}"
        await query.answer(url=f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")

    elif query.data.startswith("checksub"):
        ident, kk, file_id = query.data.split("#")
        channels = (await get_settings(int(query.from_user.id))).get('fsub')  
        if channels:
            btn = await is_subscribed(client, query, channels)
            if btn:
                await query.answer(
                    f"👋 Salut {query.from_user.first_name},\n\n"
                    "𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙧𝙚𝙟𝙤𝙞𝙣𝙩 𝙩𝙤𝙪𝙨 𝙡𝙚𝙨 𝘾𝙝𝙖̂𝙣𝙚𝙨 𝙙'𝙢𝙞𝙨𝙚 𝙖̀ 𝙟𝙤𝙪𝙧 𝙧𝙚𝙦𝙪𝙞𝙨𝙚𝙨.\n"
                    "𝙎'𝙞𝙡 𝙫𝙤𝙪𝙨 𝙥𝙡𝙖𝙞𝙩, 𝙧𝙚𝙟𝙤𝙞𝙜𝙣𝙚𝙯 𝙘𝙝𝙖𝙦𝙪𝙚 𝙘𝙝𝙖̂𝙣𝙚 𝙘𝙞-𝙙𝙚𝙨𝙨𝙤𝙪𝙨 𝙚𝙩 𝙧𝙚𝙨𝙨𝙖𝙮𝙚𝙯..\n\n",
                    show_alert=True
                )
                btn.append([InlineKeyboardButton("J'ai rejoint", callback_data=f"checksub#{kk}#{file_id}")])
                await query.edit_message_reply_markup(reply_markup=InlineKeyboardMarkup(btn))
                return
        await query.answer(url=f"https://t.me/{temp.U_NAME}?start={kk}_{file_id}")
        await query.message.delete()

    elif query.data == "pages":
        await query.answer()
    
    elif query.data.startswith("send_fsall"):
        temp_var, ident, key, offset = query.data.split("#")
        search = BUTTON0.get(key)
        if not search:
            await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
            return
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        search = BUTTONS1.get(key)
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        search = BUTTONS2.get(key)
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        await query.answer(f"Yo {query.from_user.first_name}, 𝙏𝙤𝙪𝙨 𝙡𝙚𝙨 𝙛𝙞𝙘𝙝𝙞𝙚𝙧𝙨 𝙙𝙚 𝙘𝙚𝙩𝙩𝙚 𝙥𝙖𝙜𝙚 𝙤𝙣𝙩 𝙚́𝙩𝙚́ 𝙚𝙣𝙫𝙤𝙮𝙚́𝙨 𝙖̀ 𝙫𝙤𝙪𝙨 𝙥𝙖𝙧 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙥𝙧𝙞𝙫𝙚́. !", show_alert=True)
        
    elif query.data.startswith("send_fall"):
        temp_var, ident, key, offset = query.data.split("#")
        if BUTTONS.get(key)!=None:
            search = BUTTONS.get(key)
        else:
            search = FRESH.get(key)
        if not search:
            await query.answer(script.OLD_ALRT_TXT.format(query.from_user.first_name),show_alert=True)
            return
        files, n_offset, total = await get_search_results(query.message.chat.id, search, offset=int(offset), filter=True)
        await send_all(client, query.from_user.id, files, ident, query.message.chat.id, query.from_user.first_name, query)
        await query.answer(f"Yo {query.from_user.first_name}, 𝙏𝙤𝙪𝙨 𝙡𝙚𝙨 𝙛𝙞𝙘𝙝𝙞𝙚𝙧𝙨 𝙙𝙚 𝙘𝙚𝙩𝙩𝙚 𝙥𝙖𝙜𝙚 𝙤𝙣𝙩 𝙚́𝙩𝙚́ 𝙚𝙣𝙫𝙤𝙮𝙚́𝙨 𝙖̀ 𝙫𝙤𝙪𝙨 𝙥𝙖𝙧 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙥𝙧𝙞𝙫𝙚́. !", show_alert=True)
        
    elif query.data.startswith("killfilesdq"):
        ident, keyword = query.data.split("#")
        await query.message.edit_text(f"<b>𝙍𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙙𝙚 𝙛𝙞𝙘𝙝𝙞𝙚𝙧𝙨 𝙥𝙤𝙪𝙧 𝙫𝙤𝙩𝙧𝙚 𝙧𝙚𝙦𝙪𝙚̂𝙩𝙚 {keyword} Dans notre base de donnée. veuillez patientez...</b>")
        files, total = await get_bad_files(keyword)
        await query.message.edit_text("<b>ꜰɪʟᴇ ᴅᴇʟᴇᴛɪᴏɴ ᴘʀᴏᴄᴇꜱꜱ ᴡɪʟʟ ꜱᴛᴀʀᴛ ɪɴ 5 ꜱᴇᴄᴏɴᴅꜱ !</b>")
        await asyncio.sleep(5)
        deleted = 0
        async with lock:
            try:
                for file in files:
                    file_ids = file.file_id
                    file_name = file.file_name
                    result = await Media.collection.delete_one({
                        '_id': file_ids,
                    })
                    if not result.deleted_count:
                        result = await Media2.collection.delete_one({
                            '_id': file_ids,
                        })
                    if result.deleted_count:
                        logger.info(f'ꜰɪʟᴇ ꜰᴏᴜɴᴅ ꜰᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {keyword}! ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {file_name} ꜰʀᴏᴍ ᴅᴀᴛᴀʙᴀꜱᴇ.')
                    deleted += 1
                    if deleted % 20 == 0:
                        await query.message.edit_text(f"<b>ᴘʀᴏᴄᴇꜱꜱ ꜱᴛᴀʀᴛᴇᴅ ꜰᴏʀ ᴅᴇʟᴇᴛɪɴɢ ꜰɪʟᴇꜱ ꜰʀᴏᴍ ᴅʙ. ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ꜰɪʟᴇꜱ ꜰʀᴏᴍ ᴅʙ ꜰᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {keyword} !\n\nᴘʟᴇᴀꜱᴇ ᴡᴀɪᴛ...</b>")
            except Exception as e:
                logger.exception(e)
                await query.message.edit_text(f'Error: {e}')
            else:
                await query.message.edit_text(f"<b>ᴘʀᴏᴄᴇꜱꜱ ᴄᴏᴍᴘʟᴇᴛᴇᴅ ꜰᴏʀ ꜰɪʟᴇ ᴅᴇʟᴇᴛᴀᴛɪᴏɴ !\n\nꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴅᴇʟᴇᴛᴇᴅ {str(deleted)} ꜰɪʟᴇꜱ ꜰʀᴏᴍ ᴅʙ ꜰᴏʀ ʏᴏᴜʀ ǫᴜᴇʀʏ {keyword}.</b>")
    
    elif query.data.startswith("opnsetgrp"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙡𝙚𝙨 𝙙𝙧𝙤𝙞𝙩𝙨 𝙣𝙚́𝙘𝙚𝙨𝙨𝙖𝙞𝙧𝙚𝙨 𝙥𝙤𝙪𝙧 𝙛𝙖𝙞𝙧𝙚 𝙘𝙚𝙡𝙖 !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇꜱᴜʟᴛ ᴘᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇɴᴅ ᴍᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ꜱᴛᴀʀᴛ' if settings["botpm"] else 'ᴀᴜᴛᴏ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["file_secure"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ɪᴍᴅʙ ᴘᴏꜱᴛᴇʀ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["imdb"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["welcome"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_delete"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_ffilter"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴍᴀx ʙᴜᴛᴛᴏɴꜱ',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱʜᴏʀᴛʟɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["is_shortlink"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('⇋ ᴄʟᴏꜱᴇ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ⇋', 
                                         callback_data='close_data'
                                         )
                ]
            ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_text(
                text=f"<b>ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {title} ᴀꜱ ʏᴏᴜ ᴡɪꜱʜ ⚙</b>",
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML
            )
            await query.message.edit_reply_markup(reply_markup)
        
    elif query.data.startswith("opnsetpm"):
        ident, grp_id = query.data.split("#")
        userid = query.from_user.id if query.from_user else None
        st = await client.get_chat_member(grp_id, userid)
        if (
                st.status != enums.ChatMemberStatus.ADMINISTRATOR
                and st.status != enums.ChatMemberStatus.OWNER
                and str(userid) not in ADMINS
        ):
            await query.answer("𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙡𝙚𝙨 𝙙𝙧𝙤𝙞𝙩𝙨 𝙣𝙚́𝙘𝙚𝙨𝙨𝙖𝙞𝙧𝙚𝙨 𝙥𝙤𝙪𝙧 𝙛𝙖𝙞𝙧𝙚 𝙘𝙚𝙡𝙖 !", show_alert=True)
            return
        title = query.message.chat.title
        settings = await get_settings(grp_id)
        btn2 = [[
                 InlineKeyboardButton("𝘾𝙤𝙣𝙨𝙪𝙡𝙩𝙚𝙯 𝙢𝙤𝙣 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙥𝙧𝙞𝙫𝙚́ 🗳️", url=f"telegram.me/{temp.U_NAME}")
               ]]
        reply_markup = InlineKeyboardMarkup(btn2)
        await query.message.edit_text(f"<b>ʏᴏᴜʀ sᴇᴛᴛɪɴɢs ᴍᴇɴᴜ ғᴏʀ {title} ʜᴀs ʙᴇᴇɴ sᴇɴᴛ ᴛᴏ ʏᴏᴜ ʙʏ ᴅᴍ.</b>")
        await query.message.edit_reply_markup(reply_markup)
        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇꜱᴜʟᴛ ᴘᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇɴᴅ ᴍᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ꜱᴛᴀʀᴛ' if settings["botpm"] else 'ᴀᴜᴛᴏ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["file_secure"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ɪᴍᴅʙ ᴘᴏꜱᴛᴇʀ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["imdb"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["welcome"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_delete"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_ffilter"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴍᴀx ʙᴜᴛᴛᴏɴꜱ',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱʜᴏʀᴛʟɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["is_shortlink"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('⇋ ᴄʟᴏꜱᴇ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ⇋', 
                                         callback_data='close_data'
                                         )
                ]
        ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await client.send_message(
                chat_id=userid,
                text=f"<b>ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {title} ᴀꜱ ʏᴏᴜ ᴡɪꜱʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=query.message.id
            )

    elif query.data.startswith("show_option"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("ᴜɴᴀᴠᴀɪʟᴀʙʟᴇ", callback_data=f"unavailable#{from_user}"),
                InlineKeyboardButton("ᴜᴘʟᴏᴀᴅᴇᴅ", callback_data=f"uploaded#{from_user}")
             ],[
                InlineKeyboardButton("ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ", callback_data=f"already_available#{from_user}")
             ],[
                InlineKeyboardButton("Not Released", callback_data=f"Not_Released#{from_user}"),
                InlineKeyboardButton("Type Correct Spelling", callback_data=f"Type_Correct_Spelling#{from_user}")
             ],[
                InlineKeyboardButton("Not Available In The Hindi", callback_data=f"Not_Available_In_The_Hindi#{from_user}")
             ]]
        btn2 = [[
                 InlineKeyboardButton("ᴠɪᴇᴡ ꜱᴛᴀᴛᴜꜱ", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Hᴇʀᴇ ᴀʀᴇ ᴛʜᴇ ᴏᴘᴛɪᴏɴs !")
        else:
            await query.answer("𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙡𝙚𝙨 𝙙𝙧𝙤𝙞𝙩𝙨 𝙣𝙚́𝙘𝙚𝙨𝙨𝙖𝙞𝙧𝙚𝙨 𝙥𝙤𝙪𝙧 𝙛𝙖𝙞𝙧𝙚 𝙘𝙚𝙡𝙖 !", show_alert=True)
        
    elif query.data.startswith("unavailable"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("⚠️ 𝙄𝙣𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚 ⚠️", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Rejoins le canal', url=link.invite_link),
                 InlineKeyboardButton("𝙑𝙤𝙞𝙧 𝙡'𝙚́𝙩𝙖𝙩", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Slt {user.mention}, 𝘿𝙚́𝙨𝙤𝙡𝙚́, 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙚𝙨𝙩 𝙞𝙣𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚. 𝘿𝙪 𝙘𝙤𝙪𝙥, 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨 𝙣𝙚 𝙥𝙚𝙪𝙫𝙚𝙣𝙩 𝙥𝙖𝙨 𝙡𝙖 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚𝙧..</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Slt {user.mention}, 𝘿𝙚́𝙨𝙤𝙡𝙚́, 𝙫𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙚𝙨𝙩 𝙞𝙣𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚. 𝘿𝙪 𝙘𝙤𝙪𝙥, 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨 𝙣𝙚 𝙥𝙚𝙪𝙫𝙚𝙣𝙩 𝙥𝙖𝙨 𝙡𝙖 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚𝙧..\n\n𝙉𝙤𝙩𝙚 : 𝘾𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙚𝙨𝙩 𝙚𝙣𝙫𝙤𝙮𝙚́ 𝙙𝙖𝙣𝙨 𝙘𝙚 𝙜𝙧𝙤𝙪𝙥𝙚 𝙘𝙖𝙧 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙗𝙡𝙤𝙦𝙪𝙚́ 𝙡𝙚 𝙗𝙤𝙩. 𝙋𝙤𝙪𝙧 𝙧𝙚𝙘𝙚𝙫𝙤𝙞𝙧 𝙘𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙚𝙣 𝙥𝙧𝙞𝙫𝙚́, 𝙫𝙤𝙪𝙨 𝙙𝙚𝙫𝙚𝙯 𝙙𝙖𝙗𝙤𝙧𝙙 𝙙𝙚́𝙗𝙡𝙤𝙦𝙪𝙚𝙧 𝙡𝙚 𝙗𝙤𝙩..</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙡𝙚𝙨 𝙙𝙧𝙤𝙞𝙩𝙨 𝙣𝙚́𝙘𝙚𝙨𝙨𝙖𝙞𝙧𝙚𝙨 𝙥𝙤𝙪𝙧 𝙛𝙖𝙞𝙧𝙚 𝙘𝙚𝙡𝙖 !", show_alert=True)
            
    elif query.data.startswith("Not_Released"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("📌 𝙋𝙖𝙨 𝙚𝙣𝙘𝙤𝙧𝙚 𝙙𝙞𝙨𝙥𝙤𝙣𝙞𝙗𝙡𝙚 📌", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Rejoindre le canal', url=link.invite_link),
                 InlineKeyboardButton("Voir l'etat", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uɴᴀᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, The movie you requested has not been released yet. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, The movie you requested has not been released yet. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("𝙑𝙤𝙪𝙨 𝙣'𝙖𝙫𝙚𝙯 𝙥𝙖𝙨 𝙡𝙚𝙨 𝙙𝙧𝙤𝙞𝙩𝙨 𝙣𝙚́𝙘𝙚𝙨𝙨𝙖𝙞𝙧𝙚𝙨 𝙥𝙤𝙪𝙧 𝙛𝙖𝙞𝙧𝙚 𝙘𝙚𝙡𝙖 !", show_alert=True)

    elif query.data.startswith("Type_Correct_Spelling"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("♨️ 𝙑𝙚𝙪𝙞𝙡𝙡𝙚𝙯 𝙨𝙖𝙞𝙨𝙞𝙧 𝙡'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙚 ♨️", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Rejoins le canal', url=link.invite_link),
                 InlineKeyboardButton("ᴠɪᴇᴡ ꜱᴛᴀᴛᴜꜱ", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Type Correct Spelling !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙇'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙙𝙪 𝙛𝙞𝙡𝙢 𝙦𝙪𝙚 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙧𝙚𝙦𝙪𝙞𝙨 𝙚𝙨𝙩 𝙞𝙣𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙚. 𝙎𝙫𝙥, 𝙨𝙖𝙞𝙨𝙞𝙨𝙨𝙚𝙯 𝙡'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙚 𝙙𝙪 𝙣𝙤𝙢 𝙙𝙪 𝙛𝙞𝙡𝙢 𝙚𝙩 𝙧𝙚𝙨𝙨𝙖𝙮𝙚𝙯.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙇'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙙𝙪 𝙛𝙞𝙡𝙢 𝙦𝙪𝙚 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙧𝙚𝙦𝙪𝙞𝙨 𝙚𝙨𝙩 𝙞𝙣𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙚. 𝙎𝙫𝙥, 𝙨𝙖𝙞𝙨𝙞𝙨𝙨𝙚𝙯 𝙡'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙘𝙤𝙧𝙧𝙚𝙘𝙩𝙚 𝙙𝙪 𝙣𝙤𝙢 𝙙𝙪 𝙛𝙞𝙡𝙢 𝙚𝙩 𝙧𝙚𝙨𝙨𝙖𝙮𝙚𝙯.\n\n𝙉𝙤𝙩𝙚 : 𝘾𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙖 𝙚́𝙩𝙚́ 𝙚𝙣𝙫𝙤𝙮𝙚́ 𝙙𝙖𝙣𝙨 𝙘𝙚 𝙜𝙧𝙤𝙪𝙥𝙚 𝙥𝙖𝙧𝙘𝙚 𝙦𝙪𝙚 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙗𝙡𝙤𝙦𝙪𝙚́ 𝙡𝙚 𝙗𝙤𝙩. 𝙋𝙤𝙪𝙧 𝙧𝙚𝙘𝙚𝙫𝙤𝙞𝙧 𝙘𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙚𝙣 𝙥𝙧𝙞𝙫𝙚́, 𝙫𝙤𝙪𝙨 𝙙𝙚𝙫𝙚𝙯 𝙙𝙖𝙗𝙤𝙧𝙙 𝙙𝙚́𝙗𝙡𝙤𝙘𝙠𝙚𝙧 𝙡𝙚 𝙗𝙤𝙩..</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("Not_Available_In_The_Hindi"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("⚜️ Not Available In The Hindi ⚜️", callback_data=f"unalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ', url=link.invite_link),
                 InlineKeyboardButton("ᴠɪᴇᴡ ꜱᴛᴀᴛᴜꜱ", url=f"{query.message.link}")
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Not Available In The Hindi  !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Yo {user.mention}, Your request is not available in the Hindi language. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Yo {user.mention}, Your request is not available in the Hindi language. Sᴏ ᴏᴜʀ ᴍᴏᴅᴇʀᴀᴛᴏʀs ᴄᴀɴ'ᴛ ᴜᴘʟᴏᴀᴅ ɪᴛ.\n\nNᴏᴛᴇ: Tʜɪs ᴍᴇssᴀɢᴇ ɪs sᴇɴᴛ ᴛᴏ ᴛʜɪs ɢʀᴏᴜᴘ ʙᴇᴄᴀᴜsᴇ ʏᴏᴜ'ᴠᴇ ʙʟᴏᴄᴋᴇᴅ ᴛʜᴇ ʙᴏᴛ. Tᴏ sᴇɴᴅ ᴛʜɪs ᴍᴇssᴀɢᴇ ᴛᴏ ʏᴏᴜʀ PM, Mᴜsᴛ ᴜɴʙʟᴏᴄᴋ ᴛʜᴇ ʙᴏᴛ.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢʜᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("uploaded"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("🟢 Téléversé 🟢", callback_data=f"upalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('Rejoindre le canal', url=link.invite_link),
                 InlineKeyboardButton("ᴠɪᴇᴡ ꜱᴛᴀᴛᴜꜱ", url=f"{query.message.link}")
               ],[
                 InlineKeyboardButton("🔍 Recherché ici 🔎", url=GRP_LNK)
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Uᴘʟᴏᴀᴅᴇᴅ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙑𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙖 𝙚́𝙩𝙚́ 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚́𝙚 𝙥𝙖𝙧 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨. 𝙑𝙚𝙪𝙞𝙡𝙡𝙚𝙯 𝙛𝙖𝙞𝙧𝙚 𝙪𝙣𝙚 𝙧𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙙𝙖𝙣𝙨 𝙣𝙤𝙩𝙧𝙚 𝙂𝙧𝙤𝙪𝙥𝙚..</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙑𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙖 𝙚́𝙩𝙚́ 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚́𝙚 𝙥𝙖𝙧 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨. 𝙎𝙫𝙥, 𝙧𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚𝙯 𝙙𝙖𝙣𝙨 𝙣𝙤𝙩𝙧𝙚 𝙂𝙧𝙤𝙪𝙥𝙚.\n\n𝙉𝙤𝙩𝙚 : 𝘾𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙖 𝙚́𝙩𝙚́ 𝙚𝙣𝙫𝙤𝙮𝙚́ 𝙞𝙘𝙞 𝙘𝙖𝙧 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙗𝙡𝙤𝙘𝙠𝙚́ 𝙡𝙚 𝙗𝙤𝙩. 𝙋𝙤𝙪𝙧 𝙧𝙚𝙘𝙚𝙫𝙤𝙞𝙧 𝙘𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙚𝙣 𝙥𝙧𝙞𝙫𝙚́, 𝙫𝙤𝙪𝙨 𝙙𝙚𝙫𝙚𝙯 𝙙𝙖𝙗𝙤𝙧𝙙 𝙙𝙚́𝙗𝙡𝙤𝙘𝙠𝙚𝙧 𝙡𝙚 𝙗𝙤𝙩.</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("already_available"):
        ident, from_user = query.data.split("#")
        btn = [[
                InlineKeyboardButton("♻️ ᴀʟʀᴇᴀᴅʏ ᴀᴠᴀɪʟᴀʙʟᴇ ♻️", callback_data=f"alalert#{from_user}")
              ]]
        btn2 = [[
                 InlineKeyboardButton('ᴊᴏɪɴ ᴄʜᴀɴɴᴇʟ', url=link.invite_link),
                 InlineKeyboardButton("ᴠɪᴇᴡ ꜱᴛᴀᴛᴜꜱ", url=f"{query.message.link}")
               ],[
                 InlineKeyboardButton("🔍 Rechercher Encore 🔎", url=GRP_LNK)
               ]]
        if query.from_user.id in ADMINS:
            user = await client.get_users(from_user)
            reply_markup = InlineKeyboardMarkup(btn)
            content = query.message.text
            await query.message.edit_text(f"<b><strike>{content}</strike></b>")
            await query.message.edit_reply_markup(reply_markup)
            await query.answer("Sᴇᴛ ᴛᴏ Aʟʀᴇᴀᴅʏ Aᴠᴀɪʟᴀʙʟᴇ !")
            try:
                await client.send_message(chat_id=int(from_user), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙑𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙖 𝙚́𝙩𝙚́ 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚́𝙚 𝙥𝙖𝙧 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨. 𝙑𝙚𝙪𝙞𝙡𝙡𝙚𝙯 𝙛𝙖𝙞𝙧𝙚 𝙪𝙣𝙚 𝙧𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙙𝙖𝙣𝙨 𝙣𝙤𝙩𝙧𝙚 𝙂𝙧𝙤𝙪𝙥𝙚..</b>", reply_markup=InlineKeyboardMarkup(btn2))
            except UserIsBlocked:
                await client.send_message(chat_id=int(SUPPORT_CHAT_ID), text=f"<u>{content}</u>\n\n<b>Hᴇʏ {user.mention}, 𝙑𝙤𝙩𝙧𝙚 𝙙𝙚𝙢𝙖𝙣𝙙𝙚 𝙖 𝙚́𝙩𝙚́ 𝙩𝙚́𝙡𝙚́𝙘𝙝𝙖𝙧𝙜𝙚́𝙚 𝙥𝙖𝙧 𝙣𝙤𝙨 𝙢𝙤𝙙𝙚́𝙧𝙖𝙩𝙚𝙪𝙧𝙨. 𝙎𝙫𝙥, 𝙧𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚𝙯 𝙙𝙖𝙣𝙨 𝙣𝙤𝙩𝙧𝙚 𝙂𝙧𝙤𝙪𝙥𝙚.\n\n𝙉𝙤𝙩𝙚 : 𝘾𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙖 𝙚́𝙩𝙚́ 𝙚𝙣𝙫𝙤𝙮𝙚́ 𝙞𝙘𝙞 𝙘𝙖𝙧 𝙫𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙗𝙡𝙤𝙘𝙠𝙚́ 𝙡𝙚 𝙗𝙤𝙩. 𝙋𝙤𝙪𝙧 𝙧𝙚𝙘𝙚𝙫𝙤𝙞𝙧 𝙘𝙚 𝙢𝙚𝙨𝙨𝙖𝙜𝙚 𝙚𝙣 𝙥𝙧𝙞𝙫𝙚́, 𝙫𝙤𝙪𝙨 𝙙𝙚𝙫𝙚𝙯 𝙙𝙖𝙗𝙤𝙧𝙙 𝙙𝙚́𝙗𝙡𝙤𝙘𝙠𝙚𝙧 𝙡𝙚 𝙗𝙤𝙩..</b>", reply_markup=InlineKeyboardMarkup(btn2))
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
            
    
    elif query.data.startswith("alalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, ta requête est dispo  !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    elif query.data.startswith("upalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Ta requête a été téléversé !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)
        
    elif query.data.startswith("unalert"):
        ident, from_user = query.data.split("#")
        if int(query.from_user.id) == int(from_user):
            user = await client.get_users(from_user)
            await query.answer(f"Hᴇʏ {user.first_name}, Yᴏᴜʀ Rᴇᴏ̨ᴜᴇsᴛ ɪs Uɴᴀᴠᴀɪʟᴀʙʟᴇ !", show_alert=True)
        else:
            await query.answer("Yᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ sᴜғғɪᴄɪᴀɴᴛ ʀɪɢᴛs ᴛᴏ ᴅᴏ ᴛʜɪs !", show_alert=True)

    
    elif lazyData.startswith("generate_stream_link"):
        _, file_id = lazyData.split(":")
        try:
            user_id = query.from_user.id
            username =  query.from_user.mention 

            log_msg = await client.send_cached_media(
                chat_id=LOG_CHANNEL,
                file_id=file_id,
            )
            fileName = {quote_plus(get_name(log_msg))}
            lazy_stream = f"{URL}watch/{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"
            lazy_download = f"{URL}{str(log_msg.id)}/{quote_plus(get_name(log_msg))}?hash={get_hash(log_msg)}"

            xo = await query.message.reply_text(f'💘')
            await asyncio.sleep(1)
            await xo.delete()

            await log_msg.reply_text(
                text=f"•• 𝙇𝙞𝙚𝙣 𝙜𝙚́𝙣𝙚́𝙧𝙚́ 𝙥𝙤𝙪𝙧 𝙡'𝙄𝘿 #{user_id} \n•• Ton Nom : {username} \n\n•• ᖴᎥᒪᗴ Nᗩᗰᗴ : {fileName}",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Telechargement rapide 🚀", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('🖥️ Regarder sur notre web 🖥️', url=lazy_stream)]])  # web stream Link
            )
            lucypro = await query.message.reply_text(
                text="•• Lien Généré ☠︎⚔",
                quote=True,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🚀 Telechargement rapide 🚀", url=lazy_download),  # we download Link
                                                    InlineKeyboardButton('🖥️  Regarder sur notre web 🖥️', url=lazy_stream)]])  # web stream Link
            )  
            
            await asyncio.sleep(DELETE_TIME) 
            await lucypro.delete()
            return
            
        except Exception as e:
            print(e)  # print the error message
            await query.answer(f"⚠️ Quelque chose s'est mal passé \n\n{e}", show_alert=True)
            return
            
       #@codeflix_bots
    
    elif query.data == "pagesn1":
        await query.answer(text=script.PAGE_TXT, show_alert=True)

    elif query.data == "reqinfo":
        await query.answer(text=script.REQINFO, show_alert=True)

    elif query.data == "select":
        await query.answer(text=script.SELECT, show_alert=True)

    elif query.data == "sinfo":
        await query.answer(text=script.SINFO, show_alert=True)

    elif query.data == "start":
        buttons = [[
                    InlineKeyboardButton(text="🏡", callback_data="start"),
                    InlineKeyboardButton(text="🛡", callback_data="group_info"),
                    InlineKeyboardButton(text="💳", callback_data="about"),
                    InlineKeyboardButton(text="💸", callback_data="shortlink_info"),
                    InlineKeyboardButton(text="🖥", callback_data="main"),
                ],[
                    InlineKeyboardButton('Mon Groupe de Film/Série/Cartoon', url='t.me/ZFlixTeam')
                ],[
                    InlineKeyboardButton('• Commandes •', callback_data='main'),
                    InlineKeyboardButton('• Anim-Loko •', url='t.me/AnimLoko')
                ],[
                    InlineKeyboardButton('• Premium •', callback_data='premium_info'),
                    InlineKeyboardButton('• A propos •', callback_data='about')
                  ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"
        await query.message.edit_text(
            text=script.START_TXT.format(query.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        await query.answer(MSG_ALRT)
 
    elif query.data == "main":
        buttons = [[
            InlineKeyboardButton('• Commande Admin •', callback_data='admic')
        ], [
            InlineKeyboardButton('• Group •', callback_data='users'),
            InlineKeyboardButton('• Plus •', callback_data='help')
        ], [
            InlineKeyboardButton('• AI •', callback_data='aihelp'),
            InlineKeyboardButton('• Top demande •', callback_data='topsearch')
        ], [
            InlineKeyboardButton('• Autre demande •', callback_data='topsearch')
        ], [
            InlineKeyboardButton('⇋ Retour princiale ⇋', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id,
            query.message.id,
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MAIN_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "purchase":
        buttons = [[
            InlineKeyboardButton('💵 Payé par ID 💵', callback_data='upi_info')
        ],[
            InlineKeyboardButton('📸 Scannez Idian pay 📸', callback_data='qr_info')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/7519d226226bec1090db7.jpg")
        )
        await query.message.edit_text(
            text=script.PURCHASE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "donation":
        buttons = [[
            InlineKeyboardButton('Envoyer Capture d\'écran', url=OWNER_LNK)
        ],[
            InlineKeyboardButton('⇍ Retour ⇏', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto('https://graph.org/file/99eebf5dbe8a134f548e0.jpg')
        )
        await query.message.edit_text(
            text=script.DONATION.format(query.from_user.mention, QR_CODE, OWNER_UPI_ID),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    
    elif query.data == "upi_info":
        buttons = [[
            InlineKeyboardButton('📲 Envoyer Capture d\'écran paiement', url=OWNER_LNK)
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='purchase')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/7519d226226bec1090db7.jpg")
        )
        await query.message.edit_text(
            text=script.UPI_TXT.format(query.from_user.mention, OWNER_UPI_ID),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "qr_info":
        buttons = [[
            InlineKeyboardButton('📲 Envoyer Capture d\'écran paiement', url=OWNER_LNK)
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='purchase')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/7519d226226bec1090db7.jpg")
        )
        await query.message.edit_text(
            text=script.QR_TXT.format(query.from_user.mention, QR_CODE),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "give_trial":
        user_id = query.from_user.id
        has_free_trial = await db.check_trial_status(user_id)
        if has_free_trial:
            await query.answer("🚸 𝙑𝙤𝙪𝙨 𝙖𝙫𝙚𝙯 𝙙𝙚́𝙟𝙖̀ 𝙥𝙧𝙤𝙛𝙞𝙩𝙚́ 𝙙𝙚 𝙫𝙤𝙩𝙧𝙚 𝙚𝙨𝙨𝙖𝙞 𝙜𝙧𝙖𝙩𝙪𝙞𝙩 𝙪𝙣𝙚 𝙛𝙤𝙞𝙨 !\n\n📌 𝘾𝙤𝙣𝙨𝙪𝙡𝙩𝙚𝙯 𝙣𝙤𝙨 𝙛𝙤𝙧𝙛𝙖𝙞𝙩𝙨 𝙖𝙫𝙚𝙘 : /plan", show_alert=True)
            return
        else:            
            await db.give_free_trial(user_id)
            await query.message.reply_text(
                text="<b>🥳 🎉 𝙁𝙚́𝙡𝙞𝙘𝙞𝙩𝙖𝙩𝙞𝙤𝙣𝙨 !\n\n🎉 𝙑𝙤𝙪𝙨 𝙥𝙤𝙪𝙫𝙚𝙯 𝙪𝙩𝙞𝙡𝙞𝙨𝙚𝙧 𝙡'𝙚𝙨𝙨𝙖𝙞 𝙜𝙧𝙖𝙩𝙪𝙞𝙩 𝙥𝙚𝙣𝙙𝙖𝙣𝙩 <u>5 𝙢𝙞𝙣𝙪𝙩𝙚𝙨</u> 𝙖̀ 𝙥𝙖𝙧𝙩𝙞𝙧 𝙙𝙚 𝙢𝙖𝙞𝙣𝙩𝙚𝙣𝙖𝙣𝙩. !</b>",
                quote=False,
                disable_web_page_preview=True,                  
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("💸 𝘿𝙚́𝙘𝙤𝙪𝙫𝙧𝙚𝙯 𝙣𝙤𝙨 𝙛𝙤𝙧𝙛𝙖𝙞𝙩𝙨 𝙥𝙧𝙚𝙢𝙞𝙪𝙢 💸", callback_data='seeplans')]]))
            return    

    elif query.data == "seeplans":
        btn = [[
            InlineKeyboardButton('Parrainez et obtenez Premium', callback_data='reffff') 
        ],[
            InlineKeyboardButton(' Bronze ', callback_data='broze'),
            InlineKeyboardButton('Argent ', callback_data='silver')
        ],[
            InlineKeyboardButton('Or ', callback_data='gold'),
            InlineKeyboardButton('Platine ', callback_data='platinum')
        ],[
            InlineKeyboardButton('Diamant ', callback_data='diamond'),
            InlineKeyboardButton('Autres ', callback_data='other')
        ],[
            InlineKeyboardButton('𝙊𝙗𝙩𝙚𝙣𝙚𝙯 𝙪𝙣 𝙚𝙨𝙨𝙖𝙞 𝙜𝙧𝙖𝙩𝙪𝙞𝙩 𝙙𝙚 𝟱 𝙢𝙞𝙣𝙪𝙩𝙚𝙨', callback_data='free')
        ],[            
            InlineKeyboardButton('❌ Fermer ❌', callback_data='close_data')
        ]]
        reply_markup = InlineKeyboardMarkup(btn)
        await query.message.reply_photo(
            photo=(SUBSCRIPTION),
            caption=script.PREPLANS_TXT.format(query.from_user.mention, OWNER_UPI_ID, QR_CODE),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    

    elif query.data == "premium_info":
        buttons = [[
            InlineKeyboardButton('Parrainez et obtenez Premium', callback_data='reffff'),
        ],[
            InlineKeyboardButton('Bronze ', callback_data='broze'),
            InlineKeyboardButton('Argent ', callback_data='silver')
        ],[
            InlineKeyboardButton('Or ', callback_data='gold'),
            InlineKeyboardButton('Platine ', callback_data='platinum')
        ],[
            InlineKeyboardButton('Diamant ', callback_data='diamond'),
            InlineKeyboardButton('Autres ', callback_data='other')
        ],[
            InlineKeyboardButton('𝙊𝙗𝙩𝙚𝙣𝙚𝙯 𝙪𝙣 𝙚𝙨𝙨𝙖𝙞 𝙜𝙧𝙖𝙩𝙪𝙞𝙩 𝙙𝙚 𝟱 𝙢𝙞𝙣𝙪𝙩𝙚𝙨 ☺️', callback_data='free')
        ],[            
            InlineKeyboardButton('⇋ Retour Principale ⇋', callback_data='start')
        ]]
        
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/7519d226226bec1090db7.jpg")
        )
        await query.message.edit_text(
            text=script.PLAN_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        #@Deendayal_dhakad   
    elif query.data == "free":
        buttons = [[
            InlineKeyboardButton('⚜️ 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙤𝙗𝙩𝙚𝙣𝙞𝙧 𝙪𝙣 𝙚𝙨𝙨𝙖𝙞 𝙜𝙧𝙖𝙩𝙪𝙞𝙩', callback_data="give_trial")
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='other'),
            InlineKeyboardButton('1 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='broze')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.FREE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "broze":
        buttons = [[
            InlineKeyboardButton('🔐 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙖𝙘𝙝𝙚𝙩𝙚𝙧 𝙡𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='free'),
            InlineKeyboardButton('2 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='silver')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/670f6df9f755dc2c9a00a.jpg")
        )
        await query.message.edit_text(
            text=script.BRONZE_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "silver":
        buttons = [[
            InlineKeyboardButton('🔐 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙖𝙘𝙝𝙚𝙩𝙚𝙧 𝙡𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='broze'),
            InlineKeyboardButton('3 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='gold')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/670f6df9f755dc2c9a00a.jpg")
        )
        await query.message.edit_text(
            text=script.SILVER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
#Deendayal403
    elif query.data == "gold":
        buttons = [[
            InlineKeyboardButton('🔐 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙖𝙘𝙝𝙚𝙩𝙚𝙧 𝙡𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='silver'),
            InlineKeyboardButton('4 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='platinum')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/670f6df9f755dc2c9a00a.jpg")
        )
        await query.message.edit_text(
            text=script.GOLD_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "platinum":
        buttons = [[
            InlineKeyboardButton('🔐 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙖𝙘𝙝𝙚𝙩𝙚𝙧 𝙡𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='gold'),
            InlineKeyboardButton('5 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='diamond')
        ],[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/670f6df9f755dc2c9a00a.jpg")
        )
        await query.message.edit_text(
            text=script.PLATINUM_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "diamond":
        buttons = [[
            InlineKeyboardButton('🔐 𝘾𝙡𝙞𝙦𝙪𝙚𝙯 𝙞𝙘𝙞 𝙥𝙤𝙪𝙧 𝙖𝙘𝙝𝙚𝙩𝙚𝙧 𝙡𝙚 𝙥𝙧𝙚𝙢𝙞𝙪𝙢', callback_data='purchase')
        ],[
            InlineKeyboardButton('⋞ Reour', callback_data='platinum'),
            InlineKeyboardButton('6 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='other')
        ],[
            InlineKeyboardButton('⇋ Suivant ⇋', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.DIAMOND_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "other":
        buttons = [[
            InlineKeyboardButton('☎️ 𝘾𝙤𝙣𝙩𝙖𝙘𝙩𝙚𝙯 𝙡𝙚 𝙥𝙧𝙤𝙥𝙧𝙞𝙚́𝙩𝙖𝙞𝙧𝙚 𝙥𝙤𝙪𝙧 𝙚𝙣 𝙨𝙖𝙫𝙤𝙞𝙧 𝙥𝙡𝙪𝙨', url=OWNER_LNK)
        ],[
            InlineKeyboardButton('⋞ Retour', callback_data='diamond'),
            InlineKeyboardButton('7 / 7', callback_data='pagesn1'),
            InlineKeyboardButton('Suivant ⋟', callback_data='free')
        ],[
            InlineKeyboardButton('⇋ retour ⇋', callback_data='premium_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto("https://graph.org/file/670f6df9f755dc2c9a00a.jpg")
        )
        await query.message.edit_text(
            text=script.OTHER_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    
    elif query.data == "group_info":
        buttons = [[
            InlineKeyboardButton('× Tous Nos LIens ×', url="https://t.me/AntiFlix_A")
       ],[
            InlineKeyboardButton('• Group •', url="t.me/ZFlixTeam"),
            InlineKeyboardButton('• Mis à Jour •', url="t.me/BOtZFlix")
       ],[
            InlineKeyboardButton('• Anim-Loko •', url="https://t.me/AnimeLoko"),
            InlineKeyboardButton('• Groupe de torrent •', url="https://t.me/MegaXleech")
       ],[
            InlineKeyboardButton('• Chrunchy Neko •', url="https://t.me/Chrunchy_Neko")
       ],[ 
            InlineKeyboardButton('• Retour •', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.CHANNELS.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "users":
        buttons = [[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.USERS_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "group":
        buttons = [[
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.GROUP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query.data == "admic":
        if query.from_user.id not in ADMINS:
            return await query.answer("⚠️ Tu n'es pas un admin du bot !", show_alert=True)
        page = 0  
        buttons = [
            [InlineKeyboardButton('Suivant ➡️', callback_data=f'admic_next_{page}')],
            [InlineKeyboardButton('⇋ Retour ⇋', callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=commands[page],  
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data.startswith("admic_next_"):
        page = int(query.data.split('_')[-1]) + 1
        if page >= len(commands):
            page = len(commands) - 1

        buttons = []
        if page > 0:
            buttons.append(InlineKeyboardButton('Avant ⬅️', callback_data=f'admic_prev_{page}'))

        if page < len(commands) - 1:
            buttons.append(InlineKeyboardButton('Suivant ➡️', callback_data=f'admic_next_{page}'))

        reply_markup = InlineKeyboardMarkup([buttons, [InlineKeyboardButton('⇋ Retour ⇋', callback_data='help')]])
        await query.message.edit_text(
            text=commands[page],
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data.startswith("admic_prev_"):
        page = int(query.data.split('_')[-1]) - 1
        if page < 0:
            page = 0  

        buttons = []
        if page > 0:
            buttons.append(InlineKeyboardButton('Avant ⬅️', callback_data=f'admic_prev_{page}'))

        if page < len(commands) - 1:
            buttons.append(InlineKeyboardButton('Suivant ➡️', callback_data=f'admic_next_{page}'))

        reply_markup = InlineKeyboardMarkup([buttons, [InlineKeyboardButton('⇋ Retour ⇋', callback_data='help')]])
        await query.message.edit_text(
            text=commands[page],
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query.data == "help":
        buttons = [[
            InlineKeyboardButton('Chat-GPT', callback_data='chatgpt'),
            InlineKeyboardButton('Approbation', callback_data='approve'),
            InlineKeyboardButton('FONT', callback_data='font')
        ], [
            InlineKeyboardButton('IMAGE', callback_data='image'),
            InlineKeyboardButton('Mongo', callback_data='mongo'),
            InlineKeyboardButton('Anime', callback_data='anime')
        ], [
            InlineKeyboardButton('Outils', callback_data='group'),
            InlineKeyboardButton('Torrent', callback_data='torrent'),
            InlineKeyboardButton('Stream', callback_data='streamx')
        ], [
            InlineKeyboardButton('◁', callback_data='main'),
            InlineKeyboardButton('• Maison •', callback_data='start'),
            InlineKeyboardButton('▷', callback_data='help1')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "help1":
        buttons = [[
            InlineKeyboardButton('Extra', callback_data='extra'),
            InlineKeyboardButton('Telegraph', callback_data='tele')
        ], [
            InlineKeyboardButton('Github', callback_data='git')
        ], [
            InlineKeyboardButton('◁', callback_data='help'),
            InlineKeyboardButton('• Maison •', callback_data='start'),
            InlineKeyboardButton('▷', callback_data='help2')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.HELP_TXT.format(query.from_user.mention),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "about":
        buttons = [[
            InlineKeyboardButton('‼️ 𝘼𝙫𝙚𝙧𝙩𝙞𝙨𝙨𝙚𝙢𝙚𝙣𝙩 ‼️', callback_data='disclaimer'),
        ], [
            InlineKeyboardButton('• Support', callback_data='group_info'),
            InlineKeyboardButton('Commandes •', callback_data='main')
        ], [
            InlineKeyboardButton('• Developpeur', user_id=int(7428552084)),
            InlineKeyboardButton('Reseau •', url="t.me/BotZFlix")
        ], [
            InlineKeyboardButton('• Retour •', callback_data='start')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.ABOUT_TXT.format(temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "source":
        buttons = [[
            InlineKeyboardButton('Code Source 📜', url='https://t.me/BotZFlix'),
            InlineKeyboardButton('⇋ Retour ⇋', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=script.SOURCE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query.data == "json":
        buttons = [[
            InlineKeyboardButton('⇍ Retour ⇏', callback_data='help')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=(script.JSON_TXT),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        
    elif query.data == "sticker":
            btn = [[
                    InlineKeyboardButton("⇋ Retour ⇋", callback_data="help")                    
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.STICKER_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "tele":
            btn = [[
                    InlineKeyboardButton("⟸ Retour", callback_data="help1"),
                    InlineKeyboardButton("Contact", url=OWNER_LNK)
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.TELE_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "git":
            btn = [[
                    InlineKeyboardButton("⟸ Retour", callback_data="help1"),
                    InlineKeyboardButton("Contact", url=OWNER_LNK)
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.GITHUB_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "extra":
            btn = [[
                    InlineKeyboardButton("⟸ Retour", callback_data="help1"),
                    InlineKeyboardButton("Contact", url=OWNER_LNK)
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.EXTRA_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "font":
            btn = [[
                    InlineKeyboardButton("⇋ Retour ⇋", callback_data="help")
                  ]]
            await client.edit_message_media(
                query.message.chat.id, 
                query.message.id, 
                InputMediaPhoto(random.choice(PICS))
            )
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.FONT_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "anime":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.ANIME_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "torrent":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.TORRENT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
    elif query.data == "cctools":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.CC_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "image":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.IMAGE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "font":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.FONT_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "approve":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.APPROVE_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "chatgpt":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.CHATGPT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "mongo":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('Support', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.MONGO_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "streamx":
        buttons = [[
            InlineKeyboardButton('Retour', callback_data='help'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.STREAM,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )

    elif query.data == "aihelp":
        buttons = [[
            InlineKeyboardButton('ʙᴀᴄᴋ', callback_data='main'),
            InlineKeyboardButton('sᴜᴘᴘᴏʀᴛ', callback_data='group_info')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text="● ◌ ◌"
        )
        await query.message.edit_text(
            text="● ● ◌"
        )
        await query.message.edit_text(
            text="● ● ●"
        )
        reply_markup = InlineKeyboardMarkup(buttons)
        await client.edit_message_media(
            query.message.chat.id, 
            query.message.id, 
            InputMediaPhoto(random.choice(PICS))
        )
        await query.message.edit_text(
            text=script.AI_TXT,
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )


    elif query.data == "ref_point":
        await query.answer(f'Tu as: {referdb.get_refer_points(query.from_user.id)} Points de parrainage.', show_alert=True)
    
   
    elif query.data == "shortlink_info":
            btn = [[
            InlineKeyboardButton("1 / 3", callback_data="pagesn1"),
            InlineKeyboardButton("Suivant ⋟", callback_data="shortlink_info2")
            ],[
            InlineKeyboardButton('⇋ Retour Principale ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )   
    elif query.data == "shortlink_info2":
            btn = [[
            InlineKeyboardButton("⋞ Retour", callback_data="shortlink_info"),
            InlineKeyboardButton("2 / 3", callback_data="pagesn1"),
            InlineKeyboardButton("Suivant ⋟", callback_data="shortlink_info3")
            ],[
            InlineKeyboardButton('⇋ Retour Principale ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO2),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )
    elif query.data == "shortlink_info3":
            btn = [[
            InlineKeyboardButton("⋞ Retour", callback_data="shortlink_info2"),
            InlineKeyboardButton("3 / 3", callback_data="pagesn1")
            ],[
            InlineKeyboardButton('⇋ Retour Principale ⇋', callback_data='start')
            ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.SHORTLINK_INFO3),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML
            )   
    
    elif query.data == "disclaimer":
            btn = [[
                    InlineKeyboardButton("⇋ Retour ⇋", callback_data="about")
                  ]]
            reply_markup = InlineKeyboardMarkup(btn)
            await query.message.edit_text(
                text=(script.DISCLAIMER_TXT),
                reply_markup=reply_markup,
                parse_mode=enums.ParseMode.HTML 
            )
    elif query.data.startswith("setgs"):
        ident, set_type, status, grp_id = query.data.split("#")
        grpid = await active_connection(str(query.from_user.id))

        if str(grp_id) != str(grpid):
            await query.message.edit("Yᴏᴜʀ Aᴄᴛɪᴠᴇ Cᴏɴɴᴇᴄᴛɪᴏɴ Hᴀs Bᴇᴇɴ Cʜᴀɴɢᴇᴅ. Gᴏ Tᴏ /connections ᴀɴᴅ ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ᴀᴄᴛɪᴠᴇ ᴄᴏɴɴᴇᴄᴛɪᴏɴ.")
            return await query.answer(MSG_ALRT)

        if set_type == 'is_shortlink' and query.from_user.id not in ADMINS:
            return await query.answer(text=f"Hey {query.from_user.first_name}, You can't change shortlink settings for your group !\n\nIt's an admin only setting !", show_alert=True)

        if status == "True":
            await save_group_settings(grpid, set_type, False)
        else:
            await save_group_settings(grpid, set_type, True)

        settings = await get_settings(grpid)

        if settings is not None:
            buttons = [
                [
                    InlineKeyboardButton('ʀᴇꜱᴜʟᴛ ᴘᴀɢᴇ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ʙᴜᴛᴛᴏɴ' if settings["button"] else 'ᴛᴇxᴛ',
                                         callback_data=f'setgs#button#{settings["button"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇɴᴅ ᴍᴏᴅᴇ', callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ꜱᴛᴀʀᴛ' if settings["botpm"] else 'ᴀᴜᴛᴏ',
                                         callback_data=f'setgs#botpm#{settings["botpm"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜰɪʟᴇ ꜱᴇᴄᴜʀᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["file_secure"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#file_secure#{settings["file_secure"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ɪᴍᴅʙ ᴘᴏꜱᴛᴇʀ', callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["imdb"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#imdb#{settings["imdb"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱᴘᴇʟʟ ᴄʜᴇᴄᴋ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["spell_check"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#spell_check#{settings["spell_check"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴡᴇʟᴄᴏᴍᴇ ᴍꜱɢ', callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["welcome"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#welcome#{settings["welcome"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_delete"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴀᴜᴛᴏ ꜰɪʟᴛᴇʀ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["auto_ffilter"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ᴍᴀx ʙᴜᴛᴛᴏɴꜱ',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}'),
                    InlineKeyboardButton('10' if settings["max_btn"] else f'{MAX_B_TN}',
                                         callback_data=f'setgs#max_btn#{settings["max_btn"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('ꜱʜᴏʀᴛʟɪɴᴋ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}'),
                    InlineKeyboardButton('ᴇɴᴀʙʟᴇ' if settings["is_shortlink"] else 'ᴅɪꜱᴀʙʟᴇ',
                                         callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{str(grp_id)}')
                ],
                [
                    InlineKeyboardButton('⇋ ᴄʟᴏꜱᴇ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ⇋', 
                                         callback_data='close_data'
                                         )
                ]
        ]
            reply_markup = InlineKeyboardMarkup(buttons)
            await query.message.edit_reply_markup(reply_markup)
    await query.answer(MSG_ALRT)

    
async def auto_filter(client, msg, spoll=False):
    curr_time = datetime.now(pytz.timezone('Asia/Kolkata')).time()
    # reqstr1 = msg.from_user.id if msg.from_user else 0
    # reqstr = await client.get_users(reqstr1)
    
    if not spoll:
        message = msg
        if message.text.startswith("/"): return  # ignore commands
        if re.findall("((^\/|^,|^!|^\.|^[\U0001F600-\U000E007F]).*)", message.text):
            return
        if len(message.text) < 100:
            search = message.text         
            search = search.lower()
            m=await message.reply_text(f'**🔎 sᴇᴀʀᴄʜɪɴɢ** `{search}`')
            find = search.split(" ")
            search = ""
            removes = ["in","upload", "series", "full", "horror", "thriller", "mystery", "print", "file"]
            for x in find:
                if x in removes:
                    continue
                else:
                    search = search + x + " "
            #search = re.sub(r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|bro|bruh|broh|helo|that|find|dubbed|link|venum|iruka|pannunga|pannungga|anuppunga|anupunga|anuppungga|anupungga|film|undo|kitti|kitty|tharu|kittumo|kittum|movie|any(one)|with\ssubtitle(s)?)", "", search, flags=re.IGNORECASE)
            #search = re.sub(r"\s+", " ", search).strip()
            search = search.replace("-", " ")
            search = search.replace(":","")
            files, offset, total_results = await get_search_results(message.chat.id ,search, offset=0, filter=True)
            settings = await get_settings(message.chat.id)
            if not files:
                #await m.delete()
                if settings["spell_check"]:
                    ai_sts = await m.edit('𝙎𝙫𝙥, 𝙥𝙖𝙩𝙞𝙚𝙣𝙩𝙚𝙯... 𝙅𝙚 𝙫𝙚́𝙧𝙞𝙛𝙞𝙚 𝙡\'𝙤𝙧𝙩𝙝𝙤𝙜𝙧𝙖𝙥𝙝𝙚 𝙙𝙚 𝙫𝙤𝙩𝙧𝙚 𝙧𝙚𝙦𝙪𝙚̂𝙩𝙚...')
                    is_misspelled = await ai_spell_check(chat_id = message.chat.id,wrong_name=search)
                    if is_misspelled:
                        await ai_sts.edit(f'<b>✅Je suggere <code> {is_misspelled}</code> \n𝘿𝙪 𝙘𝙤𝙪𝙥, 𝙟𝙚 𝙛𝙖𝙞𝙨 𝙡𝙖 𝙧𝙚𝙘𝙝𝙚𝙧𝙘𝙝𝙚 𝙥𝙤𝙪𝙧 𝙫𝙤𝙪𝙨 <code>{is_misspelled}</code></b>')
                        await asyncio.sleep(2)
                        message.text = is_misspelled
                        await ai_sts.delete()
                        return await auto_filter(client, message)
                    await ai_sts.delete()
                    return await advantage_spell_chok(client, message)
        else:
            return
    else:
        message = msg.message.reply_to_message  # msg will be callback query
        search, files, offset, total_results = spoll
        m=await message.reply_text(f'**Recherche de...** `{search}`')
        settings = await get_settings(message.chat.id)
        await msg.message.delete()
    pre = 'filep' if settings['file_secure'] else 'file'
    key = f"{message.chat.id}-{message.id}"
    FRESH[key] = search
    temp.GETALL[key] = files
    temp.SHORT[message.from_user.id] = message.chat.id
    if settings["button"]:
        btn = [
            [
                InlineKeyboardButton(
                    text=f"[{get_size(file.file_size)}] {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}", callback_data=f'{pre}#{file.file_id}'
                ),
            ]
            for file in files
        ]
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis une Option ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saison",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré les pubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
            
        ])

    else:
        btn = []
        btn.insert(0, 
            [
                InlineKeyboardButton("⇈ Choisis une Option ⇈", 'reqinfo')
            ]
        )
        btn.insert(0, 
            [
                InlineKeyboardButton(f'Qualité', callback_data=f"qualities#{key}"),
                InlineKeyboardButton("Langue", callback_data=f"languages#{key}"),
                InlineKeyboardButton("Saisons",  callback_data=f"seasons#{key}")
            ]
        )
        btn.insert(0, [
            InlineKeyboardButton("Retiré lespubs", url=f"https://t.me/{temp.U_NAME}?start=premium"),
            InlineKeyboardButton("Envoyer tout", callback_data=f"sendfiles#{key}")
            
        ])

    if offset != "":
        req = message.from_user.id if message.from_user else 0
        try:
            if settings['max_btn']:
                btn.append(
                    [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
            else:
                btn.append(
                    [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/int(MAX_B_TN))}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
                )
        except KeyError:
            await save_group_settings(message.chat.id, 'max_btn', True)
            btn.append(
                [InlineKeyboardButton("Page", callback_data="pages"), InlineKeyboardButton(text=f"1/{math.ceil(int(total_results)/10)}",callback_data="pages"), InlineKeyboardButton(text="Suivant ⋟",callback_data=f"next_{req}_{key}_{offset}")]
            )
    else:
        btn.append(
            [InlineKeyboardButton(text="↭ Plus de page dispo ↭",callback_data="pages")]
        )
    imdb = await get_poster(search, file=(files[0]).file_name) if settings["imdb"] else None
    cur_time = datetime.now(pytz.timezone('Africa/Lome')).time()
    time_difference = timedelta(hours=cur_time.hour, minutes=cur_time.minute, seconds=(cur_time.second+(cur_time.microsecond/1000000))) - timedelta(hours=curr_time.hour, minutes=curr_time.minute, seconds=(curr_time.second+(curr_time.microsecond/1000000)))
    remaining_seconds = "{:.2f}".format(time_difference.total_seconds())
    TEMPLATE = script.IMDB_TEMPLATE_TXT
    if imdb:
        cap = TEMPLATE.format(
            qurey=search,
            title=imdb['title'],
            votes=imdb['votes'],
            aka=imdb["aka"],
            seasons=imdb["seasons"],
            box_office=imdb['box_office'],
            localized_title=imdb['localized_title'],
            kind=imdb['kind'],
            imdb_id=imdb["imdb_id"],
            cast=imdb["cast"],
            runtime=imdb["runtime"],
            countries=imdb["countries"],
            certificates=imdb["certificates"],
            languages=imdb["languages"],
            director=imdb["director"],
            writer=imdb["writer"],
            producer=imdb["producer"],
            composer=imdb["composer"],
            cinematographer=imdb["cinematographer"],
            music_team=imdb["music_team"],
            distributors=imdb["distributors"],
            release_date=imdb['release_date'],
            year=imdb['year'],
            genres=imdb['genres'],
            poster=imdb['poster'],
            plot=imdb['plot'],
            rating=imdb['rating'],
            url=imdb['url'],
            **locals()
        )
        temp.IMDB_CAP[message.from_user.id] = cap
        if not settings["button"]:
            cap+="\n\n<b>📚 <u>Les fichiers de ta demande</u> 👇\n\n</b>"
            for file in files:
                cap += f"<b>\n<a href='https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}'> 📁 {get_size(file.file_size)} ▷ {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n</a></b>"
    else:
        if settings["button"]:
            cap = f"<b>›› Titre : <code>{search}</code>\n›› Fichier Total : <code>{total_results}</code>\n›› Demander Par : {message.from_user.mention}\n›› Affiché dans : <code>{remaining_seconds} Seconds</code>\n\n›› 𝙁𝙞𝙘𝙝𝙞𝙚𝙧𝙨 𝙙𝙚𝙢𝙖𝙣𝙙𝙚́𝙨 👇 \n\n</b>"
        else:
            cap = f"<b>›› Titre : <code>{search}</code>\n›› Fichier Total : <code>{total_results}</code>\n›› Demander Par : {message.from_user.mention}\n›› Affiché dans : <code>{remaining_seconds} Sᴇᴄᴏɴᴅs</code>\n\n›› 𝙁𝙞𝙘𝙝𝙞𝙚𝙧𝙨 𝙙𝙚𝙢𝙖𝙣𝙙𝙚́𝙨 👇 \n\n</b>"
            
            for file in files:
                cap += f"<b><a href='https://telegram.me/{temp.U_NAME}?start=files_{file.file_id}'> 📁 {get_size(file.file_size)} ▷ {' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))}\n\n</a></b>"
                
    if imdb and imdb.get('poster'):
        try:
            hehe = await message.reply_photo(photo=imdb.get('poster'), caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(DELETE_TIME)
                    await hehe.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(DELETE_TIME)
                await hehe.delete()
                await message.delete()
        except (MediaEmpty, PhotoInvalidDimensions, WebpageMediaEmpty):
            pic = imdb.get('poster')
            poster = pic.replace('.jpg', "._V1_UX360.jpg") 
            hmm = await message.reply_photo(photo=poster, caption=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
               if settings['auto_delete']:
                    await asyncio.sleep(DELETE_TIME)
                    m=await message.reply_text("🔎")
                    await hmm.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(DELETE_TIME)
                await hmm.delete()
                await message.delete()
        except Exception as e:
            logger.exception(e)
            m=await message.reply_text("🔎") 
            fek = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn))
            await m.delete()
            try:
                if settings['auto_delete']:
                    await asyncio.sleep(DELETE_TIME)
                    await fek.delete()
                    await message.delete()
            except KeyError:
                await save_group_settings(message.chat.id, 'auto_delete', True)
                await asyncio.sleep(DELETE_TIME)
                await fek.delete()
                await message.delete()
    else:
        fuk = await message.reply_text(text=cap, reply_markup=InlineKeyboardMarkup(btn), disable_web_page_preview=True)
        await m.delete()
        try:
            if settings['auto_delete']:
                await asyncio.sleep(DELETE_TIME)
                await fuk.delete()
                await message.delete()
        except KeyError:
            await save_group_settings(message.chat.id, 'auto_delete', True)
            await asyncio.sleep(DELETE_TIME)
            await fuk.delete()
            await message.delete()

async def ai_spell_check(chat_id, wrong_name):
    async def search_movie(wrong_name):
        search_results = imdb.search_movie(wrong_name)
        movie_list = [movie['title'] for movie in search_results]
        return movie_list
    movie_list = await search_movie(wrong_name)
    if not movie_list:
        return
    for _ in range(5):
        closest_match = process.extractOne(wrong_name, movie_list)
        if not closest_match or closest_match[1] <= 80:
            return 
        movie = closest_match[0]
        files, offset, total_results = await get_search_results(chat_id=chat_id, query=movie)
        if files:
            return movie
        movie_list.remove(movie)

async def advantage_spell_chok(client, message):
    mv_id = message.id
    search = message.text
    chat_id = message.chat.id
    settings = await get_settings(chat_id)
    query = re.sub(
        r"\b(pl(i|e)*?(s|z+|ease|se|ese|(e+)s(e)?)|((send|snd|giv(e)?|gib)(\sme)?)|movie(s)?|new|latest|br((o|u)h?)*|^h(e|a)?(l)*(o)*|mal(ayalam)?|t(h)?amil|file|that|find|und(o)*|kit(t(i|y)?)?o(w)?|thar(u)?(o)*w?|kittum(o)*|aya(k)*(um(o)*)?|full\smovie|any(one)|with\ssubtitle(s)?)",
        "", message.text, flags=re.IGNORECASE)
    query = query.strip() + " movie"
    try:
        movies = await get_poster(search, bulk=True)
    except:
        k = await message.reply(script.I_CUDNT.format(message.from_user.mention))
        await asyncio.sleep(60)
        await k.delete()
        try:
            await message.delete()
        except:
            pass
        return
    if not movies:
        google = search.replace(" ", "+")
        button = [[
            InlineKeyboardButton("ᴅᴏ ɢᴏᴏɢʟᴇ", url=f"https://www.google.com/search?q={google}")
        ]]
        k = await message.reply_text(text=script.I_CUDNT.format(search), reply_markup=InlineKeyboardMarkup(button))
        await asyncio.sleep(60)
        await k.delete()
        try:
            await message.delete()
        except:
            pass
        return
    user = message.from_user.id if message.from_user else 0
    buttons = [[
        InlineKeyboardButton(text=movie.get('title'), callback_data=f"spol#{movie.movieID}#{user}")
    ]
        for movie in movies
    ]
    buttons.append(
        [InlineKeyboardButton(text="Fermer", callback_data='close_data')]
    )
    d = await message.reply_text(text=script.CUDNT_FND.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(buttons), reply_to_message_id=message.id)
    await asyncio.sleep(60)
    await d.delete()
    try:
        await message.delete()
    except:
        pass


async def manual_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_filters(group_id)
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_filter(group_id, keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                protect_content=True if settings["file_secure"] else False,
                                reply_to_message_id=reply_id
                            )
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            protect_content=True if settings["file_secure"] else False,
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(DELETE_TIME)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(DELETE_TIME)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        try:
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await asyncio.sleep(DELETE_TIME)
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await asyncio.sleep(DELETE_TIME)
                                        await joelkb.delete()
                        except KeyError:
                            grpid = await active_connection(str(message.from_user.id))
                            await save_group_settings(grpid, 'auto_ffilter', True)
                            settings = await get_settings(message.chat.id)
                            if settings['auto_ffilter']:
                                await auto_filter(client, message)

                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False

async def global_filters(client, message, text=False):
    settings = await get_settings(message.chat.id)
    group_id = message.chat.id
    name = text or message.text
    reply_id = message.reply_to_message.id if message.reply_to_message else message.id
    keywords = await get_gfilters('gfilters')
    for keyword in reversed(sorted(keywords, key=len)):
        pattern = r"( |^|[^\w])" + re.escape(keyword) + r"( |$|[^\w])"
        if re.search(pattern, name, flags=re.IGNORECASE):
            reply_text, btn, alert, fileid = await find_gfilter('gfilters', keyword)

            if reply_text:
                reply_text = reply_text.replace("\\n", "\n").replace("\\t", "\t")

            if btn is not None:
                try:
                    if fileid == "None":
                        if btn == "[]":
                            joelkb = await client.send_message(
                                group_id, 
                                reply_text, 
                                disable_web_page_preview=True,
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(DELETE_TIME)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(DELETE_TIME)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                            
                        else:
                            button = eval(btn)
                            joelkb = await client.send_message(
                                group_id,
                                reply_text,
                                disable_web_page_preview=True,
                                reply_markup=InlineKeyboardMarkup(button),
                                reply_to_message_id=reply_id
                            )
                            manual = await manual_filters(client, message)
                            if manual == False:
                                settings = await get_settings(message.chat.id)
                                try:
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message)
                                        try:
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await joelkb.delete()
                                    else:
                                        try:
                                            if settings['auto_delete']:
                                                await asyncio.sleep(DELETE_TIME)
                                                await joelkb.delete()
                                        except KeyError:
                                            grpid = await active_connection(str(message.from_user.id))
                                            await save_group_settings(grpid, 'auto_delete', True)
                                            settings = await get_settings(message.chat.id)
                                            if settings['auto_delete']:
                                                await asyncio.sleep(DELETE_TIME)
                                                await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_ffilter', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_ffilter']:
                                        await auto_filter(client, message) 
                            else:
                                try:
                                    if settings['auto_delete']:
                                        await joelkb.delete()
                                except KeyError:
                                    grpid = await active_connection(str(message.from_user.id))
                                    await save_group_settings(grpid, 'auto_delete', True)
                                    settings = await get_settings(message.chat.id)
                                    if settings['auto_delete']:
                                        await joelkb.delete()

                    elif btn == "[]":
                        joelkb = await client.send_cached_media(
                            group_id,
                            fileid,
                            caption=reply_text or "",
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                    else:
                        button = eval(btn)
                        joelkb = await message.reply_cached_media(
                            fileid,
                            caption=reply_text or "",
                            reply_markup=InlineKeyboardMarkup(button),
                            reply_to_message_id=reply_id
                        )
                        manual = await manual_filters(client, message)
                        if manual == False:
                            settings = await get_settings(message.chat.id)
                            try:
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message)
                                    try:
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await joelkb.delete()
                                else:
                                    try:
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                                    except KeyError:
                                        grpid = await active_connection(str(message.from_user.id))
                                        await save_group_settings(grpid, 'auto_delete', True)
                                        settings = await get_settings(message.chat.id)
                                        if settings['auto_delete']:
                                            await asyncio.sleep(DELETE_TIME)
                                            await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_ffilter', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_ffilter']:
                                    await auto_filter(client, message) 
                        else:
                            try:
                                if settings['auto_delete']:
                                    await joelkb.delete()
                            except KeyError:
                                grpid = await active_connection(str(message.from_user.id))
                                await save_group_settings(grpid, 'auto_delete', True)
                                settings = await get_settings(message.chat.id)
                                if settings['auto_delete']:
                                    await joelkb.delete()

                                
                except Exception as e:
                    logger.exception(e)
                break
    else:
        return False
