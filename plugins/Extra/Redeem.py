from datetime import timedelta, datetime
import pytz
import string
import random
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from database.users_chats_db import db
from info import ADMINS, PREMIUM_LOGS
from utils import get_seconds, temp

REDEEM_CODE = {}

def generate_code(length=10):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))

@Client.on_message(filters.command("add_redeem") & filters.user(ADMINS))
async def add_redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 3:
        try:
            time = message.command[1]
            num_codes = int(message.command[2])
        except ValueError:
            await message.reply_text("Veuillez fournir un nombre valide de codes à générer.")
            return

        codes = []
        for _ in range(num_codes):
            code = generate_code()
            REDEEM_CODE[code] = time
            codes.append(code)

        codes_text = '\n'.join(f"➔ <code>/redeem {code}</code>" for code in codes)
        text = f"""
            <b>🎉 <u>Code cadeau généré ✅</u></b>

            <b> <u>Nombre total de codes :</u></b> {num_codes}

            {codes_text}

            <b>⏳ <u>Durée :</u></b> {time}

            🌟<u>Instructions pour utiliser le code</u>🌟

            <b> <u>Cliquez sur le code ci-dessus</u> pour le copier instantanément !</b>
            <b> <u>Envoyez le code copié au bot</u>\npour débloquer vos fonctionnalités premium !</b>

            <b>🚀 Profitez de votre accès premium ! 🔥</u></b>
            """
        keyboard = InlineKeyboardMarkup([[InlineKeyboardButton("🔑 Utiliser maintenant 🔥", url=f"https://t.me/{temp.U_NAME}")]])
        await message.reply_text(text, reply_markup=keyboard)
    else:
        await message.reply_text("<b>♻ Utilisation :\n\n➩ <code>/add_redeem 1min 1</code>,\n➩ <code>/add_redeem 1hour 10</code>,\n➩ <code>/add_redeem 1day 5</code></b>")


@Client.on_message(filters.command("redeem"))
async def redeem_code(client, message):
    user_id = message.from_user.id
    if len(message.command) == 2:
        redeem_code = message.command[1]

        if redeem_code in REDEEM_CODE:
            try:
                time = REDEEM_CODE.pop(redeem_code)
                user = await client.get_users(user_id)
                try:
                    seconds = await get_seconds(time)
                except Exception:
                    await message.reply_text("Format de temps invalide dans le code.")
                    return
                if seconds > 0:
                    data = await db.get_user(user_id)
                    current_expiry = data.get("expiry_time") if data else None
                    now_aware = datetime.now(pytz.utc)

                    if current_expiry:
                        current_expiry = current_expiry.replace(tzinfo=pytz.utc)
                    if current_expiry and current_expiry > now_aware:
                        expiry_str_in_ist = current_expiry.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")
                        await message.reply_text(
                            f"🚫 <b>Vous avez déjà un accès premium actif !</b>\n\n"
                            f"⏳ <b>Expiration du premium actuel :</b> {expiry_str_in_ist}\n\n"
                            f"<i>Vous ne pouvez pas utiliser un autre code tant que votre accès premium actuel n'a pas expiré.</i>\n\n"
                            f"<b>Merci d'utiliser notre service ! 🔥</b>",
                            disable_web_page_preview=True
                        )
                        return
                    expiry_time = now_aware + timedelta(seconds=seconds)
                    user_data = {"id": user_id, "expiry_time": expiry_time}
                    await db.update_user(user_data)

                    expiry_str_in_ist = expiry_time.astimezone(pytz.timezone("Africa/Lome")).strftime("%d-%m-%Y\n⏱️ Heure d'expiration : %I:%M:%S %p")
                    await message.reply_text(
                        f"🎉 <b>Premium activé avec succès ! 🚀</b>\n\n"
                        f"👤 <b>Utilisateur :</b> {user.mention}\n"
                        f"⚡ <b>ID Utilisateur :</b> <code>{user_id}</code>\n"
                        f"⏳ <b>Durée de l'accès premium :</b> <code>{time}</code>\n"
                        f"⌛️ <b>Date d'expiration :</b> {expiry_str_in_ist}",
                        disable_web_page_preview=True
                    )
                    log_message = f"""
                        #Redeem_Premium 🔓

                        👤 <b>Utilisateur :</b> {user.mention}
                        ⚡ <b>ID Utilisateur :</b> <code>{user_id}</code>
                        ⏳ <b>Durée de l'accès premium :</b> <code>{time}</code>
                        ⌛️ <b>Date d'expiration :</b> {expiry_str_in_ist}

                        🎉 Premium activé avec succès ! 🚀
                        """
                    await client.send_message(
                        PREMIUM_LOGS,
                        text=log_message,
                        disable_web_page_preview=True
                    )
                else:
                    await message.reply_text("Format de temps invalide dans le code.")
            except Exception as e:
                await message.reply_text(f"Une erreur s'est produite lors de l'utilisation du code : {e}")
        else:
            await message.reply_text("Code invalide ou expiré.")
    else:
        await message.reply_text("Utilisation : /redeem <code>")