from . import *
import handlers.fill.rec as hndl_r
import handlers.fill.emp as hndl_e

@dp.message_handler(lambda message: not message.is_command())
async def anymes(msg: Message):
    uname = msg.from_user.username
    kind = db.get(uname, db.COLS[0])
    if kind:
        await anymes_sample(msg, kind)
    else:
        await msg.answer(text='Для початку введіть /start')
    return

@dp.callback_query_handler(text_contains="tact")
async def tact(cb: CallbackQuery):
    data = cb.data.split(':')
    if data[-1] == 'tact':
        await cb.answer()
        cur = db.get(cb.from_user.username, db.COLS[2])
        if cur:
            await cb.message.edit_text(
                "Поточний вид:\n"\
                f"{cur}\n"\
                "Оберіть вид професії зі списку:"
            )
        else:
            await cb.message.edit_text("Оберіть вид професії зі списку:")
        await cb.message.edit_reply_markup(kb.new_tact(data[0]))
    else:
        db.push(data[0], cb.from_user.username, tact=kb.ACTIVITY_TYPES[int(data[-1])])
        await cb.answer("Інформацію записано", show_alert=False)
        if data[0] == 'e':
            await hndl_e.fill(cb)
        else:
            await hndl_r.fill(cb)
    return

@dp.callback_query_handler(text_contains="edu")
async def edu(cb: CallbackQuery):
    data = cb.data.split(':')
    back_handler = hndl_r.fill if data[0] == 'r' else hndl_e.fill
    kb = kb_r.edu if data[0] == 'r' else kb_e.edu
    question = "Яка освіта необхідна робітнику?" if data[0] == 'r' else "Чи маєте Ви освіту?"
    if data[-1] == "edu":
        await cb.answer()
        cur = db.get(cb.from_user.username, db.COLS[5])
        if cur:
            await cb.message.edit_text(
                "Поточна інформація:\n"\
                f"{cur}\n"\
                "Можливі варіанти:", reply_markup=kb)
        else:
            await cb.message.edit_text(question, reply_markup=kb)
        return
    match data[-1]:
        case "high": db.push(data[0], cb.from_user.username, edu="Вища освіта")
        case "mid" : db.push(data[0], cb.from_user.username, edu="Cередня освіта")
        case "zero": db.push(data[0], cb.from_user.username, edu="Без освіти")
    await cb.answer("Інформацію записано", show_alert=False)
    await back_handler(cb)
    return

@dp.callback_query_handler(text_contains="xp")
async def xp(cb: CallbackQuery):
    data = cb.data.split(':')
    if data[-1] == "xp":
        await cb.answer()
        kb = kb_e.xp if data[0] == 'e' else kb_r.xp
        cur = db.get(cb.from_user.username, db.COLS[4])
        info = '\nТак\n' if cur == '1' else '\nНі\n'
        if cur:
            txt = f"Поточна інформація:{info}Можливі варіанти:"
        elif data[0] == 'e':
            txt = "Чи маєте Ви досвід роботи?"
        else:
            txt = "Чи необхідний досід робітнику?"
        await cb.message.edit_text(txt, reply_markup=kb)
        return
    elif data[-1] == 't':
        db.push(data[0], cb.from_user.username, xp='1')
    elif data[-1] == 'f':
        db.push(data[0], cb.from_user.username, xp='0')
    await cb.answer("Дані записано!", show_alert=False)
    f = hndl_r.fill if data[0]=='r' else hndl_e.fill
    await f(cb)
    return