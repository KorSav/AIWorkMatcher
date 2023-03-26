from . import *

start = new(
    InlineKeyboardButton("Надати інформацію про себе", callback_data="e:fill"), 
    InlineKeyboardButton("Переглянути мої дані", callback_data="e:look"), 
    InlineKeyboardButton("Пошук роботи", callback_data="e:find"), 
    )

look = new(
    InlineKeyboardButton("Перейти до заповнення", callback_data="e:fill"),
    back("e")
    )

find = new(
    InlineKeyboardButton("Всі вакансії", callback_data="e:find:a"),
    InlineKeyboardButton("Найкраща вакансія", callback_data="e:find:b"),
    back("e"),
    )

fill = new(
    InlineKeyboardButton("Вид діяльності", callback_data="e:tact"),
    InlineKeyboardButton("Опис навичок", callback_data="e:act"),
    InlineKeyboardButton("Досвід", callback_data="e:xp"),
    InlineKeyboardButton("Освіта", callback_data="e:edu"),
    InlineKeyboardButton("Місце роботи", callback_data="e:place"),
    back("e"),
    )

act = new(
    InlineKeyboardButton("Приклад опису", callback_data="e:act:e"),
    back("e:act:q")
    )

xp = new(
    InlineKeyboardButton("Так, маю досвід", callback_data="e:xp:t"), 
    InlineKeyboardButton("Ні, досвіду немає", callback_data="e:xp:f"),
    back("e:fill"),
)

edu = new(
    InlineKeyboardButton("Маю вищу освіту", callback_data="e:edu:high"),
    InlineKeyboardButton("Маю середню освіту", callback_data="e:edu:mid"),
    InlineKeyboardButton("Освіти немає", callback_data="e:edu:zero"),
    back("e:fill"),
    )

place = new(
    InlineKeyboardButton("Онлайн", callback_data="e:place:on"),
    InlineKeyboardButton("Офлайн", callback_data="e:place:of"),
    back("e:place:q"),
    )

