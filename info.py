import re
import os
from os import environ, getenv
from Script import script

# Utility functions
id_pattern = re.compile(r'^.\d+$')

def is_enabled(value, default):
    if value.lower() in ["true", "yes", "1", "enable", "y"]:
        return True
    elif value.lower() in ["false", "no", "0", "disable", "n"]:
        return False
    else:
        return default

# ============================
# Bot Information Configuration
# ============================
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ.get('API_ID', '24817837'))
API_HASH = environ.get('API_HASH', 'acd9f0cc6beb08ce59383cf250052686')
BOT_TOKEN = environ.get('BOT_TOKEN', "7783135016:AAHlbGLRu1f-E1Uqtfl7_vd8CC33cFX4fJE")
# ============================
# Bot Settings Configuration
# ============================
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))

PICS = (environ.get('PICS', 'https://iili.io/FoH3o0b.md.jpg https://iili.io/FoHdknn.jpg https://iili.io/FoHdCT7.jpg https://iili.io/FoHKKPe.md.jpg')).split()  # Sample pic
NOR_IMG = environ.get("NOR_IMG", "https://envs.sh/Wdj.jpg")
MELCOW_VID = environ.get("MELCOW_VID", "https://envs.sh/Wdj.jpg")
SPELL_IMG = environ.get("SPELL_IMG", "https://envs.sh/Wdj.jpg")
SUBSCRIPTION = (environ.get('SUBSCRIPTION', 'https://iili.io/FoHdknn.jpg'))
FSUB_PICS = (environ.get('FSUB_PICS', 'https://iili.io/FoH1H5x.md.jpg')).split()  # Fsub pic

# ============================
# Admin, Channels & Users Configuration
# ============================
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '7428552084').split()] # Replace with the actual admin ID(s) to add
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '-1002463797892').split()]  # Channel id for auto indexing (make sure bot is admin)
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', '-1002757788052'))  # Log channel id (make sure bot is admin)
BIN_CHANNEL = int(environ.get('BIN_CHANNEL', '-1002376378205'))  # Bin channel id (make sure bot is admin)
MOVIE_UPDATE_CHANNEL = int(environ.get('MOVIE_UPDATE_CHANNEL', '-1002376378205'))  # Notification of those who verify will be sent to your channel
PREMIUM_LOGS = int(environ.get('PREMIUM_LOGS', '-1002376378205'))  # Premium logs channel id
auth_channel = environ.get('AUTH_CHANNEL', '-1002722250222')  # Channel/Group ID for force sub (make sure bot is admin)
DELETE_CHANNELS = [int(dch) if id_pattern.search(dch) else dch for dch in environ.get('DELETE_CHANNELS', '').split()]
support_chat_id = environ.get('SUPPORT_CHAT_ID', '-1002165407793')  # Support group id (make sure bot is admin)
reqst_channel = environ.get('REQST_CHANNEL_ID', '-1002376378205')  # Request channel id (make sure bot is admin)
AUTH_CHANNEL = [int(fch) if id_pattern.search(fch) else fch for fch in environ.get('AUTH_CHANNEL', '-1002800117370 -1002647818964 -1002387859851').split()]
MULTI_FSUB = [int(channel_id) for channel_id in environ.get('MULTI_FSUB', '-1002800117370 -1002647818964 -1002387859851').split() if re.match(r'^-?\d+$', channel_id)]  # Channel for force sub (make sure bot is admin)


# ============================
# Payment Configuration
# ============================
QR_CODE = environ.get('QR_CODE', 'https://envs.sh/Wdj.jpg')
OWNER_UPI_ID = environ.get('OWNER_UPI_ID', '@fam')

#Auto approve 
CHAT_ID = [int(app_chat_id) if id_pattern.search(app_chat_id) else app_chat_id for app_chat_id in environ.get('CHAT_ID', '').split()]
TEXT = environ.get("APPROVED_WELCOME_TEXT", "<b>{mention},\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ᴛᴏ ᴊᴏɪɴ {title} ɪs ᴀᴘᴘʀᴏᴠᴇᴅ.\n\‣ ᴘᴏᴡᴇʀᴇᴅ ʙʏ @BotZFlix</b>")
APPROVED = environ.get("APPROVED_WELCOME", "on").lower()


# ============================
# MongoDB Configuration
# ============================
DATABASE_URI = environ.get('DATABASE_URI', "mongodb+srv://tgbot:4KzEdxEl4YldwwFR@tg.vr8ef.mongodb.net/?retryWrites=true&w=majority&appName=Tg")
DATABASE_URI2 = environ.get('DATABASE_URI2', "mongodb+srv://Ethan:Ethan123@telegrambots.lva9j.mongodb.net/?retryWrites=true&w=majority&appName=TELEGRAMBOTS")
DATABASE_NAME = environ.get('DATABASE_NAME', "kingcey")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Lucy_files')

# ============================
# Movie Notification & Update Settings
# ============================
MOVIE_UPDATE_NOTIFICATION = bool(environ.get('MOVIE_UPDATE_NOTIFICATION', True))  # Notification On (True) / Off (False)
IMAGE_FETCH = bool(environ.get('IMAGE_FETCH', True))  # On (True) / Off (False)
CAPTION_LANGUAGES = ["Vostfr", "English", "French"]

# ============================
# Verification Settings
# ============================
VERIFY = bool(environ.get('VERIFY', False))  # Verification On (True) / Off (False)
VERIFY_EXPIRE = int(environ.get('VERIFY_EXPIRE', 7))  # Add time in hours
VERIFIED_LOG = int(environ.get('VERIFIED_LOG', '-1002376378205'))  # Log channel id (make sure bot is admin)
HOW_TO_VERIFY = environ.get('HOW_TO_VERIFY', 'https://t.me/BotZFlix/195')  # How to open tutorial link for verification

# ============================
# Link Shortener Configuration
# ============================
IS_SHORTLINK = bool(environ.get('IS_SHORTLINK', True))
SHORTLINK_URL = environ.get('SHORTLINK_URL', 'shareus.io')
SHORTLINK_API = environ.get('SHORTLINK_API', 'nJ0xMvXlLEhpVcJK2MjvU6Vxx6u2')
TUTORIAL = environ.get('TUTORIAL', 'https://t.me/BotZFlix/195')  # Tutorial video link for opening shortlink website
IS_TUTORIAL = bool(environ.get('IS_TUTORIAL', True))

# ============================
# Channel & Group Links Configuration
# ============================
GRP_LNK = environ.get('GRP_LNK', 'https://t.me/ZFlixTeam')
CHNL_LNK = environ.get('CHNL_LNK', 'https://t.me/AntiFlix_A')
OWNER_LNK = environ.get('OWNER_LNK', 'https://t.me/Kingcey')
MOVIE_UPDATE_CHANNEL_LNK = environ.get('MOVIE_UPDATE_CHANNEL_LNK', 'https://t.me/AnimLoko')
OWNERID = int(os.environ.get('OWNERID', '7428552084'))  # Replace with the actual admin ID

# ============================
# User Configuration
# ============================
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '7428552084').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
PREMIUM_USER = [int(user) if id_pattern.search(user) else user for user in environ.get('PREMIUM_USER', '7428552084').split()]

# ============================
# Miscellaneous Configuration
# ============================
NO_RESULTS_MSG = bool(environ.get("NO_RESULTS_MSG", True))  # True if you want no results messages in Log Channel
MAX_B_TN = environ.get("MAX_B_TN", "15")
MAX_BTN = is_enabled((environ.get('MAX_BTN', "True")), True)
PORT = environ.get("PORT", "8080")
MSG_ALRT = environ.get('MSG_ALRT', 'Créé Par @Kingcey')
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'https://t.me/AntiFlix_d')  # Support group link (make sure bot is admin)
P_TTI_SHOW_OFF = is_enabled((environ.get('P_TTI_SHOW_OFF', "False")), False)
IMDB = is_enabled((environ.get('IMDB', "True")), False)
AUTO_FFILTER = is_enabled((environ.get('AUTO_FFILTER', "True")), True)
AUTO_DELETE = is_enabled((environ.get('AUTO_DELETE', "True")), True)
DELETE_TIME = int(environ.get("DELETE_TIME", "86400"))  #  deletion time in seconds (default: 5 minutes). Adjust as per your needs.
SINGLE_BUTTON = is_enabled((environ.get('SINGLE_BUTTON', "False")), False) # pm & Group button or link mode (True) / Off (False)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", f"{script.CAPTION}")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", CUSTOM_FILE_CAPTION)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", f"{script.IMDB_TEMPLATE_TXT}")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled((environ.get('MELCOW_NEW_USERS', "False")), False)
PROTECT_CONTENT = is_enabled((environ.get('PROTECT_CONTENT', "False")), True)
PUBLIC_FILE_STORE = is_enabled((environ.get('PUBLIC_FILE_STORE', "True")), True)
PM_SEARCH = bool(environ.get('PM_SEARCH', False))  # PM Search On (True) / Off (False)
EMOJI_MODE = bool(environ.get('EMOJI_MODE', True))  # Emoji status On (True) / Off (False)

# ============================
# Bot Configuration
# ============================
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None
REQST_CHANNEL = int(reqst_channel) if reqst_channel and id_pattern.search(reqst_channel) else None
SUPPORT_CHAT_ID = int(support_chat_id) if support_chat_id and id_pattern.search(support_chat_id) else None
LANGUAGES = ["hindi", "english", "french"]
QUALITIES = ["360P", "HdRip", "480P", "540P", "720P", "bluray", "1080P", "1440P", "2160P", "4k", "WebRiP"]
SEASONS = ["saison 1" , "saison 2" , "saison 3" , "saison 4", "saison 5" , "saison 6" , "saison 7" , "saison 8" , "saison 9" , "saison 10"]

# ============================
# Server & Web Configuration
# ============================

STREAM_MODE = bool(environ.get('STREAM_MODE', True)) # Set Stream mode True or False

NO_PORT = bool(environ.get('NO_PORT', False))
APP_NAME = None
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = environ.get('APP_NAME')
else:
    ON_HEROKU = False
BIND_ADRESS = str(getenv('WEB_SERVER_BIND_ADDRESS', '8.8.8.8'))
FQDN = str(getenv('FQDN', BIND_ADRESS)) if not ON_HEROKU or getenv('FQDN') else APP_NAME+'https://lovely-sula-justpourgpt-e4d6e688.koyeb.app/'
URL = "https://{}/".format(FQDN) if ON_HEROKU or NO_PORT else "https://{}/".format(FQDN, PORT)
SLEEP_THRESHOLD = int(environ.get('SLEEP_THRESHOLD', '60'))
WORKERS = int(environ.get('WORKERS', '4'))
SESSION_NAME = str(environ.get('SESSION_NAME', 'kingcey'))
MULTI_CLIENT = False
name = str(environ.get('name', 'Deendayal'))
PING_INTERVAL = int(environ.get("PING_INTERVAL", "1200"))  # 20 minutes
if 'DYNO' in environ:
    ON_HEROKU = True
    APP_NAME = str(getenv('APP_NAME'))
else:
    ON_HEROKU = False
HAS_SSL = bool(getenv('HAS_SSL', True))
if HAS_SSL:
    URL = "https://{}/".format(FQDN)
else:
    URL = "http://{}/".format(FQDN)

# ============================
# Reactions Configuration
# ============================
REACTIONS = ["🤝", "😇", "🤗", "😍", "👍", "🎅", "😐", "🥰", "🤩", "😱", "🤣", "😘", "👏", "😛", "😈", "🎉", "⚡️", "🫡", "🤓", "😎", "🏆", "🔥", "🤭", "🌚", "🆒", "👻", "😁"]



# ============================
# Command admin
# ============================
commands = [
    """• /system - <code>Informations système</code>
• /del_msg - <code>Supprimer les notifications de collection de noms de fichiers</code>
• /movie_update - <code>Activer/désactiver selon vos besoins...</code>
• /pm_search - <code>Recherche en MP activer/désactiver selon vos besoins...</code>
• /logs - <code>Obtenir les erreurs récentes</code>
• /delete - <code>Supprimer un fichier spécifique de la base de données</code>
• /users - <code>Obtenir la liste de mes utilisateurs et leurs IDs</code>
• /chats - <code>Obtenir la liste de mes chats et leurs IDs</code>
• /leave - <code>Quitter un chat</code>
• /disable - <code>Désactiver un chat</code>""",

    """• /ban - <code>Bannir un utilisateur</code>
• /unban - <code>Débannir un utilisateur</code>
• /channel - <code>Obtenir la liste des groupes connectés</code>
• /broadcast - <code>Diffuser un message à tous les utilisateurs</code>
• /grp_broadcast - <code>Diffuser un message à tous les groupes connectés</code>
• /clear_junk - <code>Nettoyer les utilisateurs inactifs</code>
• /junk_group - <code>Nettoyer les groupes inactifs</code>
• /gfilter - <code>Ajouter des filtres globaux</code>
• /gfilters - <code>Voir la liste de tous les filtres globaux</code>
• /delg - <code>Supprimer un filtre global spécifique</code>
• /delallg - <code>Supprimer tous les filtres globaux de la base de données</code>
• /deletefiles - <code>Supprimer les fichiers CamRip et PreDVD de la base de données</code>
• /send - <code>Envoyer un message à un utilisateur spécifique</code>""",

    """• /add_premium - <code>Ajouter un utilisateur premium</code>
• /remove_premium - <code>Retirer un utilisateur premium</code>
• /premium_users - <code>Obtenir la liste des utilisateurs premium</code>
• /get_premium - <code>Obtenir les infos d'un utilisateur premium</code>
• /restart - <code>Redémarrer le bot</code>"""
]

# ============================
# Commandes du Bot
# ============================
Bot_cmds = {
    "start": "Démarrer le bot",
    "alive": "Vérifier si le bot est en ligne",
    "settings": "Modifier les paramètres",
    "id": "Obtenir l'ID Telegram",
    "info": "Obtenir les infos utilisateur",
    "system": "Informations système",
    "del_msg": "Supprimer les notifications de collection de noms de fichiers",
    "movie_update": "Activer/désactiver les mises à jour de films",
    "pm_search": "Activer/désactiver la recherche en MP",
    "trendlist": "Obtenir la liste des recherches tendances",
    "logs": "Obtenir les erreurs récentes",
    "delete": "Supprimer un fichier spécifique de la base de données",
    "users": "Obtenir la liste des utilisateurs et leurs IDs",
    "chats": "Obtenir la liste des chats et leurs IDs",
    "leave": "Quitter un chat",
    "disable": "Désactiver un chat",
    "ban": "Bannir un utilisateur",
    "unban": "Débannir un utilisateur",
    "channel": "Obtenir la liste des groupes connectés",
    "broadcast": "Diffuser un message à tous les utilisateurs",
    "grp_broadcast": "Diffuser un message à tous les groupes connectés",
    "clear_junk": "Nettoyer les utilisateurs inactifs",
    "junk_group": "Nettoyer les groupes inactifs",
    "gfilter": "Ajouter des filtres globaux",
    "gfilters": "Voir tous les filtres globaux",
    "delg": "Supprimer un filtre global spécifique",
    "delallg": "Supprimer tous les filtres globaux",
    "deletefiles": "Supprimer les fichiers CamRip et PreDVD",
    "send": "Envoyer un message à un utilisateur spécifique",
    "add_premium": "Ajouter un utilisateur premium",
    "remove_premium": "Retirer un utilisateur premium",
    "premium_users": "Liste des utilisateurs premium",
    "get_premium": "Infos d'un utilisateur premium",
    "restart": "Redémarrer le bot"
}




# ============================
# Logs Configuration
# ============================
LOG_STR = "Current Customized Configurations are:-\n"
LOG_STR += ("IMDB Results are enabled, Bot will be showing imdb details for your queries.\n" if IMDB else "IMDB Results are disabled.\n")
LOG_STR += ("P_TTI_SHOW_OFF found, Users will be redirected to send /start to Bot PM instead of sending file directly.\n" if P_TTI_SHOW_OFF else "P_TTI_SHOW_OFF is disabled, files will be sent in PM instead of starting the bot.\n")
LOG_STR += ("SINGLE_BUTTON is found, filename and file size will be shown in a single button instead of two separate buttons.\n" if SINGLE_BUTTON else "SINGLE_BUTTON is disabled, filename and file size will be shown as different buttons.\n")
LOG_STR += (f"CUSTOM_FILE_CAPTION enabled with value {CUSTOM_FILE_CAPTION}, your files will be sent along with this customized caption.\n" if CUSTOM_FILE_CAPTION else "No CUSTOM_FILE_CAPTION Found, Default captions of file will be used.\n")
LOG_STR += ("Long IMDB storyline enabled." if LONG_IMDB_DESCRIPTION else "LONG_IMDB_DESCRIPTION is disabled, Plot will be shorter.\n")
LOG_STR += ("Spell Check Mode is enabled, bot will be suggesting related movies if movie name is misspelled.\n" if SPELL_CHECK_REPLY else "Spell Check Mode is disabled.\n")

