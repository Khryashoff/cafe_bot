import os
import asyncio
import logging


from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from handlers.user_interaction import user_router
from common.bot_command_list import user_chat


load_dotenv()
token = os.getenv('TOKEN_BOT')


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

ALLOWED_UPDATES = ['message, edited_message']

bot = Bot(token=token)
dp = Dispatcher()

dp.include_router(user_router)


async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands(
        commands=user_chat,
        scope=types.BotCommandScopeAllPrivateChats()
    )
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)


asyncio.run(main())
