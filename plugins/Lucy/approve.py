import os
import asyncio
from info import *
from pyrogram import Client, filters
from pyrogram.types import Message, User, ChatJoinRequest, InlineKeyboardMarkup, InlineKeyboardButton

# Default settings
APPROVAL_WAIT_TIME = 10  # seconds
AUTO_APPROVE_ENABLED = True  # Toggle for enabling/disabling auto approval

@Client.on_chat_join_request((filters.group | filters.channel) & filters.chat(CHAT_ID) if CHAT_ID else (filters.group | filters.channel))
async def autoapprove(client, message: ChatJoinRequest):
    global AUTO_APPROVE_ENABLED

    if not AUTO_APPROVE_ENABLED:
        return

    chat = message.chat
    user = message.from_user
    print(f"{user.first_name} requested to join {chat.title}")
    
    await asyncio.sleep(APPROVAL_WAIT_TIME)
    
    await client.approve_chat_join_request(chat_id=chat.id, user_id=user.id)
    
    if APPROVED == "on":
        invite_link = await client.export_chat_invite_link(chat.id)
        buttons = [
            [InlineKeyboardButton('• Rejoindre mes mises à jour •', url='https://t.me/BotZFlix')],
            [InlineKeyboardButton(f'• Rejoindre {chat.title} •', url=invite_link)]
        ]
        markup = InlineKeyboardMarkup(buttons)
        caption = f"<b>Bonjour {user.mention()},\n\nVotre demande pour rejoindre {chat.title} a été approuvée.</b>"
        
        await client.send_photo(
            chat_id=user.id,
            photo='https://graph.org/file/af409141d781c8ff521e4.jpg',
            caption=caption,
            reply_markup=markup
        )

@Client.on_message(filters.command("reqtime") & filters.user(ADMINS))
async def set_reqtime(client, message: Message):
    global APPROVAL_WAIT_TIME
    
    if len(message.command) != 2 or not message.command[1].isdigit():
        return await message.reply_text("Utilisation : <code>/reqtime {secondes}</code>")
    
    APPROVAL_WAIT_TIME = int(message.command[1])
    await message.reply_text(f"✅ Temps d'approbation défini à <b>{APPROVAL_WAIT_TIME}</b> secondes.")

@Client.on_message(filters.command("reqmode") & filters.user(ADMINS))
async def toggle_reqmode(client, message: Message):
    global AUTO_APPROVE_ENABLED
    
    if len(message.command) != 2 or message.command[1].lower() not in ["on", "off"]:
        return await message.reply_text("Utilisation : <code>/reqmode on</code> ou <code>/reqmode off</code>")
    
    mode = message.command[1].lower()
    AUTO_APPROVE_ENABLED = (mode == "on")
    status = "activé ✅" if AUTO_APPROVE_ENABLED else "désactivé ❌"
    await message.reply_text(f"L'approbation automatique a été {status}.")