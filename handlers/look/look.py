from . import *

@dp.callback_query_handler(text_contains="look")
async def look(cb: CallbackQuery):
    data = cb.data.split(':')
    uname = cb.from_user.username
    kb = rkb if data[0]=='r' else ekb
    if db.exist(uname):
        ecols = db.get_emptycols(uname)
        if len(ecols) != len(db.COLS) - 2:
            txt = "Інформація в базі даних:\n"
            for i, col in enumerate(db.COLS[2:]):
                info = db.get(uname, col)
                if i == 2:
                    match info:
                        case '1': info = "Необхідний" if data[0] == 'r' else "Маю досвід"
                        case '0': info = "Необов'язковий" if data[0] == 'r' else "Досвіду немає"
                if info:
                    txt += f"✅ {db.TRANSLATE[col][data[0]]}:\n{info}\n"
                else:
                    txt += f"❎ {db.TRANSLATE[col][data[0]]} - інформація відсутня!\n"
            await cb.message.edit_text(txt, reply_markup=kb)
        else:
            await cb.message.edit_text("Ви не заповнили жодної інформації", reply_markup=kb)
    else:
        await cb.message.edit_text("Вас немає в базі даних", reply_markup=kb)
    return
