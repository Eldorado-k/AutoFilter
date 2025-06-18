from pyrogram import *
from pyrogram.errors import MessageNotModified
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from database.verify_db import vr_db 
from info import ADMINS
from datetime import datetime

@Client.on_message(filters.command("verification") & filters.private & filters.user(ADMINS))
async def vrfs(client, message):
    today = await vr_db.get_vr_count("today")
    yesterday = await vr_db.get_vr_count("yesterday")
    this_week = await vr_db.get_vr_count("this_week")
    this_month = await vr_db.get_vr_count("this_month")
    last_month = await vr_db.get_vr_count("last_month")
    this_year = await vr_db.get_vr_count("year", year=datetime.now().year)
    last_year = await vr_db.get_vr_count("year", year=datetime.now().year - 1)

    btn = [[
        InlineKeyboardButton("Aujourd'hui", callback_data=f'vrrfrs#tud'), 
        InlineKeyboardButton(f"{today}", callback_data=f'vrrfrs#tud')
        ],[
        InlineKeyboardButton("Hier", callback_data=f'vrrfrs#yes'), 
        InlineKeyboardButton(f"{yesterday}", callback_data=f'vrrfrs#yes')
        ],[
        InlineKeyboardButton("Cette semaine", callback_data=f'vrrfrs#week'), 
        InlineKeyboardButton(f"{this_week}", callback_data=f'vrrfrs#week')     
        ],[
        InlineKeyboardButton("Ce mois", callback_data=f'vrrfrs#mont'), 
        InlineKeyboardButton(f"{this_month}", callback_data=f'vrrfrs#mont')
        ],[
        InlineKeyboardButton("Mois dernier", callback_data=f'vrrfrs#lmont'), 
        InlineKeyboardButton(f"{last_month}", callback_data=f'vrrfrs#lmont')        
        ],[
        InlineKeyboardButton("Cette année", callback_data=f'vrrfrs#tyear'), 
        InlineKeyboardButton(f"{this_year}", callback_data=f'vrrfrs#tyear')
        ],[
        InlineKeyboardButton("Année dernière", callback_data=f'vrrfrs#lyear'), 
        InlineKeyboardButton(f"{last_year}", callback_data=f'vrrfrs#lyear')
        ],[
        InlineKeyboardButton("🔄 Actualiser", callback_data=f'vrrfrs#vrrfrs'), 
    ]]
    await message.reply_text("✅ **#Vérification**\n\nUtilisateurs vérifiés au total", reply_markup=InlineKeyboardMarkup(btn))

@Client.on_callback_query(filters.regex(r"^vrrfrs"))
async def vr_ref(client, query): 
    ident, set_type = query.data.split("#")

    if set_type == "tud":
        return await query.answer('Utilisateurs vérifiés aujourd\'hui', show_alert=True)
    elif set_type == "yes":
        return await query.answer('Utilisateurs vérifiés hier', show_alert=True)
    elif set_type == "week":
        return await query.answer('Utilisateurs vérifiés cette semaine', show_alert=True)
    elif set_type == "mont":
        return await query.answer('Utilisateurs vérifiés ce mois', show_alert=True)
    elif set_type == "lmont":
        return await query.answer('Utilisateurs vérifiés le mois dernier', show_alert=True)
    elif set_type == "tyear":
        return await query.answer('Utilisateurs vérifiés cette année', show_alert=True)
    elif set_type == "lyear":
        return await query.answer('Utilisateurs vérifiés l\'année dernière', show_alert=True)
    else:#set_type == "vrrfrs":   
        pass 
        
    # Actualiser les données
    today = await vr_db.get_vr_count("today")
    yesterday = await vr_db.get_vr_count("yesterday")
    this_week = await vr_db.get_vr_count("this_week")
    this_month = await vr_db.get_vr_count("this_month")
    last_month = await vr_db.get_vr_count("last_month")
    this_year = await vr_db.get_vr_count("year", year=datetime.now().year)
    last_year = await vr_db.get_vr_count("year", year=datetime.now().year - 1)
    
    btn = [[
        InlineKeyboardButton("Aujourd'hui", callback_data=f'vrrfrs#tud'), 
        InlineKeyboardButton(f"{today}", callback_data=f'vrrfrs#tud')
        ],[
        InlineKeyboardButton("Hier", callback_data=f'vrrfrs#yes'), 
        InlineKeyboardButton(f"{yesterday}", callback_data=f'vrrfrs#yes')
        ],[
        InlineKeyboardButton("Cette semaine", callback_data=f'vrrfrs#week'), 
        InlineKeyboardButton(f"{this_week}", callback_data=f'vrrfrs#week')     
        ],[
        InlineKeyboardButton("Ce mois", callback_data=f'vrrfrs#mont'), 
        InlineKeyboardButton(f"{this_month}", callback_data=f'vrrfrs#mont')
        ],[
        InlineKeyboardButton("Mois dernier", callback_data=f'vrrfrs#lmont'), 
        InlineKeyboardButton(f"{last_month}", callback_data=f'vrrfrs#lmont')        
        ],[
        InlineKeyboardButton("Cette année", callback_data=f'vrrfrs#tyear'), 
        InlineKeyboardButton(f"{this_year}", callback_data=f'vrrfrs#tyear')
        ],[
        InlineKeyboardButton("Année dernière", callback_data=f'vrrfrs#lyear'), 
        InlineKeyboardButton(f"{last_year}", callback_data=f'vrrfrs#lyear')
        ],[
        InlineKeyboardButton("🔄 Actualiser", callback_data=f'vrrfrs#vrrfrs'), 
    ]] 
    try: 
        await query.message.edit("✅ **#Vérification**\n\nUtilisateurs vérifiés au total", reply_markup=InlineKeyboardMarkup(btn))
    except MessageNotModified:
        pass
    await query.answer("Actualisation des données ✅......")