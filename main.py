# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from dotenv import load_dotenv
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


load_dotenv()
API = "https://www.google.com/search?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


START_TEXT = """π§πΎπππ {}, π¨ πΊπ πΊ π¦πππππΎ π²πΎπΊππΌπ π‘ππ. π©πππ π²πΎππ½ π¬πΎ π  π³πΎππ π³π π²πΎπΊππΌπ, π¨ π’πΊπ π₯πππ½ ππ πΏπππ π¦πππππΎ.

πΈππ π’πΊπ π΄ππΎ π¬πΎ π¨π π¨πππππΎ π³ππ...."""

JOIN_BUTTON = [
    InlineKeyboardButton(
        text='sα΄α΄α΄α΄Κα΄ Ι’Κα΄α΄α΄',
        url='https://telegram.me/dkbotxchats'
    )
]


@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    await update.reply_text(
        text=START_TEXT.format(update.from_user.mention),
        reply_markup=InlineKeyboardMarkup([JOIN_BUTTON]),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_message(filters.private & filters.text)
async def filter(bot, update):
    await update.reply_text(
        text="π’πππΌπ π³ππΎ π‘πππππ π‘πΎπππ π₯ππ π²πΎπΊππΌππππ....",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Sα΄α΄Κα΄Κ Hα΄Κα΄", switch_inline_query_current_chat=update.text)],
                [InlineKeyboardButton(text="Sα΄α΄Κα΄Κ IΙ΄ CΚα΄α΄", switch_inline_query=update.text)]
            ]
        ),
        disable_web_page_preview=True,
        quote=True
    )


@Bot.on_inline_query()
async def inline(bot, update):
    results = google(update.query)
    answers = []
    for result in results:
        answers.append(
            InlineQueryResultArticle(
                title=result["title"],
                description=result["description"],
                input_message_content=InputTextMessageContent(
                    message_text=result["text"],
                    disable_web_page_preview=True
                ),
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(text="Link", url=result["link"])],
                        JOIN_BUTTON
                    ]
                )
            )
        )
    await update.answer(answers)


def google(query):
    r = requests.get('https://www.google.com/search?query=')
    informations = r.json()["results"][:50]
    results = []
    for info in informations:
        text = f"**π³ππππΎ:** `{info['title']}`"
        text += f"\n**π£πΎππΌπππππππ:** `{info['description']}`"
        text += f"\n\nπ₯πππ πππΎ π’ππΎπΊππππ ππΏ #ππππππα΅α΅α΅"
        results.append(
            {
                "title": info['title'],
                "description": info['description'],
                "text": text,
                "link": info['link']
            }
        )
    return results


Bot.run()
