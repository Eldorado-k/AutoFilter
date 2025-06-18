import time
import asyncio
from pyrogram import Client, filters
import platform
import os
import shutil
import logging
from pyrogram.types import BotCommand
from info import ADMINS, Bot_cmds

logging.basicConfig(level=logging.INFO)

CMD = ["/", "."]  

@Client.on_message(filters.command("vie", CMD))
async def check_alive(_, message):
    sticker = await message.reply_sticker("CAACAgQAAxkBAAJG_mhSb64Uq2vXVTZF_-tUTx-qMqPVAAJwEwACci8AAVO7CAXN8ask_R4E") 
    text = await message.reply_text("Vous avez de la chance 🤞 Je suis en vie ❤️\nAppuyez sur /start pour m'utiliser !")
    await asyncio.sleep(60)
    await sticker.delete()
    await text.delete()
    await message.delete()

@Client.on_message(filters.command("ping", CMD))
async def ping(_, message):
    start_t = time.time()
    rm = await message.reply_text("...")
    end_t = time.time()
    time_taken_s = (end_t - start_t) * 1000
    await rm.edit(f"🏓 Pong ! : {time_taken_s:.3f} ms")
    await asyncio.sleep(60)
    await rm.delete()
    await message.delete()

start_time = time.time()

def format_time(seconds):
    """Convertir les secondes au format H:M:S."""
    minutes, sec = divmod(int(seconds), 60)
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {sec}s"

def get_size(size_kb):
    """Convertir les Ko dans un format lisible."""
    size_bytes = int(size_kb) * 1024
    for unit in ['o', 'Ko', 'Mo', 'Go', 'To']:
        if size_bytes < 1024:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024
    return f"{size_bytes:.2f} Po"

def get_system_info():
    bot_uptime = format_time(time.time() - start_time)
    os_info = f"{platform.system()}"
    try:
        with open('/proc/uptime') as f:
            system_uptime = format_time(float(f.readline().split()[0]))
    except Exception:
        system_uptime = "Indisponible"
    try:
        with open('/proc/meminfo') as f:
            meminfo = f.readlines()
        total_ram = get_size(meminfo[0].split()[1])  
        available_ram = get_size(meminfo[2].split()[1])  
        used_ram = get_size(int(meminfo[0].split()[1]) - int(meminfo[2].split()[1]))
    except Exception:
        total_ram, used_ram = "Indisponible", "Indisponible"
    try:
        total_disk, used_disk, _ = shutil.disk_usage("/")
        total_disk = get_size(total_disk // 1024)
        used_disk = get_size(used_disk // 1024)
    except Exception:
        total_disk, used_disk = "Indisponible", "Indisponible"

    system_info = (
        f"💻 **Informations système**\n\n"
        f"🖥️ **OS :** {os_info}\n"
        f"⏰ **Temps de fonctionnement du bot :** {bot_uptime}\n"
        f"🔄 **Temps de fonctionnement du système :** {system_uptime}\n"
        f"💾 **Utilisation RAM :** {used_ram} / {total_ram}\n"
        f"📁 **Utilisation disque :** {used_disk} / {total_disk}\n"
    )
    return system_info

async def calculate_latency():
    start = time.time()
    await asyncio.sleep(0)  
    end = time.time()
    latency = (end - start) * 1000
    return f"{latency:.3f} ms"

@Client.on_message(filters.command("system"))
async def send_system_info(client, message):
    system_info = get_system_info()
    latency = await calculate_latency() 
    full_info = f"{system_info}\n📶 **Latence :** {latency}"
    info = await message.reply_text(full_info)
    await asyncio.sleep(60)
    await info.delete()
    await message.delete()


@Client.on_message(filters.command("commands") & filters.user(ADMINS))
async def set_commands(client, message):
    commands = [BotCommand(cmd, desc) for cmd, desc in Bot_cmds.items()]
    await client.set_bot_commands(commands)
    bot_set = await message.reply("Commandes du bot mises à jour avec succès ✅")
    await asyncio.sleep(119)  
    await bot_set.delete()
    await message.delete()