from . import *

start = new(
    InlineKeyboardButton("Заповнити інформацію про вакансію", callback_data="r:fill"), 
    InlineKeyboardButton("Переглянути створену вакансію", callback_data="r:look"), 
    InlineKeyboardButton("Знайти робітника", callback_data="r:find"), 
)

look = new(
    InlineKeyboardButton("Перейти до заповнення", callback_data="r:fill"),
    back("r")
    )

find = new(
    InlineKeyboardButton("Всі робітники", callback_data="r:find:a"),
    InlineKeyboardButton("Найкращий робітник", callback_data="r:find:b"),
    back("r"),
    )

fill = new(
    InlineKeyboardButton("Вид діяльності", callback_data="r:tact"),
    InlineKeyboardButton("Короткий опис вакансії", callback_data="r:act"),
    InlineKeyboardButton("Чи необхіден досвід робітнику", callback_data="r:xp"),
    InlineKeyboardButton("Чи необхідна освіта робітнику", callback_data="r:edu"),
    InlineKeyboardButton("Місце роботи", callback_data="r:place"),
    back("r"),
)

act = new(
    InlineKeyboardButton("Приклад опису", callback_data="r:act:e"),
    back("r:act:q")
)

xp = new(
    InlineKeyboardButton("Так, досвід обов'язковий", callback_data="r:xp:t"), 
    InlineKeyboardButton("Ні, можна працювати без досвіду", callback_data="r:xp:f"),
    back("r:fill"),
)

edu = new(
    InlineKeyboardButton("Вища освіта", callback_data="r:edu:high"),
    InlineKeyboardButton("Допускається середня освіта", callback_data="r:edu:mid"),
    InlineKeyboardButton("Освіта не потрібна", callback_data="r:edu:zero"),
    back("r:fill"),
    )

place = new(
    InlineKeyboardButton("Вказати місце", callback_data="r:place:of"),
    InlineKeyboardButton("Можна працювати онлайн", callback_data="r:place:on"),
    back("r:place:q"),
    )
