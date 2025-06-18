from datetime import timedelta
import pytz
import datetime, time
from Script import script 
from info import *
from utils import get_seconds
from database.users_chats_db import db 
from pyrogram import Client, filters 
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@Client.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])  # Convertir l'user_id en entier
        user = await client.get_users(user_id)
        if await db.remove_premium_access(user_id):
            await message.reply_text("Utilisateur retiré avec succès !")
            await client.send_message(
                chat_id=user_id,
                text=f"<b>Bonjour {user.mention},\n\n<blockquote>Votre accès Premium a été retiré. Merci d'avoir utilisé notre service 😊. Cliquez sur /plan pour voir nos autres offres.</blockquote></b>"
            )
        else:
            await message.reply_text("Impossible de retirer l'utilisateur !\nÊtes-vous sûr qu'il s'agissait d'un ID utilisateur premium ?")
    else:
        await message.reply_text("Utilisation : /remove_premium user_id") 

@Client.on_message(filters.command("myplan"))
async def myplan(client, message):
    user = message.from_user.mention 
    user_id = message.from_user.id
    data = await db.get_user(message.from_user.id)  # Convertir l'user_id en entier
    if data and data.get("expiry_time"):
        expiry = data.get("expiry_time") 
        expiry_ist = expiry.astimezone(pytz.timezone("Africa/Lome"))
        expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")            
        current_time = datetime.datetime.now(pytz.timezone("Africa/Lome"))
        time_left = expiry_ist - current_time
            
        days = time_left.days
        hours, remainder = divmod(time_left.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
            
        time_left_str = f"{days} jours, {hours} heures, {minutes} minutes"
        await message.reply_text(f"⚜️ Données utilisateur premium :\n\n👤 Utilisateur : {user}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Temps restant : {time_left_str}\n⌛️ Date d'expiration : {expiry_str_in_ist}")   
    else:
        await message.reply_text(f"<b>Bonjour {user},\n\n<blockquote>Vous n'avez aucun abonnement premium actif. Si vous souhaitez souscrire, cliquez sur le bouton ci-dessous 👇</blockquote><b>",
	reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🌳 Voir les offres premium 🌳", callback_data='seeplans')]]))			 

@Client.on_message(filters.command("get_premium") & filters.user(ADMINS))
async def get_premium(client, message):
    if len(message.command) == 2:
        user_id = int(message.command[1])
        user = await client.get_users(user_id)
        data = await db.get_user(user_id)  # Convertir l'user_id en entier
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Africa/Lome"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Africa/Lome"))
            time_left = expiry_ist - current_time
            
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            
            time_left_str = f"{days} jours, {hours} heures, {minutes} minutes"
            await message.reply_text(f"⚜️ Données utilisateur premium :\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Temps restant : {time_left_str}\n⌛️ Date d'expiration : {expiry_str_in_ist}")
        else:
            await message.reply_text("Aucune donnée premium trouvée dans la base de données !")
    else:
        await message.reply_text("Utilisation : /get_premium user_id")

@Client.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def give_premium_cmd_handler(client, message):
    if len(message.command) == 4:
        time_zone = datetime.datetime.now(pytz.timezone("Africa/Lome"))
        current_time = time_zone.strftime("%d-%m-%Y\n⏱️ Heure d'adhésion : %I:%M:%S %p") 
        user_id = int(message.command[1])  
        user = await client.get_users(user_id)
        time = message.command[2]+" "+message.command[3]
        seconds = await get_seconds(time)
        if seconds > 0:
            expiry_time = datetime.datetime.now() + datetime.timedelta(seconds=seconds)
            user_data = {"id": user_id, "expiry_time": expiry_time}  
            await db.update_user(user_data) 
            data = await db.get_user(user_id)
            expiry = data.get("expiry_time")   
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")         
            await message.reply_text(f"Premium ajouté avec succès ✅\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Accès premium : <code>{time}</code>\n\n⏳ Date d'adhésion : {current_time}\n\n⌛️ Date d'expiration : {expiry_str_in_ist}", disable_web_page_preview=True)
            await client.send_message(
                chat_id=user_id,
                text=f"👋 Bonjour {user.mention},\nMerci pour votre achat premium.\nProfitez-en !! ✨🎉\n\n⏰ Accès premium : <code>{time}</code>\n⏳ Date d'adhésion : {current_time}\n\n⌛️ Date d'expiration : {expiry_str_in_ist}", disable_web_page_preview=True              
            )    
            await client.send_message(PREMIUM_LOGS, text=f"#Added_Premium\n\n👤 Utilisateur : {user.mention}\n⚡ ID utilisateur : <code>{user_id}</code>\n⏰ Accès premium : <code>{time}</code>\n\n⏳ Date d'adhésion : {current_time}\n\n⌛️ Date d'expiration : {expiry_str_in_ist}", disable_web_page_preview=True)
                    
        else:
            await message.reply_text("Format de durée invalide. Utilisez '1 day' pour jours, '1 hour' pour heures, '1 min' pour minutes, '1 month' pour mois ou '1 year' pour année")
    else:
        await message.reply_text("Utilisation : /add_premium user_id durée (ex: '1 day' pour jours, '1 hour' pour heures, '1 min' pour minutes, '1 month' pour mois ou '1 year' pour année)")

@Client.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def premium_user(client, message):
    aa = await message.reply_text("<i>Récupération en cours...</i>")
    new = f"Liste des utilisateurs premium :\n\n"
    user_count = 1
    users = await db.get_all_users()
    async for user in users:
        data = await db.get_user(user['id'])
        if data and data.get("expiry_time"):
            expiry = data.get("expiry_time") 
            expiry_ist = expiry.astimezone(pytz.timezone("Africa/Lome"))
            expiry_str_in_ist = expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")            
            current_time = datetime.datetime.now(pytz.timezone("Africa/Lome"))
            time_left = expiry_ist - current_time
            days = time_left.days
            hours, remainder = divmod(time_left.seconds, 3600)
            minutes, seconds = divmod(remainder, 60)
            time_left_str = f"{days} jours, {hours} heures, {minutes} minutes"	 
            new += f"{user_count}. {(await client.get_users(user['id'])).mention}\n👤 ID utilisateur : {user['id']}\n⏳ Date d'expiration : {expiry_str_in_ist}\n⏰ Temps restant : {time_left_str}\n"
            user_count += 1
        else:
            pass
    try:    
        await aa.edit_text(new)
    except MessageTooLong:
        with open('usersplan.txt', 'w+') as outfile:
            outfile.write(new)
        await message.reply_document('usersplan.txt', caption="Utilisateurs payants:")

@Client.on_message(filters.command("plan"))
async def plan(client, message):
    user_id = message.from_user.id 
    users = message.from_user.mention 
    btn = [[
            InlineKeyboardButton('• Parrainage •', callback_data='reffff')
        ],[
            InlineKeyboardButton('• Bronze ', callback_data='broze'),
            InlineKeyboardButton('• Argent ', callback_data='silver')
        ],[
            InlineKeyboardButton('• Or ', callback_data='gold'),
            InlineKeyboardButton('• Platine ', callback_data='platinum')
        ],[
            InlineKeyboardButton('• Diamant ', callback_data='diamond'),
            InlineKeyboardButton('• Autre ', callback_data='other')
        ],[
            InlineKeyboardButton('• Essai gratuit ', callback_data='free')
        ],[            
            InlineKeyboardButton('⇋ Retour au menu ⇋', callback_data='start')
    ]]
    await message.reply_photo(photo="https://iili.io/FnTGQN1.md.jpg", caption=script.PREMIUM_TEXT.format(message.from_user.mention), reply_markup=InlineKeyboardMarkup(btn))