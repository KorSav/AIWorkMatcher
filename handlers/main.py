from . import *
from handlers.fill import common, emp, rec
from handlers.look import look
from handlers.find import find

@dp.callback_query_handler(text=["e","r"])
async def start(cb: CallbackQuery):
    await cb.answer()
    rm = kb.emp.start if cb.data == 'e' else kb.rec.start
    await cb.message.edit_text("Оберіть дію для роботи з системою", reply_markup=rm)
    return

