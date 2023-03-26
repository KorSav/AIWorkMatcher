from . import *

@dp.callback_query_handler(text='r:fill')
async def fill(cb: CallbackQuery):
    await cb.answer()
    if db.exist(cb.from_user.username):
        info=""
        data = db.get_emptycols(cb.from_user.username)
        if len(data) == 0:
            await cb.message.edit_text("🎉Вітаю, ваша вакасія повністю описана📝")
        else:
            for col in data:
                info += f"✎ {db.TRANSLATE[col]['r']};\n"
            info = info[:-1]
            await cb.message.edit_text(
            "В системі немає повної інформації.\n"\
            "Будь ласка, надайте інформацію щодо:\n"\
            f"{info}")
    else:
        db.push('r', cb.from_user.username)
        await cb.message.edit_text(
        "Ви увійшли як роботодавець\n"\
        "Надайте інформацію про вакансію:")
    await cb.message.edit_reply_markup(kb_r.fill)
    return


@dp.callback_query_handler(text_contains='r:act')
async def act(cb: CallbackQuery):
    username = cb.from_user.username
    await cb.answer()
    if cb.data == 'r:act':
        data =  db.get(username, db.COLS[3])
        if data:
            await cb.message.edit_text(
                "Поточний опис вакансії:\n"\
                f"{data}\n"\
                "Щоб змінити його, надішліть новий\n"\
                "Опишіть вакансію, бажано вказати наступні деталі:\n"\
                "• Опис обов'язків\n"\
                "• Які навички необхідні робітнику\n"\
                "• Режим роботи\n"\
                "• Коротка інформація щодо процесу найму\n"\
                )
        else:
            await cb.message.edit_text(
                "Опишіть вакансію, бажано вказати наступні деталі:\n"\
                "• Опис обов'язків\n"\
                "• Які навички необхідні робітнику\n"\
                "• Режим роботи\n"\
                "• Коротка інформація щодо процесу найму\n"\
                )
        await cb.message.edit_reply_markup(kb_r.act)
        description_add(username, 'r', 'a', cb.message)
    elif cb.data[-1] == 'e':
        await cb.message.edit_text("Це може зайняти декілька хвилин...")
        await cb.message.edit_reply_markup(kb.new(kb.back("r:act:q")))
        res = ""
        c=0
        async for letter in ai.ract_example():
            c+=1
            if not letter:
                res = "Виникла помилка, згенерувати текст не вдалося"
                break
            if username not in description:
                await fill(cb)
                return
            res += letter
            time.sleep(0.1)
            if c == 10:
                t = round((700-len(res))*0.1, 0)
                t = 7 if t < 0 else t
                await cb.message.edit_text(res.ljust(20, " ")+
                    f'\nЗалишилося близько {t} секунд', parse_mode=ParseMode.HTML,
                   reply_markup=kb.new(kb.back("r:act:q")))
                c=0
        await cb.message.edit_text(res + '\n✎Починайте описувати вакансію✎\nАбо\n↩Поверніться назад↩',
                reply_markup=kb.new(kb.back("r:act:q")))
    elif cb.data[-1] == 'q':
        description_remove(username)
        await fill(cb)
    return

@dp.callback_query_handler(text_contains="r:place")
async def place(cb: CallbackQuery):
    data = cb.data.split(':')
    uname = cb.from_user.username
    if data[-1] == "place":
        await cb.answer()
        cur = db.get(uname, db.COLS[6])
        if cur:
            await cb.message.edit_text(f"Поточне місце:\n{cur}\nМожливі варіанти:")
        else:
            await cb.message.edit_text("Надайте інформацію щодо місця роботи:")
        await cb.message.edit_reply_markup(kb_r.place)
        return
    elif data[-1] == "of":
        description_add(uname, 'r', 'p', cb.message)
        await cb.message.edit_text(
            "✏Введіть адресу: місто, район, вулиця, номер.\n"\
            "Або\n"\
            "↩Поверніться назад↩"\
        )
        await cb.message.edit_reply_markup(kb.new(kb.back("r:place:q")))
        return
    elif data[-1] == "on":
        db.push('r', uname, place="Онлайн")
    elif data[-1] == "q":
        description_remove(uname)
    await cb.answer("Інформацію записано", show_alert=False)
    await fill(cb)
    return