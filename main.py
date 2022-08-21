# Author: Fayas (https://github.com/FayasNoushad) (@FayasNoushad)

import os
import requests
from dotenv import load_dotenv
from requests.utils import requote_uri
from pyrogram import Client, filters
from pyrogram.types import *


load_dotenv()
API = "AIzaSyCcaUa5Z3moaVbPtm9aPNGwQ24ptjytxF0?query="


Bot = Client(
    "Google-Search-Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)


START_TEXT = """𝖧𝖾𝗅𝗅𝗈 {}, 𝖨 𝖺𝗆 𝖺 𝖦𝗈𝗈𝗀𝗅𝖾 𝖲𝖾𝖺𝗋𝖼𝗁 𝖡𝗈𝗍. 𝖩𝗎𝗌𝗍 𝖲𝖾𝗇𝖽 𝖬𝖾 𝖠 𝖳𝖾𝗑𝗍 𝖳𝗈 𝖲𝖾𝖺𝗋𝖼𝗁, 𝖨 𝖢𝖺𝗇 𝖥𝗂𝗇𝖽 𝗂𝗍 𝖿𝗋𝗈𝗆 𝖦𝗈𝗈𝗀𝗅𝖾.

𝖸𝗈𝗎 𝖢𝖺𝗇 𝖴𝗌𝖾 𝖬𝖾 𝖨𝗇 𝖨𝗇𝗅𝗂𝗇𝖾 𝖳𝗈𝗈...."""

JOIN_BUTTON = [
    InlineKeyboardButton(
        text='sᴜᴘᴘᴏʀᴛ ɢʀᴏᴜᴘ',
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
        text="𝖢𝗅𝗂𝖼𝗄 𝖳𝗁𝖾 𝖡𝗎𝗍𝗍𝗈𝗇 𝖡𝖾𝗅𝗈𝗐 𝖥𝗈𝗋 𝖲𝖾𝖺𝗋𝖼𝗁𝗂𝗇𝗀....",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton(text="Sᴇᴀʀᴄʜ Hᴇʀᴇ", switch_inline_query_current_chat=update.text)],
                [InlineKeyboardButton(text="Sᴇᴀʀᴄʜ Iɴ Cʜᴀᴛ", switch_inline_query=update.text)]
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
    r = requests.get(API + requote_uri(query))
    informations = r.json()["results"][:50]
    results = []
    for info in informations:
        text = f"**𝖳𝗂𝗍𝗅𝖾:** `{info['title']}`"
        text += f"\n**𝖣𝖾𝗌𝖼𝗋𝗂𝗉𝗍𝗂𝗈𝗇:** `{info['description']}`"
        text += f"\n\n𝖥𝗋𝗈𝗆 𝗍𝗁𝖾 𝖢𝗋𝖾𝖺𝗍𝗈𝗋𝗌 𝗈𝖿 #𝙏𝙊𝙑𝙄𝙉𝙊ᵇᵒᵗ"
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
