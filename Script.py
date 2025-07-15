class script(object):
    START_TXT = """<b>Salut {}, {}\n\nJe Suis Marsh ƈɾσɯ V2.0 je suis un puissant bot Marsh ƈɾσɯ Je peux vous fournir des Films Et des Séries de tout genre mais je peux maintenant vous fournir des Cartoons (dessin animés). Rejoins mon canal et mon Groupe puis profite de ta journée!\n\n<blockquote>‣ Maintenu par : <a href="https://t.me/JobeTECH">J-TECH</a></blockquote></b>"""

    GSTART_TXT = """<b>Salut {}, {}\n\nJe suis le bot de filtrage automatique le plus puissant avec des fonctionnalités premium, ajoute-moi simplement à ton groupe et profite !\n\n<blockquote>‣ Maintenu par : <a href="https://t.me/JobeTECH">BotZFlix</a></blockquote></b>"""
    
    HELP_TXT = """» Où veux-tu ouvrir le menu des paramètres ?"""

    ABOUT_TXT = """<blockquote><b>❍ Mon nom : <a href="https://t.me/Marsh_Mello_bot">Lucy Bot</a>
❍ Créateur : Inconnu
❍ Bibliothèque : <a href="https://pyrogram.org/">Pyrogram</a>
❍ Langage : <a href="https://www.python.org/">Python</a>
❍ Base de données : <a href="https://www.mongodb.com/">Mongo DB</a>
❍ Hébergé sur : <a href="https://t.me/Neko_Crunchy">Vercel</a>
❍ Statut de version : v3 [Avancé]</blockquote>

➻ Clique sur les boutons ci-dessous pour obtenir de l'aide de base et des informations sur moi.</b>"""
        
    MAIN_TXT = """
Voici le menu d'aide
"""

    SUPPORT_TXT = """Voici mes canaux et groupes de support. Si tu as un problème, signale-le à l'admin.
Propulsé par - @paq_Land"""
        
    HELPS_TXT = """» Où veux-tu ouvrir le menu des paramètres ?"""
    
    CHANNELS = """
<b>๏ Clique sur les boutons ci-dessous pour rejoindre les canaux et obtenir plus d'informations sur nous.

Si tu trouves un bug ou si tu veux donner ton avis sur le bot, merci de le signaler au <a href='https://t.me/BTZF_CHAT'>groupe de support</a>.</b>"""

    
    STATUS_TXT = """<b>╭────[ 🗃 Base de données 1 🗃 ]────⍟</b>
│
├⋟ 🕵️ Tous les utilisateurs ⋟ <code>{}</code>
├⋟ 🏹 Tous les groupes ⋟ <code>{}</code>
├⋟ ❤️‍🔥 Utilisateurs Premium ⋟ <code>{}</code>
├⋟ 🎬 Tous les fichiers ⋟ <code>{}</code>
├⋟ 📽️ Stockage utilisé ⋟ <code>{}</code>
├⋟ 🏷️ Stockage libre ⋟ <code>{}</code>
│
<b>├────[ 🗳 Base de données 2 🗳 ]────⍟</b>   
│
├⋟ 🎬 Tous les fichiers ➤ <code>{}</code>
├⋟ 🎤 Taille ➤ <code>{}</code>
├⋟ 🎭 Libre ➤ <code>{}</code>
│
<b>├────[ 🤖 Détails du bot 🤖 ]────⍟</b>   
│
├⋟ ⏱ Temps de fonctionnement ➤ {}
├⋟ 🌐 RAM ➤ <code>{}%</code>
├⋟ 🤖 CPU ➤ <code>{}%</code>   
│
├⋟ 🗼 Fichiers dans les deux DBs: <code>{}</code>
│
<b>╰─────────────────────⍟</b>"""

    LOG_TEXT_G = """#NouveauGroupe
    
Groupe = {}
ID = <code>{}</code>
Nombre total de membres = <code>{}</code>
Ajouté par - {}
"""

    LOG_TEXT_P = """#NouvelUtilisateur
    
ID - <code>{}</code>
Nom - {}
"""

    ALRT_TXT = """Salut {},
ce n'est pas ta demande de film,
demande le tien..."""

    OLD_ALRT_TXT = """Hey {},
tu utilises un de mes anciens messages,
merci de renvoyer la demande."""

    CUDNT_FND = """<b>😴 Ta demande n'a pas été trouvée dans ma base de données.\n\n<blockquote>» Peut-être que tu as mal orthographié, tu ne fais pas tes devoirs non plus !</blockquote></b>"""

    I_CUDNT = """<b>Désolé, aucun fichier trouvé pour ta demande {}

» Vérifie ton orthographe sur Google et réessaye

» Format pour les demandes de films :

‣ Exemple : Straw ou Straw 2025 
‣ Format pour les séries 👇
‣ Exemple : Loki S01 ou Loki S01E04 ou Lucifer S03E24

» N'utilise pas ➠ ':(!,./)</b>"""
    
    I_CUD_NT = """<b>Je n'ai trouvé aucun film lié à {}.

» Raisons possibles :

1) Pas encore sorti en O.T.T. ou DVD
2) Indique le nom avec l'année
3) Le film n'est pas disponible dans la base de données, signale aux admins</b>"""

    MVE_NT_FND = """<b>😴 Ta demande n'a pas été trouvée dans ma base de données.\n\n<blockquote>» Peut-être que tu as mal orthographié, tu ne fais pas tes devoirs non plus !</blockquote></b>"""
    

    TOP_ALRT_MSG = """Recherche de la demande dans ma base de données..."""

    MELCOW_ENG = """<b>👋 Salut {},\n\n🍁 Bienvenue dans\n🌟 {} \n\n🔍 Ici tu peux rechercher tes films ou séries préférés en tapant simplement leur nom 🔎\n\n⚠️ Si tu as un problème concernant le téléchargement ou autre, message ici 👇</b>"""
    
    DISCLAIMER_TXT = """
<blockquote><b>Ceci est un projet open source.

Tous les fichiers de ce bot sont librement disponibles sur Internet ou postés par quelqu'un d'autre. Juste pour faciliter la recherche, ce bot indexe les fichiers qui sont déjà uploadés sur Telegram. Nous respectons toutes les lois sur le copyright et travaillons en conformité avec le DMCA et l'EUCD. Si quelque chose est illégal, contacte-moi pour que je puisse le supprimer rapidement. Il est interdit de télécharger, streamer, reproduire, partager ou consommer du contenu sans permission explicite du créateur ou du détenteur des droits. Si tu penses que ce bot viole ta propriété intellectuelle, contacte les canaux respectifs pour suppression. Le bot ne possède aucun de ces contenus, il indexe seulement les fichiers depuis Telegram.</b></blockquote>"""

    USERS_TXT = """👋 Salut {},

📚 Voici ma liste de commandes pour tous les utilisateurs du bot ⇊
    
• /batch - Créer un lien batch pour plusieurs fichiers.
• /link - Créer un lien de stockage pour un seul fichier.
• /pbatch - Comme <code>/batch</code>, mais avec restrictions de transfert.
• /plink - Comme <code>/link</code>, mais avec restrictions de transfert.
• /id - Obtenir l'ID d'un utilisateur spécifique.
• /info - Obtenir des informations sur un utilisateur.
• /imdb - Obtenir les infos du film depuis IMDB.
• /search - Obtenir les infos du film depuis diverses sources.
• /stats - Obtenir le statut des fichiers dans la base de données.
• /request - Envoyer une demande de film/série aux admins du bot. (Fonctionne seulement dans le groupe de support)
• /plan - Voir les plans d'abonnement premium disponibles.
• /myplan - Voir ton plan actuel."""

    
    ADMIC_TXT = """👋 Salut {},

📚 Voici ma liste de commandes pour tous les admins du bot ⇊

• /system - <code>Informations système</code>
• /del_msg - <code>Supprimer la notification de collecte de noms de fichiers...</code> 
• /movie_update - <code>Activer/désactiver selon tes besoins...</code> 
• /pm_search - <code>Recherche en MP activer/désactiver selon tes besoins...</code>
• /logs - <code>Obtenir les erreurs récentes.</code>
• /delete - <code>Supprimer un fichier spécifique de la base de données.</code>
• /users - <code>Obtenir la liste de mes utilisateurs et leurs IDs.</code>
• /chats - <code>Obtenir la liste de mes chats et leurs IDs.</code>
• /leave - <code>Quitter un chat.</code>
• /disable - <code>Désactiver un chat.</code>
• /ban - <code>Bannir un utilisateur.</code>
• /unban - <code>Débannir un utilisateur.</code>
• /channel - <code>Obtenir la liste de tous les groupes connectés.</code>
• /broadcast - <code>Diffuser un message à tous les utilisateurs.</code>
• /grp_broadcast - <code>Diffuser un message à tous les groupes connectés.</code>
• /gfilter - <code>Ajouter des filtres globaux.</code>
• /gfilters - <code>Voir la liste de tous les filtres globaux.</code>
• /delg - <code>Supprimer un filtre global spécifique.</code>
• /delallg - <code>Supprimer tous les filtres globaux de la base de données.</code>
• /deletefiles - <code>Supprimer les fichiers CamRip et PreDVD de la base de données.</code>
• /send - <code>Envoyer un message à un utilisateur spécifique.</code>
• /add_premium - <code>Ajouter un utilisateur au premium.</code>
• /remove_premium - <code>Retirer un utilisateur du premium.</code>
• /premium_users - <code>Obtenir la liste des utilisateurs premium.</code>
• /get_premium - <code>Obtenir les infos d'un utilisateur premium.</code>
• /restart - <code>Redémarrer le bot.</code>"""      

    
    GROUP_TXT = """👋 Salut {},

📚 Voici ma liste de commandes pour tous les propriétaires de groupe ⇊
    
•  - Connecter un chat spécifique à tes MPs.
• /disconnect - Déconnecter d'un chat.
• /shortlink - Connecter ton site de liens raccourcis.
• /set_tutorial - Définir ton tutoriel de téléchargement vidéo.
• /remove_tutorial - Supprimer ton tutoriel de téléchargement vidéo.
• /shortlink_info - Voir les infos de ton groupe.
• /setshortlinkon - Activer les liens raccourcis pour ton groupe.
• /setshortlinkoff - Désactiver les liens raccourcis pour ton groupe.
• /connections - Lister toutes tes connexions.
• /settings - Modifier les paramètres comme tu veux.
• /filter - Ajouter un filtre dans un groupe.
• /filters - Lister tous les filtres d'un groupe.
• /del - Supprimer un filtre spécifique dans un groupe.
• /delall - Supprimer tous les filtres d'un groupe.
• /purge - Supprimer tous les messages depuis le message répondu jusqu'au message actuel."""

    DONATION = """<b>👋 Salut {},
    
<b>Merci de soutenir le développeur pour maintenir le service actif et continuer à ajouter de nouvelles fonctionnalités pour vous... Cela nous aidera à garder notre bot sur Heroku et à continuer à uploader des films et séries en permanence dans la meilleure qualité.</b>

<b>Vous pouvez faire un don du montant que vous souhaitez 🌝</b>

<b>🎉 Choisissez votre méthode de don 👇</b>

➢  Par Adresse USDT TRC20: <code>TYUGH5DtPc2gcz1v6hgEU2igdZ8sQ8HE9h</code>


➢  Par Adresse $TON: <code>UQB8a-qTnI_c9oPkWIXNDMNs6Z_C-TDdYFwLKQ_m_b7essq9</code>


➢  Vous pouvez me faire don par mobile Money

‼️ Merci d'envoyer une capture d'écran après votre don.</b>"""
    

    SHORTLINK_INFO = """<b>
 ❗<u>Comment gagner de l'argent avec ce bot</u>❗

★ Vous pouvez commencer à gagner 💸 de l'argent dès aujourd'hui avec notre bot simple et facile à utiliser !

›› Étape 1 : Ajoutez ce bot à votre groupe en tant qu'admin...

›› Étape 2 : Utilisez /je_suis_curieux dans votre groupe pour lier le bot à vos messages privés.

›› Étape 3 : Cliquez sur le bouton suivant pour savoir comment connecter un site de liens raccourcis à ce bot.

★ N'attendez plus pour commencer à gagner de l'argent 💰 avec votre groupe Telegram. Ajoutez notre bot dès aujourd'hui !</b>

<spoiler> Bof. tu fait tout ça mais tu ne peux pas m'ajouter à ton Groupe</spoiler>
"""

    SHORTLINK_INFO2 = """<b>
❗<u>Comment connecter votre raccourcisseur</u>❗

››Dans la vie, tout savoir peut etre un risque.</b>
"""
    SHORTLINK_INFO3 = """<b>
❗<u>Comment connecter votre tutoriel</u>❗

›› La curiosité est un vilain défaut</b>
"""
    
    
    SELECT = """
➢ Cliquez sur le bouton "Qualité" pour obtenir le fichier dans la qualité souhaitée.
➢ Cliquez sur le bouton "Langue" pour obtenir le fichier dans la langue souhaitée.
➢ Cliquez sur le bouton "Saison" pour obtenir le fichier dans la saison souhaitée.

➢ Cliquez sur le bouton "♨️ Envoyer tous les fichiers ♨️" pour obtenir tous les fichiers en un clic.
"""

    REQINFO = """➢ Cliquez sur "Qualité" pour changer la qualité.
➢ Cliquez sur "Langue" pour changer la langue. 
➢ Cliquez sur "Saison" pour changer la saison.
➢ Cliquez sur "♨️ Envoyer tous les fichiers ♨️" pour obtenir tous les fichiers."""

    SINFO = """
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯
Format pour les demandes de séries
⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯⋯

Allez sur Google ➠ Tapez le nom de la série ➠ Copiez le nom correct ➠ Collez dans ce groupe

Exemple : Loki S01E01

🚯 Ne pas utiliser ➠ ':(!,./)"""

    NORSLTS = """ 
#AucunRésultat

ID : <code>{}</code>
Nom : {}

Message : <b>{}</b>"""
    
    CAPTION = """<b>{file_name}\nRej𝗈𝗂𝗇s ➥ 「<a href='t.me/ZeeXClub'>ZeeXClub [ZXC]\nPour tous bos films, series, animes, cartoons.</a>」</b>\n\n<b><blockquote><i>Merci de transférer ces fichiers vers les messages sauvegardés et de fermer ce message</i></blockquote></b>"""

    IMDB_TEMPLATE_TXT = """
<b>‣ Titre : <a href={url}>{title}</a>

‣ 🎭Genres : {genres}
‣ 📅Année : <a href={url}/releaseinfo>{year}</a> 
‣ ⭐Note : <a href={url}/ratings>{rating}</a> / 10 (Basé sur {votes} votes)
‣ 🏳️Langue : <code>Français</code></a>
‣ ⏳Durée : {runtime} Minutes</a>

» 🕦Résultats affichés en : {remaining_seconds} <i>secondes</i>
» 👤Demandé par : {message.from_user.mention}</b>"""
    

    RESTART_TXT = """
<b>Bot redémarré !

• Date : <code>{}</code>
• Heure : <code>{}</code>
• Fuseau horaire : <code>Africa/Lome</code>
• Version : <code>v4.7 [Stable]</code>
</b>"""

    LOGO = """

Le bot fonctionne correctement"""

    #PLANS

    PAGE_TXT = """Pourquoi êtes-vous si curieux ⁉️"""

    PURCHASE_TXT = """Sélectionnez votre méthode de paiement."""

    PREMIUM_TEXT = """<b>👋 Salut {}

<blockquote>🎁 Avantages Premium :</blockquote>

›› Pas besoin d'ouvrir les liens
❏ Fichiers directs   
›› Expérience sans pub
❏ Liens de téléchargement ultra-rapides                         
›› Liens de streaming multi-joueurs                           
❏ Films et séries illimités                                                                        
›› Support admin complet                              
❏ Demandes traitées en 1h [si disponible]

›› Vérifiez votre abonnement : /myplan
</b>"""

    CPREMIUM_TEXT = """<b>👋 Salut {},
    
🎁 <u>Fonctionnalités Premium</u> :

›› Pas besoin de vérification
›› Fichiers directs  
›› Liens de téléchargement ultra-rapides  
›› Liens de streaming multi-joueurs      
›› Expérience sans pub                           
›› Films & séries illimités


🌹 Utilisez /plan pour voir tous nos abonnements.
➛ Vérifiez votre abonnement avec : /myplan

‼️ Après avoir envoyé une capture, merci de nous laisser un peu de temps pour vous ajouter.</b>"""

    PLAN_TXT = """<b>👋 Salut {},
    
🎁 <u>Fonctionnalités Premium</u> :

○ Pas besoin d'ouvrir les liens
○ Fichiers directs   
○ Expérience sans pub 
○ Liens de téléchargement ultra-rapides                         
○ Streaming multi-joueurs                           
○ Films & séries illimités                                                                        
○ Support admin complet                              
○ Demandes traitées en 1h [si disponible]

➛ Utilisez /plan pour voir tous nos abonnements.
➛ Vérifiez votre abonnement avec : /myplan

‼️ Après envoi d'une capture, merci de patienter.</b>"""

    FREE_TXT = """<b>👋 Salut {},
    
🎉 <u>Essai gratuit</u> 🎉
❗ Seulement 5 minutes
 
○ Pas besoin d'ouvrir les liens
○ Streaming multi-joueurs
○ Expérience sans pub

👨‍💻 Contactez le <a href='https://t.me/JobeBot'>propriétaire</a> pour votre essai.

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    BRONZE_TXT = """<b>👋 Salut {},
    
🥉 <u>Offre Bronze</u>
⏰ 7 jours (1 Semaine)
💸 Prix : 500F CFA

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    SILVER_TXT = """<b>👋 Salut {},
    
🥈 <u>Offre Argent</u>
⏰ 15 jours 
💸 Prix : 1000F CFA

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    GOLD_TXT = """<b>👋 Salut {},
    
🥇 <u>Offre Or</u>
⏰ 30 jours  (1 Mois)
💸 Prix : 1700F

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    PLATINUM_TXT = """<b>👋 Salut {},
    
🏅 <u>Offre Platine</u>
⏰ 45 jours 
💸 Prix : 2500F

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""
    
    DIAMOND_TXT = """<b>👋 Salut {},

💎 <u>Offre Diamant</u>
⏰ 60 jours  (2 Mois)
💸 Prix : 3000F

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    OTHER_TXT = """<b>👋 Salut {},
    
🎁 <u>Autre offre</u>
⏰ Durée personnalisée
💸 Tarif selon la durée choisie

🏆 Si vous voulez une offre différente de celles proposées, vous pouvez contacter directement notre <a href='https://t.me/Jobe_TECH_Bot'>propriétaire</a> en cliquant sur le bouton ci-dessous.
    
👨‍💻 Contactez le propriétaire pour une offre personnalisée.

➛ Utilisez /plan pour voir nos offres.
➛ Vérifiez votre abonnement avec : /myplan</b>"""

    UPI_TXT = """<b>👋 Salut {},
    
 Payez le montant correspondant à votre abonnement et profitez des avantages Premium !

💵 Wallet - <code>UQB8a-qTnI_c9oPkWIXNDMNs6Z_C-TDdYFwLKQ_m_b7essq9</code>

‼️ Merci d'envoyer une capture après paiement.</b>"""

    QR_TXT = """<b>👋 Salut {},
    
 Payez le montant correspondant à votre abonnement et profitez des avantages Premium !

📸 QR Code - <a href='t.me/Kingcey'>Cliquez ici pour scanner</a>

‼️ Merci d'envoyer une capture après paiement.</b>"""

    PREPLANS_TXT = """<b>👋 Salut {},

<blockquote>🎁 Avantages Premium :</blockquote>

›› Pas besoin d'ouvrir les liens
❏ Fichiers directs   
›› Expérience sans pub 
❏ Liens de téléchargement ultra-rapides                         
›› Streaming multi-joueurs                           
❏ Films et séries illimités                                                                        
›› Support admin complet                              
❏ Demandes traitées en 1h [si disponible]

›› Vérifiez votre abonnement : /myplan
</b>"""      

    SOURCE_TXT ="""<b>Code source : </b>

 Code source disponible ici ◉› :<a href=https://t.me/JobeTECH>Ne Clique Pas</a> """

    EXTRAF_TXT =""" <b> Voici mes fonctionnalités supplémentaires </b>"""

    STICKER_TXT = """<b>Vous pouvez utiliser ce module pour trouver l'ID d'un sticker.
 • Utilisation :
   
  Comment l'utiliser 
 ◉ Répondez à un sticker avec [/stickerid]  
 </b>""" 
  
    FONT_TXT= """<b>Utilisation 
  
 Vous pouvez utiliser ce module pour changer le style de police   
  
 Commande : /font votre texte (optionnel) 
 Exemple :- /font Bonjour 
  
 </b>"""

    TELE_TXT = """<b>Aide : Module Telegraph 
  
 Utilisation : /telegraph - Envoyez-moi une image ou vidéo (moins de 5MB) 
  
 Note : 
 Cette commande est disponible en groupe et en MP 
 Tout le monde peut l'utiliser</b>"""

    GITHUB_TXT = """<b>🔹 Commandes GitHub 🔹</b>

📌 <b>Utilisez ces commandes pour obtenir des infos sur les profils GitHub et rechercher des dépôts :</b>

🔹 <b>Utilisation :</b>  
✅ <code>/github {nom_utilisateur}</code> - <b>Récupère les infos du profil GitHub</b>  
✅ <code>/repo {nom_dépôt}</code> - <b>Recherche des dépôts sur GitHub</b>"""


    SONG_TXT = """<b>Module de téléchargement de musique</b> 
      
 <b>Téléchargez n'importe quelle musique à vitesse rapide. Fonctionne en groupe et en MP...</b> 
  
  /song nom de la chanson</b>"""

    INSTAGRAM_TXT = """<b>Avec cette commande, vous pouvez facilement télécharger des Reels Instagram.

/Instagram envoyez un lien de Reel, Story ou Post public pour le télécharger.

Exemple 👉 /Instagram https://www.instagram.com/reel/CvTNkc1ouD3/?igsh=YzljYTk1ODg3Zg==<b>"""
    
    JSON_TXT = """<b> 
 JSON :  
 Le bot retourne du JSON pour tous les messages avec /json 
  
 Fonctionnalités : 
  
 Édition de message en JSON 
 Support en PV 
 Support en groupe 
  
 Note : 
  
 Tout le monde peut utiliser cette commande, en cas de spam vous serez banni automatiquement.</b>"""

    EXTRA_TXT =""" <b> Mes fonctionnalités supplémentaires 

›› /stickerid : obtenir l'ID d'un sticker
❏ /json : retourne du JSON pour les messages
›› /telegraph : envoyez une image/vidéo (<5MB)
❏ /song : télécharger une musique                  
›› /Instagram télécharger des Reels/Stories (public uniquement)                         
</b>"""

    CHATGPT = """
» Commandes disponibles pour l'IA :

L'IA peut répondre à vos questions et afficher les résultats

 ❍ /chatgpt : répondez à un message ou envoyez du texte
 ❍ /lucy : répondez à un message ou envoyez du texte
 ❍ /ask : IA Google 
 ❍ /gpt : chatgpt
 ❍ /chat : répondez à un message ou envoyez du texte
"""

    TORRENT = """
Commande de recherche Torrent

Exemple : /torrent Spider Man
"""

    MONGO_TXT = """
Commande de vérification MongoDB

Entrez votre URL MongoDB après la commande.

Exemple : /mongo votre_url_mongodb
"""

    FONT_TXT = """Aide : <b>Police</b>

<b>Note</b>: Vous pouvez utiliser ce module pour changer le style de police, envoyez simplement :

<code>/font Kingcey est le meilleure</code>"""

    IMAGE_TXT = """
» Commandes disponibles pour la recherche d'images :

❍ /image : rechercher une image correspondant au texte
Exemple :

/image Subaru
"""

    ANIME_TXT = """
<b>Obtenez des informations sur des animes !

UTILISATION :
➢ /anime [nom] - Obtenir les infos sur l'anime</b>"""

    STREAM = """
Avec cette commande, vous pouvez streamer n'importe quel fichier sans le télécharger.

Envoyez d'abord /stream puis un fichier, le bot vous donnera un lien de stream et de téléchargement
"""

    APPROVE_TXT = """
Ajoutez-moi simplement à votre chaîne ou groupe et voyez la magie opérer
"""

    AI_TXT = """
Voici quelques commandes IA/expert

➻ Lucy - accédez à Jarvis
➻ Assis - l'IA répondra en audio
➻ /gpt - fonctionnalité GPT
➻ /chatgpt - fonctionnalité GPT
➻ /bard - fonction Bard
➻ /llama - mode Llama
➻ /gemini - fonction Gemini
➻ /geminivision - mode Gemini
➻ /mistral - code Mistral
➻ /tts - conversion texte vers parole
➻ /upscale - API gratuite d'amélioration d'image
➻ /blackbox : texte avec réponse à une photo ou juste texte
"""
    
