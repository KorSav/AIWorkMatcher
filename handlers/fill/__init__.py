from .. import *
import keyboards.rec as kb_r
import keyboards.emp as kb_e
import ai
import time
from aiogram.types import ParseMode

description = {}
'''
{
"tlink":{
    "kind": "r or e",
    "state": "state",
    "message": "message object"
    }
}
'''

def description_add(uname: str, kind: str, state: str, message: Message):
    global description
    description[uname] = {"kind": kind, "state": state, "message": message}
    return

def description_remove(uname: str):
    if uname in description:
        del description[uname]

async def anymes_sample(msg: Message, kind: str):
    uname = msg.from_user.username
    if uname in description and description[uname]["kind"] == kind:
        if description[uname]["state"] == 'a':
            btn_back = kb.back(kind+":act:q")
            db.push(kind, uname, act=msg.text)
            await description[uname]["message"].edit_text(
                "Інформацію записано, поточний опис:\n"\
                f"{db.get(uname, db.COLS[3])}\n\n"\
                "✏Для редагування надішліть новий опис✏\n"\
                "✅Якщо все правильно натискайте кнопку✅",
                reply_markup=kb.new(btn_back))
        elif description[uname]["state"] == 'p':
            btn_back = kb.back(kind+":place:q")
            db.push(kind, uname, place=msg.text)
            await description[uname]["message"].edit_text(
                "Інформацію записано, поточне місце:\n"\
                f"{db.get(uname, db.COLS[6])}\n\n"\
                "✏Для редагування надішліть нову адресу✏\n"\
                "✅Якщо все правильно натискайте кнопку✅",
                reply_markup = kb.new(btn_back))
        await msg.delete()
    else:
        await msg.answer(text='Для початку введіть /start')
    return

