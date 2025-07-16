import os
import re, sys
import json
import base64
import logging
import random
import asyncio
import time
import pytz
from database.verify_db import vr_db
from .pmfilter import auto_filter 
from Script import script
from datetime import datetime
from database.refer import referdb
from database.config_db import mdb
from pyrogram import Client, filters, enums
from pyrogram.errors import FloodWait
from pyrogram.types import *
from database.ia_filterdb import Media, Media2, get_file_details, unpack_new_file_id, get_bad_files
from database.users_chats_db import db, delete_all_msg
from info import *
from utils import *
from database.connections_mdb import active_connection

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

TIMEZONE = "Africa/Lome"
BATCH_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming)
async def start(client, message):
    if EMOJI_MODE:    
        await message.react(emoji=random.choice(REACTIONS), big=True) 
    if message.chat.type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        buttons = [[
                    InlineKeyboardButton('• Canal Anime •', url=f'http://t.me/t.me/Anime Existence')
                ],[
                    InlineKeyboardButton('• Maître •', url="https://t.me/ZeeTECHBot"),
                    InlineKeyboardButton('• Support •', url='https://t.me/btzf_chat')
                ],[
                    InlineKeyboardButton('• Rejoindre la chaîne des mises à jour •', url="https://t.me/ZeeTECH")
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.GSTART_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup, disable_web_page_preview=True)
        await asyncio.sleep(2) 
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Inconnu"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[
                    InlineKeyboardButton(text="🏡", callback_data="start"),
                    InlineKeyboardButton(text="🛡", callback_data="group_info"),
                    InlineKeyboardButton(text="💳", callback_data="about"),
                    InlineKeyboardButton(text="💸", callback_data="shortlink_info"),
                    InlineKeyboardButton(text="🖥", callback_data="main"),
                ],[
                    InlineKeyboardButton('Ajoutez-moi à votre groupe', url=f'http://t.me/AntiFlix_A')
                ],[
                    InlineKeyboardButton('• Commandes •', callback_data='main'),
                    InlineKeyboardButton('• Cyber •', callback_data='shortlink_info')
                ],[
                    InlineKeyboardButton('• Premium •', callback_data='premium_info'),
                    InlineKeyboardButton('• À propos •', callback_data='about')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après-midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"
        m=await message.reply_text("<i>Bienvenue sur <b>Marh Crow</b>.\nJ'espère que vous allez bien...</i>")
        await asyncio.sleep(0.4)
        await m.edit_text("⏳")
        await asyncio.sleep(0.5)
        await m.edit_text("👀")
        await asyncio.sleep(0.5)
        await m.edit_text("<b><i>Démarrage...</i></b>")
        await asyncio.sleep(0.4)
        await m.delete()        
        m=await message.reply_sticker("CAACAgUAAxkBAAJFeWd037UWP-vgb_dWo55DCPZS9zJzAAJpEgACqXaJVxBrhzahNnwSHgQ") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    
    if not await db.has_premium_access(message.from_user.id):
        channels = (await get_settings(int(message.from_user.id))).get('fsub')
        if channels:  
            btn = await is_subscribed(client, message, channels)
            if btn:
                kk, file_id = message.command[1].split("_", 1)
                btn.append([InlineKeyboardButton("Réessayer", callback_data=f"checksub#{kk}#{file_id}")])
                reply_markup = InlineKeyboardMarkup(btn)
                caption = (
                    f"**Rejoignez notre chaîne de mises à jour puis cliquez sur Réessayer pour obtenir votre fichier demandé.**"
                )
                await message.reply_photo(
                    photo=random.choice(FSUB_PICS),
                    caption=caption,
                    reply_markup=reply_markup,
                    parse_mode=enums.ParseMode.HTML
                )
                return
       
    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
                    InlineKeyboardButton(text="🏡", callback_data="start"),
                    InlineKeyboardButton(text="🛡", callback_data="group_info"),
                    InlineKeyboardButton(text="💳", callback_data="about"),
                    InlineKeyboardButton(text="💸", callback_data="shortlink_info"),
                    InlineKeyboardButton(text="🖥", callback_data="main"),
                ],[
                    InlineKeyboardButton('Canal Flix', url=f'http://t.me/AntiFlix_A')
                ],[
                    InlineKeyboardButton('• Commandes •', callback_data='main'),
                    InlineKeyboardButton('• Cyber •', callback_data='shortlink_info')
                ],[
                    InlineKeyboardButton('• Premium •', callback_data='premium_info'),
                    InlineKeyboardButton('• À propos •', callback_data='about')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après-midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"
        m=await message.reply_text("Salut mon Reuf, comment vas-tu \nAttends un moment mon pote...")
        await asyncio.sleep(0.4)
        await m.edit_text("🎊")
        await asyncio.sleep(0.5)
        await m.edit_text("⚡")
        await asyncio.sleep(0.5)
        await m.edit_text("Démarrage reuf...")
        await asyncio.sleep(0.4)
        await m.delete()        
        m=await message.reply_sticker("CAACAgUAAxkBAAECroBmQKMAAQ-Gw4nibWoj_pJou2vP1a4AAlQIAAIzDxlVkNBkTEb1Lc4eBA") 
        await asyncio.sleep(1)
        await m.delete()
        await message.reply_photo(
            photo=random.choice(PICS),
            caption=script.START_TXT.format(message.from_user.mention, gtxt, temp.U_NAME, temp.B_NAME),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return
    if message.command[1].startswith("reff_"):
        try:
            user_id = int(message.command[1].split("_")[1])
        except ValueError:
            await message.reply_text("Parrainage invalide !")
            return
        if user_id == message.from_user.id:
            await message.reply_text("Hé mec, tu ne peux pas te parrainer toi-même 🤣!\n\nPartage le lien avec tes amis et obtiens 10 points de parrainage. Si tu collectes 150 points, tu peux obtenir 1 mois d'abonnement premium gratuit.")
            return
        if referdb.is_user_in_list(message.from_user.id):
            await message.reply_text("Vous avez déjà été invité ❗")
            return
        try:
            uss = await client.get_users(user_id)
        except Exception:
            return 	    
        referdb.add_user(message.from_user.id)
        fromuse = referdb.get_refer_points(user_id) + 10
        if fromuse == 100:
            referdb.add_refer_points(user_id, 0) 
            await message.reply_text(f"🎉 Félicitations ! Vous avez gagné 10 points de parrainage car vous avez invité avec succès ☞ {uss.mention}!")		    
            await message.reply_text(user_id, f"Vous avez été invité avec succès par {message.from_user.mention}!") 	
            seconds = 2592000
            if seconds > 0:
                expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
                user_data = {"id": user_id, "expiry_time": expiry_time}  
                await db.update_user(user_data)		    
                await client.send_message(
                chat_id=user_id,
                text=f"<b>Hé {uss.mention}\n\nVous avez obtenu 1 mois d'abonnement premium en invitant 150 utilisateurs ❗", disable_web_page_preview=True              
                )
            for admin in ADMINS:
                await client.send_message(chat_id=admin, text=f"Tâche accomplie avec succès par cet utilisateur:\n\nNom: {uss.mention}\n\nID: {uss.id}!")	
        else:
            referdb.add_refer_points(user_id, fromuse)
            await message.reply_text(f"Vous avez été invité avec succès par {uss.mention} !")
            await client.send_message(user_id, f"Félicitations ! Vous avez gagné 10 points de parrainage car vous avez été invité avec succès ☞{message.from_user.mention} !")
        return
        
    if len(message.command) == 2 and message.command[1] in ["premium"]:
        buttons = [[
                    InlineKeyboardButton('📲 Envoyer la capture de paiement', url=OWNER_LNK)
                  ],[
                    InlineKeyboardButton('❌ Fermer ❌', callback_data='close_data')
                  ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_photo(
            photo=(SUBSCRIPTION),
            caption=script.PREPLANS_TXT.format(message.from_user.mention, OWNER_UPI_ID, QR_CODE),
            reply_markup=reply_markup,
            parse_mode=enums.ParseMode.HTML
        )
        return  
    if len(message.command) == 2 and message.command[1].startswith('getfile'):
        movies = message.command[1].split("-", 1)[1] 
        movie = movies.replace('-',' ')
        message.text = movie 
        await auto_filter(client, message) 
        return
    
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""

    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("<b>Veuillez patienter...</b>")
        file_id = data.split("-", 1)[1]
        msgs = BATCH_FILES.get(file_id)
        if not msgs:
            file = await client.download_media(file_id)
            try:
                with open(file) as file_data:
                    msgs = json.loads(file_data.read())
            except:
                await sts.edit("ÉCHEC")
                return await client.send_message(LOG_CHANNEL, "IMPOSSIBLE D'OUVRIR LE FICHIER.")
            os.remove(file)
            BATCH_FILES[file_id] = msgs

        for msg in msgs:
            title = msg.get("title")
            size = get_size(int(msg.get("size", 0)))
            f_caption = msg.get("caption", "")

            if BATCH_FILE_CAPTION:
                try:
                    f_caption = BATCH_FILE_CAPTION.format(file_name='' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption = f_caption

            if f_caption is None:
                f_caption = f"{title}"

            if STREAM_MODE:
                btn = [
                    [InlineKeyboardButton('🚀 Téléchargement rapide / Voir en ligne 🖥️', callback_data=f'generate_stream_link:{file_id}')],
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]
                ]
            else:
                btn = [
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]
                ]
            try:
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    reply_markup=InlineKeyboardMarkup(btn)
                )
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            await asyncio.sleep(1)

        await sts.delete()
        return


    elif data.split("-", 1)[0] == "DSTORE":
        sts = await message.reply("<b>Please wait...</b>")
        b_string = data.split("-", 1)[1]
        decoded = (base64.urlsafe_b64decode(b_string + "=" * (-len(b_string) % 4))).decode("ascii")
        try:
            f_msg_id, l_msg_id, f_chat_id, protect = decoded.split("_", 3)
        except:
            f_msg_id, l_msg_id, f_chat_id = decoded.split("_", 2)
            protect = "/pbatch" if PROTECT_CONTENT else "batch"
        diff = int(l_msg_id) - int(f_msg_id)
        async for msg in client.iter_messages(int(f_chat_id), int(l_msg_id), int(f_msg_id)):
            if msg.media:
                media = getattr(msg, msg.media.value)
                if BATCH_FILE_CAPTION:
                    try:
                        f_caption=BATCH_FILE_CAPTION.format(file_name=getattr(media, 'file_name', ''), file_size=getattr(media, 'file_size', ''), file_caption=getattr(msg, 'caption', ''))
                    except Exception as e:
                        logger.exception(e)
                        f_caption = getattr(msg, 'caption', '')
                else:
                    media = getattr(msg, msg.media.value)
                    file_name = getattr(media, 'file_name', '')
                    f_caption = getattr(msg, 'caption', file_name)
                try:
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, caption=f_caption, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            elif msg.empty:
                continue
            else:
                try:
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except FloodWait as e:
                    await asyncio.sleep(e.x)
                    await msg.copy(message.chat.id, protect_content=True if protect == "/pbatch" else False)
                except Exception as e:
                    logger.exception(e)
                    continue
            await asyncio.sleep(1) 
        return await sts.delete()

    elif data.split("-", 1)[0] == "verify":
        userid = data.split("-", 2)[1]
        token = data.split("-", 3)[2] 
        fileid = data.split("-", 3)[3]
        if str(message.from_user.id) != str(userid):
            return await message.reply_text(
                text="<b>Lien invalide ou expiré !</b>",
                protect_content=False
            )
        is_valid = await check_token(client, userid, token)
        if is_valid == True:
            btn = [[
                InlineKeyboardButton("Cliquez ici pour obtenir le fichier", url=f"https://telegram.me/{temp.U_NAME}?start=files_{fileid}")
            ]]
            await message.reply_photo(
                photo="https://graph.org/file/6928de1539e2e80e47fb8.jpg",
                caption=f"<blockquote><b>👋 Bonjour {message.from_user.mention}, vous avez été vérifié avec succès ✅\n\nVous avez maintenant un accès illimité pendant {VERIFY_EXPIRE} heures 🎉</blockquote></b>",
                reply_markup=InlineKeyboardMarkup(btn)
            )
            await verify_user(client, userid, token) 
            await vr_db.save_verification(message.from_user.id) 
            now = datetime.now()
            current_time = now.strftime("%H:%M:%S")
            current_date = now.strftime("%Y-%m-%d")
            
            lucy_message = (
                f"Nom: {message.from_user.mention}\n"
                f"Heure: {current_time}\n"
                f"Date: {current_date}\n"
                f"#verification_terminee"
            )
            await client.send_message(chat_id=VERIFIED_LOG, text=lucy_message)

        else:
            return await message.reply_text(
                text="<b>Lien invalide ou expiré !</b>",
                protect_content=False
            )
    if data.startswith("sendfiles"):
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après-midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"
        chat_id = int("-" + file_id.split("-")[1])
        userid = message.from_user.id if message.from_user else None
        g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=allfiles_{file_id}")
        k = await client.send_message(chat_id=message.from_user.id,text=f"🫂 Salut {message.from_user.mention}, {gtxt}\n\n‼️ Obtenez tous les fichiers en un seul lien ‼️\n\n✅ Votre lien est prêt, cliquez sur le bouton de téléchargement.\n\n<u>⚠️ Note : Ce message sera supprimé dans 5 minutes pour éviter les problèmes de copyright. Sauvegardez ce lien ailleurs.</u>", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton('📁 Télécharger 📁', url=g)
                    ], [
                        InlineKeyboardButton('⚡ Comment télécharger ⚡', url=await get_tutorial(chat_id))
                    ]
                ]
            )
        )
        await asyncio.sleep(300)
        await k.edit("<b>Votre message a été supprimé !\nVeuillez effectuer une nouvelle recherche.</b>")
        return
        
    elif data.startswith("short"):
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après-midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"        
        user_id = message.from_user.id
        if await db.has_premium_access(message.from_user.id):
            pass
        else:
            chat_id = temp.SHORT.get(user_id)
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
            k = await client.send_message(chat_id=user_id,text=f"🫂 Salut {message.from_user.mention}, {gtxt}\n\n✅ Votre lien est prêt, cliquez sur le bouton de téléchargement.\n\n⚠️ Nom du fichier : <code>{files.file_name}</code> \n\n📥 Taille du fichier : <code>{get_size(files.file_size)}</code>\n\n<u>⚠️ Note : Ce message sera supprimé dans 10 minutes pour éviter les problèmes de copyright. Sauvegardez ce lien ailleurs.</u>", reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('📁 Télécharger 📁', url=g)
                        ], [
                            InlineKeyboardButton('⚡ Comment télécharger ⚡', url=await get_tutorial(chat_id))
                        ]
                    ]
                )
            )
            await asyncio.sleep(600)
            await k.edit("<b>Votre message a été supprimé !\nVeuillez effectuer une nouvelle recherche.</b>")
            return    
    elif data.startswith("all"):
        files = temp.GETALL.get(file_id)
        if not files:
            return await message.reply('<b><i>Aucun fichier trouvé !</b></i>')
        filesarr = []
        for file in files:
            file_id = file.file_id
            files_ = await get_file_details(file_id)
            files1 = files_[0]
            title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), files1.file_name.split()))
            size = get_size(files1.file_size)
            f_caption = files1.caption

            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption = f_caption

            if f_caption is None:
                f_caption = f"{' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), files1.file_name.split()))}"
            if await db.has_premium_access(message.from_user.id):
                pass  
            else:
                if not await check_verification(client, message.from_user.id) and VERIFY == True:
                    btn = [[
                       InlineKeyboardButton("Cliquez ici pour vérifier", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id))
                       ],[
                       InlineKeyboardButton("Comment vérifier", url=HOW_TO_VERIFY)
                   ]]
                    l = await message.reply_text(
                        text=f"<blockquote><b>Bonjour,\n\n ‼️ Vous n'êtes pas vérifié aujourd'hui ‼️\n\n ›› Veuillez vous vérifier pour obtenir un accès illimité pendant {VERIFY_EXPIRE} heures ✅</blockquote></b>",
                        protect_content=False,
                        reply_markup=InlineKeyboardMarkup(btn)
                    )
                    await asyncio.sleep(180)
                    await l.delete()
                    return
            if STREAM_MODE:
                btn = [
                    [InlineKeyboardButton('🚀 Téléchargement rapide / Regarder en ligne 🖥️', callback_data=f'generate_stream_link:{file_id}')],
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]  
                ]
            else:
                btn = [
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]
                ]

            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                caption=f_caption,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            filesarr.append(msg)
        k = await client.send_message(chat_id=message.from_user.id, text=f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\nCe fichier/vidéo sera supprimé dans <b><u><code>{get_time(DELETE_TIME)}</code></u> 🫥 <i></b>(pour des raisons de copyright)</i>.\n\n<b><i>Veuillez transférer ce fichier ailleurs et commencer le téléchargement depuis là</i></b>")
        await asyncio.sleep(DELETE_TIME)
        for x in filesarr:
            await x.delete()
        await k.edit_text("<b>Tous vos fichiers/vidéos ont été supprimés avec succès !\nVeuillez effectuer une nouvelle recherche.</b>")
        return
    elif data.startswith("files"):
        current_time = datetime.now(pytz.timezone(TIMEZONE))
        curr_time = current_time.hour        
        if curr_time < 12:
            gtxt = "Bonjour 👋" 
        elif curr_time < 17:
            gtxt = "Bon après-midi 👋" 
        elif curr_time < 21:
            gtxt = "Bonsoir 👋"
        else:
            gtxt = "Bonne nuit 👋"     
        user_id = message.from_user.id
        if temp.SHORT.get(user_id)==None:
            return await message.reply_text(text="<b>Veuillez rechercher à nouveau dans le groupe</b>")
        else:
            chat_id = temp.SHORT.get(user_id)
        settings = await get_settings(chat_id)
        if not await db.has_premium_access(user_id) and settings['is_shortlink']:
            files_ = await get_file_details(file_id)
            files = files_[0]
            g = await get_shortlink(chat_id, f"https://telegram.me/{temp.U_NAME}?start=file_{file_id}")
            k = await client.send_message(chat_id=message.from_user.id,text=f"🫂 Salut {message.from_user.mention}, {gtxt}\n\n✅ Votre lien est prêt, cliquez sur le bouton de téléchargement.\n\n⚠️ Nom du fichier : <code>{files.file_name}</code> \n\n📥 Taille du fichier : <code>{get_size(files.file_size)}</code>\n\n", reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton('📁 Télécharger 📁', url=g)
                        ], [
                            InlineKeyboardButton('⚡ Comment télécharger ⚡', url=await get_tutorial(chat_id))
                        ]
                    ]
                )
            )
            await asyncio.sleep(600)
            await k.edit("<b>Votre message a été supprimé !\nVeuillez effectuer une nouvelle recherche.</b>")
            return   
    user = message.from_user.id
    files_ = await get_file_details(file_id)        
    if not files_:
        pre, file_id = ((base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))).decode("ascii")).split("_", 1)
        try:
            if await db.has_premium_access(message.from_user.id): 
                pass 
            else:
               if not await check_verification(client, message.from_user.id) and VERIFY == True:
                   btn = [[
                       InlineKeyboardButton("Cliquez ici pour vérifier", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id))
                   ],[
                        InlineKeyboardButton("Comment vérifier", url=HOW_TO_VERIFY)
                   ]]
                   l = await message.reply_text(
                       text=f"<blockquote><b>Bonjour,\n\n ‼️ Vous n'êtes pas vérifié aujourd'hui ‼️\n\n ›› Veuillez vous vérifier pour obtenir un accès illimité pendant {VERIFY_EXPIRE} heures ✅\n\n ›› Si vous voulez des fichiers directs, vous pouvez prendre un abonnement premium.</blockquote></b>",
                       protect_content=False,
                       reply_markup=InlineKeyboardMarkup(btn)
                   )
                   await asyncio.sleep(180)
                   await l.delete()
                   return
            if STREAM_MODE:
                btn = [
                    [InlineKeyboardButton('🚀 Téléchargement rapide / Regarder en ligne 🖥️', callback_data=f'generate_stream_link:{file_id}')],
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]  
                ]
            else:
                btn = [
                    [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]
                ]
            msg = await client.send_cached_media(
                chat_id=message.from_user.id,
                file_id=file_id,
                protect_content=True if pre == 'filep' else False,
                reply_markup=InlineKeyboardMarkup(btn))

            filetype = msg.media
            file = getattr(msg, filetype.value)
            title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), file.file_name.split()))
            size=get_size(file.file_size)
            f_caption = f"<code>{title}</code>"
            if CUSTOM_FILE_CAPTION:
                try:
                    f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='')
                except:
                    return
            await msg.edit_caption(f_caption)
            btn = [[
                InlineKeyboardButton("❗ Obtenir le fichier à nouveau ❗", callback_data=f'delfile#{file_id}')
            ]]
            k = await msg.reply(
                f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\n"
                f"Ce fichier/vidéo sera supprimé dans <b><u><code>{get_time(DELETE_TIME)}</code></u> 🫥 <i></b>"
                "(pour des raisons de copyright)</i>.\n\n"
                "<b><i>Veuillez transférer ce fichier ailleurs et commencer le téléchargement depuis là</i></b>",
                quote=True
            )
            await asyncio.sleep(DELETE_TIME)
            await msg.delete()
            await k.edit_text("<b>Votre vidéo/fichier a été supprimé avec succès !!</b>")
            return
        except:
            pass
        return await message.reply('Aucun fichier existant !')
    
    files = files_[0]
    title = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), files.file_name.split()))
    size = get_size(files.file_size)
    f_caption = files.caption

    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption = f_caption

    if f_caption is None:
        f_caption = ' '.join(filter(lambda x: not x.startswith('[') and not x.startswith('@') and not x.startswith('www.'), files.file_name.split()))

    if await db.has_premium_access(message.from_user.id):
        pass
    else:
        if not await check_verification(client, message.from_user.id) and VERIFY == True:
            btn = [[
              InlineKeyboardButton("Cliquez ici pour vérifier", url=await get_token(client, message.from_user.id, f"https://telegram.me/{temp.U_NAME}?start=", file_id))
           ],[
              InlineKeyboardButton("Comment vérifier", url=HOW_TO_VERIFY)
           ]]
            l = await message.reply_text(
                text=f"<blockquote><b>Bonjour,\n\n ‼️ Vous n'êtes pas vérifié aujourd'hui ‼️\n\n ›› Veuillez vous vérifier pour obtenir un accès illimité pendant {VERIFY_EXPIRE} heures ✅\n\n ›› Si vous voulez des fichiers directs, vous pouvez prendre un abonnement premium.</blockquote></b>",
                protect_content=False,
                reply_markup=InlineKeyboardMarkup(btn)
            )
            await asyncio.sleep(180)
            await l.delete()
            return
    if STREAM_MODE:
        btn = [
            [InlineKeyboardButton('🚀 Téléchargement rapide / Voir en ligne 🖥️', callback_data=f'generate_stream_link:{file_id}')],
            [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]  # Garder cette ligne inchangée
        ]
    else:
        btn = [
            [InlineKeyboardButton('📌 Rejoindre la chaîne des mises à jour 📌', url=MOVIE_UPDATE_CHANNEL_LNK)]
        ]
    msg = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        protect_content=True if pre == 'filep' else False,
        reply_markup=InlineKeyboardMarkup(btn)
    )
    btn = [[
            InlineKeyboardButton("❗ Obtenir le fichier à nouveau ❗", callback_data=f'delfile#{file_id}')
        ]]
    k = await msg.reply(
        f"<b><u>❗️❗️❗️IMPORTANT❗️️❗️❗️</u></b>\n\n"
        f"Ce fichier/vidéo sera supprimé dans <b><u><code>{get_time(DELETE_TIME)}</code></u> 🫥 <i></b>"
        "(pour des raisons de copyright)</i>.\n\n"
        "<b><i>Veuillez transférer ce fichier ailleurs et commencer le téléchargement depuis là</i></b>",
        quote=True
    )     
    await asyncio.sleep(DELETE_TIME)
    await msg.delete()
    await k.edit_text("<b>Votre vidéo/fichier a été supprimé avec succès !!</b>")
    return


@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Envoyer les informations de base du canal"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Type de canaux inattendu.")

    text = '📑 **Liste des canaux/groupes indexés :**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total :** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Canaux_indexés.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Envoyer le fichier de logs"""
    try:
        await message.reply_document('TELEGRAM BOT.LOG')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Supprimer un fichier de la base de données"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Traitement en cours...⏳", quote=True)
    else:
        await message.reply('Répondez au fichier avec /delete que vous voulez supprimer', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('Format de fichier non supporté')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)
    if await Media.count_documents({'file_id': file_id}):
        result = await Media.collection.delete_one({
            '_id': file_id,
        })
    else:
        result = await Media2.collection.delete_one({
            '_id': file_id,
        })
    if result.deleted_count:
        await msg.edit('Fichier supprimé avec succès de la base de données ✅')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_many({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('Fichier supprimé avec succès de la base de données ✅')
        else:
            result = await Media2.collection.delete_many({
                'file_name': file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('Fichier supprimé avec succès de la base de données')
            else:
                result = await Media.collection.delete_many({
                    'file_name': media.file_name,
                    'file_size': media.file_size,
                    'mime_type': media.mime_type
                })
                if result.deleted_count:
                    await msg.edit('Fichier supprimé avec succès de la base de données ✅')
                else:
                    result = await Media2.collection.delete_many({
                        'file_name': media.file_name,
                        'file_size': media.file_size,
                        'mime_type': media.mime_type
                    })
                    if result.deleted_count:
                        await msg.edit('Fichier supprimé avec succès de la base de données ✅')
                    else:
                        await msg.edit('Fichier non trouvé dans la base de données ❌')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'Ceci supprimera tous vos fichiers indexés !\nVoulez-vous vraiment continuer ?',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="⚠️ OUI ⚠️", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="❌ NON ❌", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await Media2.collection.drop()
    await message.answer("Tout a été supprimé")
    await message.message.edit('Tous les fichiers indexés ont été supprimés avec succès ✅')


@Client.on_message(filters.command('settings'))
async def settings(client, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Vous êtes un admin anonyme.\nUtilisez /connect {message.chat.id} en MP.")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("Assurez-vous que je suis présent dans votre groupe !!", quote=True)
                return
        else:
            await message.reply_text("Je ne suis connecté à aucun groupe !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return
    
    settings = await get_settings(grp_id)

    try:
        if settings['max_btn']:
            settings = await get_settings(grp_id)
    except KeyError:
        await save_group_settings(grp_id, 'max_btn', False)
        settings = await get_settings(grp_id)
    if 'is_shortlink' not in settings.keys():
        await save_group_settings(grp_id, 'is_shortlink', False)
    else:
        pass

    if settings is not None:
        buttons = [        
                [
                InlineKeyboardButton(
                    'Page de résultats',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Bouton' if settings["button"] else 'Texte',
                    callback_data=f'setgs#button#{settings["button"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Mode d\'envoi des fichiers',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Manuel' if settings["botpm"] else 'Auto',
                    callback_data=f'setgs#botpm#{settings["botpm"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Sécurité des fichiers',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["file_secure"] else 'Désactivé',
                    callback_data=f'setgs#file_secure#{settings["file_secure"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Poster IMDB',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["imdb"] else 'Désactivé',
                    callback_data=f'setgs#imdb#{settings["imdb"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Vérification orthographique',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["spell_check"] else 'Désactivé',
                    callback_data=f'setgs#spell_check#{settings["spell_check"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Message de bienvenue',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["welcome"] else 'Désactivé',
                    callback_data=f'setgs#welcome#{settings["welcome"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Suppression automatique',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["auto_delete"] else 'Désactivé',
                    callback_data=f'setgs#auto_delete#{settings["auto_delete"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Filtre automatique',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["auto_ffilter"] else 'Désactivé',
                    callback_data=f'setgs#auto_ffilter#{settings["auto_ffilter"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Boutons max',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    '10' if settings["max_btn"] else f'{MAX_B_TN}',
                    callback_data=f'setgs#max_btn#{settings["max_btn"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton(
                    'Raccourcis',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
                InlineKeyboardButton(
                    'Activé' if settings["is_shortlink"] else 'Désactivé',
                    callback_data=f'setgs#is_shortlink#{settings["is_shortlink"]}#{grp_id}',
                ),
            ],
            [
                InlineKeyboardButton('⇋ Fermer le menu des paramètres ⇋', 
                                     callback_data='close_data'
                                     )
            ]
        ]
        

        btn = [[
                InlineKeyboardButton("👤 Ouvrir en chat privé 👤", callback_data=f"opnsetpm#{grp_id}")
              ],[
                InlineKeyboardButton("👥 Ouvrir ici 👥", callback_data=f"opnsetgrp#{grp_id}")
              ]]

        reply_markup = InlineKeyboardMarkup(buttons)
        if chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
            await message.reply_text(
                text="<b>ᴡʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴏᴘᴇɴ ꜱᴇᴛᴛɪɴɢꜱ ᴍᴇɴᴜ ? ⚙️</b>",
                reply_markup=InlineKeyboardMarkup(btn),
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )
        else:
            await message.reply_text(
                text=f"<b>ᴄʜᴀɴɢᴇ ʏᴏᴜʀ ꜱᴇᴛᴛɪɴɢꜱ ꜰᴏʀ {title} ᴀꜱ ʏᴏᴜ ᴡɪꜱʜ ⚙</b>",
                reply_markup=reply_markup,
                disable_web_page_preview=True,
                parse_mode=enums.ParseMode.HTML,
                reply_to_message_id=message.id
            )



@Client.on_message(filters.command('set_template'))
async def save_template(client, message):
    sts = await message.reply("ᴄʜᴇᴄᴋɪɴɢ ᴛᴇᴍᴘʟᴀᴛᴇ...")
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"ʏᴏᴜ'ʀᴇ ᴀɴᴏɴʏᴍᴏᴜꜱ ᴀᴅᴍɪɴ.\nᴜꜱᴇ /connect {message.chat.id} ɪɴ ᴘᴍ.")
    chat_type = message.chat.type

    if chat_type == enums.ChatType.PRIVATE:
        grpid = await active_connection(str(userid))
        if grpid is not None:
            grp_id = grpid
            try:
                chat = await client.get_chat(grpid)
                title = chat.title
            except:
                await message.reply_text("ᴍᴀᴋᴇ ꜱᴜʀᴇ ɪ'ᴍ ᴘʀᴇꜱᴇɴᴛ ɪɴ ʏᴏᴜʀ ɢʀᴏᴜᴘ !!", quote=True)
                return
        else:
            await message.reply_text("ɪ'ᴍ ɴᴏᴛ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴀɴʏ ɢʀᴏᴜᴘ !", quote=True)
            return

    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grp_id = message.chat.id
        title = message.chat.title

    else:
        return

    st = await client.get_chat_member(grp_id, userid)
    if (
            st.status != enums.ChatMemberStatus.ADMINISTRATOR
            and st.status != enums.ChatMemberStatus.OWNER
            and str(userid) not in ADMINS
    ):
        return

    if len(message.command) < 2:
        return await sts.edit("ɴᴏ ɪɴᴘᴜᴛ !")
    template = message.text.split(" ", 1)[1]
    await save_group_settings(grp_id, 'template', template)
    await sts.edit(f"✅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ ᴄʜᴀɴɢᴇᴅ ᴛᴇᴍᴘʟᴀᴛᴇ ꜰᴏʀ <code>{title}</code> ᴛᴏ\n\n{template}")


@Client.on_message((filters.command(["request", "Request"]) | filters.regex("#request") | filters.regex("#Request")) & filters.group)
async def requests(bot, message):
    if REQST_CHANNEL is None or SUPPORT_CHAT_ID is None: return # Must add REQST_CHANNEL and SUPPORT_CHAT_ID to use this feature
    if message.reply_to_message and SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.reply_to_message.text
        try:
            if REQST_CHANNEL is not None:
                btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('ᴠɪᴇᴡ ʀᴇǫᴜᴇꜱᴛ', url=f"{message.reply_to_message.link}"),
                        InlineKeyboardButton('ꜱʜᴏᴡ ᴏᴘᴛɪᴏɴꜱ', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 ʀᴇǫᴜᴇꜱᴛ : <u>{content}</u>\n\n📚 ʀᴇᴘᴏʀᴛᴇᴅ ʙʏ : {mention}\n📖 ʀᴇᴘᴏʀᴛᴇʀ ɪᴅ : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>ʏᴏᴜ ᴍᴜꜱᴛ ᴛʏᴘᴇ ᴀʙᴏᴜᴛ ʏᴏᴜʀ ʀᴇǫᴜᴇꜱᴛ [ᴍɪɴɪᴍᴜᴍ 3 ᴄʜᴀʀᴀᴄᴛᴇʀꜱ]. ʀᴇǫᴜᴇꜱᴛꜱ ᴄᴀɴ'ᴛ ʙᴇ ᴇᴍᴘᴛʏ.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Error: {e}")
            pass
        
    elif SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                        InlineKeyboardButton('Voir la demande', url=f"{message.link}"),
                        InlineKeyboardButton('Afficher les options', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 Demande : <u>{content}</u>\n\n📚 Signalé par : {mention}\n📖 ID du demandeur : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('Voir la demande', url=f"{message.link}"),
                        InlineKeyboardButton('Afficher les options', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 Demande : <u>{content}</u>\n\n📚 Signalé par : {mention}\n📖 ID du demandeur : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>Vous devez décrire votre demande [minimum 3 caractères]. Les demandes ne peuvent pas être vides.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Erreur : {e}")
            pass
     
    elif SUPPORT_CHAT_ID == message.chat.id:
        chat_id = message.chat.id
        reporter = str(message.from_user.id)
        mention = message.from_user.mention
        success = True
        content = message.text
        keywords = ["#request", "/request", "#Request", "/Request"]
        for keyword in keywords:
            if keyword in content:
                content = content.replace(keyword, "")
        try:
            if REQST_CHANNEL is not None and len(content) >= 3:
                btn = [[
                        InlineKeyboardButton('Voir la demande', url=f"{message.link}"),
                        InlineKeyboardButton('Afficher les options', callback_data=f'show_option#{reporter}')
                      ]]
                reported_post = await bot.send_message(chat_id=REQST_CHANNEL, text=f"<b>📝 Demande : <u>{content}</u>\n\n📚 Signalé par : {mention}\n📖 ID du demandeur : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                success = True
            elif len(content) >= 3:
                for admin in ADMINS:
                    btn = [[
                        InlineKeyboardButton('Voir la demande', url=f"{message.link}"),
                        InlineKeyboardButton('Afficher les options', callback_data=f'show_option#{reporter}')
                      ]]
                    reported_post = await bot.send_message(chat_id=admin, text=f"<b>📝 Demande : <u>{content}</u>\n\n📚 Signalé par : {mention}\n📖 ID du demandeur : {reporter}\n\n</b>", reply_markup=InlineKeyboardMarkup(btn))
                    success = True
            else:
                if len(content) < 3:
                    await message.reply_text("<b>Vous devez décrire votre demande [minimum 3 caractères]. Les demandes ne peuvent pas être vides.</b>")
            if len(content) < 3:
                success = False
        except Exception as e:
            await message.reply_text(f"Erreur : {e}")
            pass

    else:
        success = False
    
    if success:
        link = await bot.create_chat_invite_link(int(REQST_CHANNEL))
        btn = [[
                InlineKeyboardButton('Rejoindre le canal', url=link.invite_link),
                InlineKeyboardButton('Voir la demande', url=f"{reported_post.link}")
              ]]
        await message.reply_text("<b>Votre demande a été enregistrée ! Veuillez patienter un moment.\n\nRejoignez d'abord le canal puis consultez la demande.</b>", reply_markup=InlineKeyboardMarkup(btn))
    
@Client.on_message(filters.command("send") & filters.user(ADMINS))
async def send_msg(bot, message):
    if message.reply_to_message:
        target_id = message.text.split(" ", 1)[1]
        out = "Les utilisateurs enregistrés dans la base sont :\n\n"
        success = False
        try:
            user = await bot.get_users(target_id)
            users = await db.get_all_users()
            async for usr in users:
                out += f"{usr['id']}"
                out += '\n'
            if str(user.id) in str(out):
                await message.reply_to_message.copy(int(user.id))
                success = True
            else:
                success = False
            if success:
                await message.reply_text(f"<b>Votre message a été envoyé avec succès à {user.mention}.</b>")
            else:
                await message.reply_text("<b>Cet utilisateur n'a pas encore démarré ce bot !</b>")
        except Exception as e:
            await message.reply_text(f"<b>Erreur : {e}</b>")
    else:
        await message.reply_text("<b>Utilisez cette commande en réponse à un message avec l'ID du chat cible. Exemple : /send userid</b>")

@Client.on_message(filters.command("deletefiles") & filters.user(ADMINS))
async def deletemultiplefiles(bot, message):
    chat_type = message.chat.type
    if chat_type != enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, This command won't work in groups. It only works on my PM !</b>")
    else:
        pass
    try:
        keyword = message.text.split(" ", 1)[1]
    except:
        return await message.reply_text(f"<b>Hey {message.from_user.mention}, Give me a keyword along with the command to delete files.</b>")
    k = await bot.send_message(chat_id=message.chat.id, text=f"<b>Fetching Files for your query {keyword} on DB... Please wait...</b>")
    files, total = await get_bad_files(keyword)
    await k.delete()
    #await k.edit_text(f"<b>Found {total} files for your query {keyword} !\n\nFile deletion process will start in 5 seconds !</b>")
    #await asyncio.sleep(5)
    btn = [[
       InlineKeyboardButton("⚠️ Yes, Continue ! ⚠️", callback_data=f"killfilesdq#{keyword}")
       ],[
       InlineKeyboardButton("❌ No, Abort operation ! ❌", callback_data="close_data")
    ]]
    await message.reply_text(
        text=f"<b>Found {total} files for your query {keyword} !\n\nDo you want to delete?</b>",
        reply_markup=InlineKeyboardMarkup(btn),
        parse_mode=enums.ParseMode.HTML
    )

@Client.on_message(filters.command("shortlink"))
async def shortlink(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Vous êtes un administrateur anonyme, désactivez l'administration anonyme et réessayez cette commande.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>Salut {message.from_user.mention}, cette commande ne fonctionne que dans les groupes !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    data = message.text
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>Vous n'avez pas accès à cette commande !\nCette commande ne fonctionne que pour les administrateurs de groupe.</b>")
    else:
        pass
    try:
        command, shortlink_url, api = data.split(" ")
    except:
        return await message.reply_text("<b>Commande incomplète !\nDonnez-moi la commande avec le site de raccourcissement et l'API.\n\nFormat : <code>/shortlink shortxlinks.com c8dacdff6e91a8e4b4f093fdb4d8ae31bc273c1a</code>")
    reply = await message.reply_text("<b>Veuillez patienter...</b>")
    shortlink_url = re.sub(r"https?://?", "", shortlink_url)
    shortlink_url = re.sub(r"[:/]", "", shortlink_url)
    await save_group_settings(grpid, 'shortlink', shortlink_url)
    await save_group_settings(grpid, 'shortlink_api', api)
    await save_group_settings(grpid, 'is_shortlink', True)
    await reply.edit_text(f"<b>✅ Raccourcisseur ajouté avec succès pour <code>{title}</code>.\n\nSite de raccourcissement : <code>{shortlink_url}</code>\nAPI de raccourcissement : <code>{api}</code></b>")

@Client.on_message(filters.command("setshortlinkoff") & filters.user(ADMINS))
async def offshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("Cette commande ne fonctionne que dans les groupes !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    await save_group_settings(grpid, 'is_shortlink', False)
    ENABLE_SHORTLINK = False
    return await message.reply_text("Raccourcisseur désactivé avec succès.")
    
@Client.on_message(filters.command("setshortlinkon") & filters.user(ADMINS))
async def onshortlink(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("Cette commande ne fonctionne que dans les groupes !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    await save_group_settings(grpid, 'is_shortlink', True)
    ENABLE_SHORTLINK = True
    return await message.reply_text("Raccourcisseur activé avec succès.")


@Client.on_message(filters.command("shortlink_info"))
async def ginfo(bot, message):
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text(f"<b>{message.from_user.mention},\n\nUtilisez cette commande dans votre groupe.</b>")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    chat_id=message.chat.id
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return await message.reply_text("<b>Seul le propriétaire ou un administrateur du groupe peut utiliser cette commande !</b>")
    else:
        settings = await get_settings(chat_id) #récupération des paramètres du groupe
        if 'shortlink' in settings.keys() and 'tutorial' in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            st = settings['tutorial']
            return await message.reply_text(f"<b><u>Statut actuel<u> 📊\n\nSite web : <code>{su}</code>\n\nAPI : <code>{sa}</code>\n\nTutoriel : {st}</b>", disable_web_page_preview=True)
        elif 'shortlink' in settings.keys() and 'tutorial' not in settings.keys():
            su = settings['shortlink']
            sa = settings['shortlink_api']
            return await message.reply_text(f"<b><u>Statut actuel<u> 📊\n\nSite web : <code>{su}</code>\n\nAPI : <code>{sa}</code>\n\nUtilisez la commande /set_tutorial pour définir votre tutoriel.")
        elif 'shortlink' not in settings.keys() and 'tutorial' in settings.keys():
            st = settings['tutorial']
            return await message.reply_text(f"<b>Tutoriel : <code>{st}</code>\n\nUtilisez la commande /shortlink pour connecter votre raccourcisseur</b>")
        else:
            return await message.reply_text("Le raccourcisseur et le tutoriel ne sont pas connectés.\n\nVérifiez les commandes /set_tutorial et /shortlink.")

@Client.on_message(filters.command("set_tutorial"))
async def settutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Vous êtes un administrateur anonyme, désactivez l'administration anonyme et réessayez cette commande.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("Cette commande ne fonctionne que dans les groupes !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    if len(message.command) == 1:
        return await message.reply("<b>Donnez-moi un lien de tutoriel avec cette commande.\n\nUsage : /set_tutorial <code>https://t.me/HowToOpenHP</code></b>")
    elif len(message.command) == 2:
        reply = await message.reply_text("<b>Veuillez patienter...</b>")
        tutorial = message.command[1]
        await save_group_settings(grpid, 'tutorial', tutorial)
        await save_group_settings(grpid, 'is_tutorial', True)
        await reply.edit_text(f"<b>✅ Tutoriel ajouté avec succès\n\nVotre groupe : {title}\n\nVotre tutoriel : <code>{tutorial}</code></b>")
    else:
        return await message.reply("<b>Format incorrect !\nFormat correct : /set_tutorial <code>https://t.me/HowToOpenHP</code></b>")

@Client.on_message(filters.command("remove_tutorial"))
async def removetutorial(bot, message):
    userid = message.from_user.id if message.from_user else None
    if not userid:
        return await message.reply(f"Vous êtes un administrateur anonyme, désactivez l'administration anonyme et réessayez cette commande.")
    chat_type = message.chat.type
    if chat_type == enums.ChatType.PRIVATE:
        return await message.reply_text("Cette commande ne fonctionne que dans les groupes !")
    elif chat_type in [enums.ChatType.GROUP, enums.ChatType.SUPERGROUP]:
        grpid = message.chat.id
        title = message.chat.title
    else:
        return
    userid = message.from_user.id
    user = await bot.get_chat_member(grpid, userid)
    if user.status != enums.ChatMemberStatus.ADMINISTRATOR and user.status != enums.ChatMemberStatus.OWNER and str(userid) not in ADMINS:
        return
    else:
        pass
    reply = await message.reply_text("<b>Veuillez patienter...</b>")
    await save_group_settings(grpid, 'is_tutorial', False)
    await reply.edit_text(f"<b>Lien de tutoriel supprimé avec succès ✅</b>")
    

@Client.on_callback_query(filters.regex("topsearch"))
async def topsearch_callback(client, callback_query):
    
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    
    limit = 20  
    top_messages = await mdb.get_top_messages(limit)
    seen_messages = set()
    truncated_messages = []
    for msg in top_messages:
        msg_lower = msg.lower()
        if msg_lower not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg_lower)
            
            if len(msg) > 35:
                truncated_messages.append(msg[:32] + "...")
            else:
                truncated_messages.append(msg)
    keyboard = [truncated_messages[i:i+2] for i in range(0, len(truncated_messages), 2)]
    reply_markup = ReplyKeyboardMarkup(
        keyboard, 
        one_time_keyboard=True, 
        resize_keyboard=True, 
        placeholder="Recherches les plus populaires du jour"
    )
    await callback_query.message.reply_text("<b>Recherches les plus populaires du jour 👇</b>", reply_markup=reply_markup)
    await callback_query.answer()

@Client.on_message(filters.command('top_search'))
async def top(_, message):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    try:
        limit = int(message.command[1])
    except (IndexError, ValueError):
        limit = 20
    top_messages = await mdb.get_top_messages(limit)
    seen_messages = set()
    truncated_messages = []
    for msg in top_messages:
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            
            if len(msg) > 35:
                truncated_messages.append(msg[:35 - 3])
            else:
                truncated_messages.append(msg)
    keyboard = []
    for i in range(0, len(truncated_messages), 2):
        row = truncated_messages[i:i+2]
        keyboard.append(row)
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True, resize_keyboard=True, placeholder="Recherches les plus populaires du jour")
    await message.reply_text(f"<b>Recherches les plus populaires du jour 👇</b>", reply_markup=reply_markup)

    
@Client.on_message(filters.command('trendlist'))
async def trendlist(client, message):
    def is_alphanumeric(string):
        return bool(re.match('^[a-zA-Z0-9 ]*$', string))
    limit = 31
    if len(message.command) > 1:
        try:
            limit = int(message.command[1])
        except ValueError:
            await message.reply_text("Format de nombre invalide.\nVeuillez fournir un nombre valide après la commande /trendlist.")
            return 
    try:
        top_messages = await mdb.get_top_messages(limit)
    except Exception as e:
        await message.reply_text(f"Erreur lors de la récupération des messages : {str(e)}")
        return  

    if not top_messages:
        await message.reply_text("Aucun message populaire trouvé.")
        return 
    seen_messages = set()
    truncated_messages = []

    for msg in top_messages:
        if msg.lower() not in seen_messages and is_alphanumeric(msg):
            seen_messages.add(msg.lower())
            truncated_messages.append(msg[:32] + '...' if len(msg) > 35 else msg)

    if not truncated_messages:
        await message.reply_text("Aucun message populaire valide trouvé.")
        return  
    formatted_list = "\n".join([f"{i+1}. <b>{msg}</b>" for i, msg in enumerate(truncated_messages)])
    additional_message = "⚡️ Tous les résultats ci-dessus proviennent des recherches des utilisateurs. Ils vous sont montrés exactement tels qu'ils ont été recherchés, sans aucune modification par le propriétaire."
    formatted_list += f"\n\n{additional_message}"
    reply_text = f"<b>Top {len(truncated_messages)} des tendances du jour 👇:</b>\n\n{formatted_list}"
    await message.reply_text(reply_text)

@Client.on_message(filters.private & filters.command("pm_search") & filters.user(ADMINS))
async def set_pm_search(client, message):
    bot_id = client.me.id
    try:
        option = message.text.split(" ", 1)[1].strip().lower()
        enable_status = option in ['on', 'true']
    except (IndexError, ValueError):
        await message.reply_text("<b>💔 Option invalide. Veuillez envoyer 'on' ou 'off' après la commande.</b>")
        return
    try:
        await db.update_pm_search_status(bot_id, enable_status)
        response_text = (
            "<b>Recherche en MP activée ✅</b>" if enable_status 
            else "<b>Recherche en MP désactivée ❌</b>"
        )
        await message.reply_text(response_text)
    except Exception as e:
        await log_error(client, f"Erreur dans set_pm_search: {e}")
        await message.reply_text(f"<b>❗ Une erreur est survenue : {e}</b>")

@Client.on_message(filters.private & filters.command("movie_update") & filters.user(ADMINS))
async def set_movie_update_notification(client, message):
    bot_id = client.me.id
    try:
        option = message.text.split(" ", 1)[1].strip().lower()
        enable_status = option in ['on', 'true']
    except (IndexError, ValueError):
        await message.reply_text("<b>💔 Option invalide. Veuillez envoyer 'on' ou 'off' après la commande.</b>")
        return
    try:
        await db.update_movie_update_status(bot_id, enable_status)
        response_text = (
            "<b>Notifications de mise à jour de films activées ✅</b>" if enable_status 
            else "<b>Notifications de mise à jour de films désactivées ❌</b>"
        )
        await message.reply_text(response_text)
    except Exception as e:
        await log_error(client, f"Erreur dans set_movie_update_notification: {e}")
        await message.reply_text(f"<b>❗ Une erreur est survenue : {e}</b>")

@Client.on_message(filters.command("restart") & filters.user(ADMINS))
async def stop_button(bot, message):
    msg = await bot.send_message(text="<b><i>ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛɪɴɢ</i></b>", chat_id=message.chat.id)       
    await asyncio.sleep(3)
    await msg.edit("<b><i><u>ʙᴏᴛ ɪꜱ ʀᴇꜱᴛᴀʀᴛᴇᴅ</u> ✅</i></b>")
    os.execl(sys.executable, sys.executable, *sys.argv)

async def log_error(client, error_message):
    """Logs errors to the specified LOG_CHANNEL."""
    try:
        await client.send_message(
            chat_id=LOG_CHANNEL, 
            text=f"<b>⚠️ Error Log:</b>\n<code>{error_message}</code>"
        )
    except Exception as e:
        print(f"Failed to log error: {e}")

@Client.on_message(filters.command("del_msg") & filters.user(ADMINS))
async def del_msg(client, message):
    user_id = message.from_user.id
    confirm_markup = InlineKeyboardMarkup([
        [InlineKeyboardButton("Yes", callback_data="confirm_del_yes"),
         InlineKeyboardButton("No", callback_data="confirm_del_no")]
    ])
    sent_message = await message.reply_text(
        "⚠️ Aʀᴇ ʏᴏᴜ sᴜʀᴇ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ᴄʟᴇᴀʀ ᴛʜᴇ ᴜᴘᴅᴀᴛᴇs ᴄʜᴀɴɴᴇʟ ʟɪsᴛ ?\n\n ᴅᴏ ʏᴏᴜ ꜱᴛɪʟʟ ᴡᴀɴᴛ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ ?",
        reply_markup=confirm_markup
    )
    await asyncio.sleep(60)
    try:
        await sent_message.delete()
    except Exception as e:
        print(f"Error deleting the message: {e}")

@Client.on_callback_query(filters.regex('^confirm_del_'))
async def confirmation_handler(client, callback_query):
    user_id = callback_query.from_user.id
    action = callback_query.data.split("_")[-1]  
    if action == "yes":
        await delete_all_msg(user_id)
        await callback_query.message.edit_text(
            '🧹 ᴜᴘᴅᴀᴛᴇꜱ ᴄʜᴀɴɴᴇʟ ʟɪsᴛ ʜᴀs ʙᴇᴇɴ ᴄʟᴇᴀʀᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ ✅'
        )
    elif action == "no":
        await callback_query.message.delete()
    await callback_query.answer()
