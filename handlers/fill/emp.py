from . import *

@dp.callback_query_handler(text='e:fill')
async def fill(cb: CallbackQuery):
    await cb.answer()
    if db.exist(cb.from_user.username):
        info=""
        data = db.get_emptycols(cb.from_user.username)
        if len(data) == 0:
            await cb.message.edit_text("🎉Вітаю, Ви надали всю інформацію\nМожете перейти до пошуку вакансій📝",
                reply_markup = kb_e.fill)
        else:
            for col in data:
                info += f"✎ {db.TRANSLATE[col]['e']};\n"
            info = info[:-1]
            await cb.message.edit_text(
            "В системі немає повної інформації.\n"\
            "Будь ласка, надайте інформацію щодо:\n"\
            f"{info}", reply_markup = kb_e.fill)
    else:
        db.push('e', cb.from_user.username)
        await cb.message.edit_text(
        "Ви увійшли як робітник\n"\
        "Надайте інформацію про себе:", reply_markup = kb_e.fill)
    return

@dp.callback_query_handler(text_contains='e:act')
async def act(cb: CallbackQuery):
    username = cb.from_user.username
    data = cb.data.split(':')
    await cb.answer()
    if data[-1] == 'act':
        info =  db.get(username, db.COLS[3])
        if info:
            info = "Поточний опис Ваших навичок:\n"\
                f"{info}\n"\
                "Щоб змінити його, надішліть новий\n"
        else:
            info = ''
        await cb.message.edit_text(info+
            "Опишіть свої навички, бажано вказати:\n"\
            "• Вміння та навички\n"\
            "• На який режим роботи розраховуєте\n"\
            "• Які завдання для Вас найцікавіші\n", reply_markup=kb_e.act)
        description_add(username, 'e', 'a', cb.message)
    elif data[-1] == 'e':
        await cb.message.edit_text("Це може зайняти декілька хвилин...",
            reply_markup=kb.new(kb.back("e:act:q")))
        res = ""
        i = 0
        async for letter in ai.eact_example():
            i+=1
            if not letter:
                res = "Виникла помилка, згенерувати текст не вдалося"
                break
            if username not in description:
                await fill(cb)
                return
            res += letter
            time.sleep(0.1)
            if i%10 == 0:
                t = int(round((700-len(res))*0.1, 0))
                t = 7 if t < 0 else t
                await cb.message.edit_text(res.ljust(20, " ")+
                    f'\nЗалишилося близько {t} секунд', parse_mode=ParseMode.HTML,
                   reply_markup=kb.new(kb.back("e:act:q")))
        await cb.message.edit_text(res + '\n✎Починайте описувати свої навички✎\nАбо\n↩Поверніться назад↩',
                reply_markup=kb.new(kb.back("e:act:q")))
    elif data[-1] == 'q':
        description_remove(username)
        await fill(cb)
    return

@dp.callback_query_handler(text_contains="e:place")
async def place(cb: CallbackQuery):
    data = cb.data.split(':')
    uname = cb.from_user.username
    if data[-1] == "place":
        await cb.answer()
        cur = db.get(uname, db.COLS[6])
        if cur:
            await cb.message.edit_text(f"Поточне місце:\n{cur}\nМожливі варіанти:")
        else:
            await cb.message.edit_text("Ваше побажання щодо місця роботи:")
        await cb.message.edit_reply_markup(kb_e.place)
        return
    elif data[-1] == "of":
        description_add(uname, 'e', 'p', cb.message)
        await cb.message.edit_text(
            "✏Введіть адресу: місто, район, вулиця, номер.\n"\
            "Або\n"\
            "↩Поверніться назад↩"\
        )
        await cb.message.edit_reply_markup(kb.new(kb.back("e:place:q")))
        return
    elif data[-1] == "on":
        db.push('e', uname, place="Онлайн")
    elif data[-1] == "q":
        description_remove(uname)
    await cb.answer("Інформацію записано", show_alert=False)
    await fill(cb)
    return