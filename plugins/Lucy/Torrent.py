import asyncio
from pyrogram import Client, filters
import requests
from info import LOG_CHANNEL

@Client.on_message(filters.command("torrent"))
async def torrent_search(client, message):
    try:
        # Récupérer la requête de l'utilisateur
        user_query = message.text.split()[1:]
        if not user_query:
            await message.reply_text("Veuillez fournir un nom de film, <code>/torrent nom du film</code>")
            return 
        
        # Encoder la requête pour l'URL
        encoded_query = " ".join(user_query).replace(" ", "%20")

        # Faire la requête à l'API Torrent
        response = requests.get(f"https://api.safone.dev/torrent?query={encoded_query}&limit=1")
        
        if response.status_code == 200:
            data = response.json()
            
            # Vérifier si des résultats existent
            if not data['results']:
                await message.reply_text("Aucun torrent trouvé pour cette recherche.")
                return
                
            torrent_r = data['results'][0]
          
            # Formater la réponse
            tor = f"**📁 Nom du fichier:** <code>{torrent_r['name']}</code>\n\n"\
                  f"**📏 Taille:** <code>{torrent_r['size']}</code>\n" \
                  f"**📌 Type:** <code>{torrent_r['type']}</code>\n" \
                  f"**🌐 Langue:** <code>{torrent_r['language']}</code>\n" \
                  f"**🧲 Lien Magnet:** \n<code>{torrent_r['magnetLink']}</code>"
    
            # Envoyer les résultats
            await client.send_message(message.chat.id, tor)
            
            # Logger dans le canal de logs
            log_msg = f"#TORRENT\nUtilisateur: {message.from_user.mention}\nRecherche: {' '.join(user_query)}"
            await client.send_message(LOG_CHANNEL, text=log_msg)
            
    except IndexError:
        await message.reply_text("Format incorrect. Utilisez: <code>/torrent nom du film</code>")
    except Exception as e:
        await message.reply_text(f"Une erreur est survenue: {str(e)}")