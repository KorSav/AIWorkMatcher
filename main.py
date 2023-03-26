import asyncio
import logging
from keyboards import *
from handlers.main import *

kb_Person = InlineKeyboardMarkup()
btn1 = InlineKeyboardButton("Роботодавець", callback_data='r')
btn2 = InlineKeyboardButton("Робітник", callback_data='e')
kb_Person.add(btn1, btn2)

@dp.message_handler(commands="help")
async def mes_cmd_help(msg: Message):
    await msg.answer("Для того, щоб почати роботу з ботом введіть /start")

@dp.message_handler(commands="start")
async def mes_cmd_start(msg: Message):
    await msg.answer("Оберіть, будь ласка, хто Ви:", reply_markup=kb_Person)
    await msg.delete()

async def main():
    await dp.start_polling()

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
