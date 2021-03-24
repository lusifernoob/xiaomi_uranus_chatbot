#!/usr/bin/env python3.7
""" Xiaomi Geeks Telegram Bot"""
import asyncio
import pickle

from os import path, remove

from telethon.sync import TelegramClient

from uranus_bot import API_KEY, API_HASH, BOT_TOKEN, WITH_EXTRA
from uranus_bot.i18n.localize import Localize
from uranus_bot.providers.provider import Provider
from uranus_bot.telegram_bot import TG_LOGGER
from uranus_bot.telegram_bot.modules import ALL_MODULES
from uranus_bot.utils.loader import load_modules

BOT = TelegramClient('xfu_bot', API_KEY, API_HASH).start(bot_token=BOT_TOKEN)
BOT.parse_mode = 'markdown'
BOT_INFO = {}
PROVIDER = Provider(BOT.loop)
LOCALIZE = Localize()


def main():
    """Main"""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())


async def run():
    """Run the bot."""
    bot_info = await BOT.get_me()
    BOT_INFO.update({'name': bot_info.first_name,
                     'username': bot_info.username, 'id': bot_info.id})
    TG_LOGGER.info("Bot started as %s! Username is %s and ID is %s",
                   BOT_INFO['name'], BOT_INFO['username'], BOT_INFO['id'])
    load_modules(ALL_MODULES, __package__)
    if WITH_EXTRA:
        from uranus_bot.telegram_bot.bot_private.private import load_private_modules
        await load_private_modules()
    # Check if the bot is restarting
    if path.exists('restart.pickle'):
        with open('restart.pickle', 'rb') as status:
            restart_message = pickle.load(status)
        await BOT.edit_message(restart_message['chat'], restart_message['message'], 'Restarted Successfully!')
        remove('restart.pickle')
    async with BOT:
        await BOT.run_until_disconnected()
