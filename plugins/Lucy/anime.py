import json
from calendar import month_name

import aiohttp
from pyrogram import filters, Client
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from plugins.Extra.human_read import get_readable_time

anime_query = """
query ($id: Int, $idMal: Int, $search: String) {
  Media(id: $id, idMal: $idMal, type: ANIME, search: $search) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    type
    format
    status(version: 2)
    description(asHtml: true)
    startDate {
      year
      month
      day
    }
    endDate {
      year
      month
      day
    }
    season
    seasonYear
    episodes
    duration
    chapters
    volumes
    countryOfOrigin
    source
    hashtag
    trailer {
      id
      site
      thumbnail
    }
    updatedAt
    coverImage {
      large
    }
    bannerImage
    genres
    synonyms
    averageScore
    meanScore
    popularity
    trending
    favourites
    tags {
      name
      description
      rank
    }
    relations {
      edges {
        node {
          id
          title {
            romaji
            english
            native
          }
          format
          status
          source
          averageScore
          siteUrl
        }
        relationType
      }
    }
    characters {
      edges {
        role
        node {
          name {
            full
            native
          }
          siteUrl
        }
      }
    }
    studios {
      nodes {
         name
         siteUrl
      }
    }
    isAdult
    nextAiringEpisode {
      airingAt
      timeUntilAiring
      episode
    }
    airingSchedule {
      edges {
        node {
          airingAt
          timeUntilAiring
          episode
        }
      }
    }
    externalLinks {
      url
      site
    }
    rankings {
      rank
      year
      context
    }
    reviews {
      nodes {
        summary
        rating
        score
        siteUrl
        user {
          name
        }
      }
    }
    siteUrl
  }
}
"""


async def get_anime(title):
    async with aiohttp.ClientSession() as sesi:
        r = await sesi.post(
            "https://graphql.anilist.co",
            json={"query": anime_query, "variables": title},
        )
        return await r.json()


def shorten(description, info="anilist.co"):
    ms_g = ""
    if len(description) > 700:
        description = f"{description[:500]}...."
        ms_g += f'\n<strong>Description :</strong> <em>{description}</em><a href="{info}">Plus d\'infos</a>'
    else:
        ms_g += f"\n<strong>Description :</strong> <em>{description}</em>"
    return (
        ms_g.replace("<br>", "")
        .replace("</br>", "")
        .replace("<i>", "")
        .replace("</i>", "")
    )


@Client.on_message(filters.command("anime", '/'))
async def anime_search(_, mesg):
    search = mesg.text.split(None, 1)
    reply = await mesg.reply("⏳ <i>Veuillez patienter...</i>", quote=True)
    if len(search) == 1:
        return await reply.edit("⚠️ <b>Veuillez indiquer un nom d'anime.</b>")
    else:
        search = search[1]
    variables = {"search": search}
    try:
        res = (await get_anime(variables))["data"].get("Media", None)
        if not res:
            return await reply.edit("💢 Aucun anime trouvé ! [404]")
    except Exception as e:
        return await reply.edit(f"❌ Erreur API : {str(e)}")

    durasi = (
        get_readable_time(int(res.get("duration") * 60))
        if res.get("duration") is not None
        else "0"
    )
    msg = f"<b>{res['title']['romaji']}</b> (<code>{res['title']['native']}</code>)\n<b>Type</b>: {res['format']}\n<b>Statut</b>: {res['status']}\n<b>Épisodes</b>: {res.get('episodes', 'N/A')}\n<b>Durée</b>: {durasi} par épisode.\n<b>Score</b>: {res['averageScore']}%\n<b>Catégorie</b>: <code>"
    for x in res["genres"]:
        msg += f"{x}, "
    msg = msg[:-2] + "</code>\n"
    
    try:
        sd = res["startDate"]
        startdate = str(f"{month_name[sd['month']]} {sd['day']}, {sd['year']}")
    except:
        startdate = "-"
    msg += f"<b>Date de début</b>: <code>{startdate}</code>\n"
    
    try:
        ed = res["endDate"]
        enddate = str(f"{month_name[ed['month']]} {ed['day']}, {ed['year']}")
    except:
        enddate = "-"
    msg += f"<b>Date de fin</b>: <code>{enddate}</code>\n"
    
    msg += "<b>Studios</b>: <code>"
    for x in res["studios"]["nodes"]:
        msg += f"{x['name']}, "
    msg = msg[:-2] + "</code>\n"
    
    info = res.get("siteUrl")
    trailer = res.get("trailer", None)
    if trailer:
        trailer_id = trailer.get("id", None)
        site = trailer.get("site", None)
        if site == "youtube":
            trailer = f"https://youtu.be/{trailer_id}"
    
    description = (
        res.get("description", "N/A")
        .replace("<i>", "")
        .replace("</i>", "")
        .replace("<br>", "")
    )
    msg += shorten(description, info)
    image = info.replace("anilist.co/anime/", "img.anili.st/media/") if info else None
    
    btn = (
        [
            [
                InlineKeyboardButton("Plus d'infos", url=info),
                InlineKeyboardButton("Bande-annonce 🎬", url=trailer),
            ]
        ]
        if trailer
        else [[InlineKeyboardButton("Plus d'infos", url=info)]]
    )

    if image:
        try:
            await mesg.reply_photo(
                image, 
                caption=msg, 
                reply_markup=InlineKeyboardMarkup(btn)
            )
        except Exception as e:
            print(f"Erreur d'envoi photo: {e}")
            msg += f" [〽️]({image})"
            await reply.edit(msg, reply_markup=InlineKeyboardMarkup(btn) if btn else await reply.edit(msg)
    else:
        await reply.edit(msg, reply_markup=InlineKeyboardMarkup(btn)) if btn else await reply.edit(msg)
    
    await reply.delete()
