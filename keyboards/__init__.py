from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ACTIVITY_TYPES = (
    "Аграрна професія",
    "Бізнес та управління",
    "Комп'ютерні технології",
    "Культура та мистецтво",
    "Освіта",
    "Медицина та охорона здоров'я",
    "Право і кримінальна юстиція",
    )

def back(data):
    return InlineKeyboardButton("Повернутися назад↩", callback_data=data)

def new(*args):
    kb = InlineKeyboardMarkup(row_width=1)
    for arg in args:
        kb.add(arg)
    return kb

def new_tact(kind: str):
    kb = InlineKeyboardMarkup()
    for i, arg in enumerate(ACTIVITY_TYPES):
        kb.add(InlineKeyboardButton(arg, callback_data=f"{kind}:tact:{i}"))
    kb.add(back(f"{kind}:fill"))
    return kb

