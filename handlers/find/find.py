from . import *

@dp.callback_query_handler(text_contains="find")
async def find(cb: CallbackQuery):
    info = db.get_info(cb.from_user.username)
    res = []
    data = db.get_same(cb.data[0], info[2], info[4], info[5])
    if cb.data[-1] == 'b':
        if not data:
            txt = "На жаль, робітників немає(" if cb.data[0] == 'r' else "На ринку немає відповідних вакансій("
            await cb.message.edit_text(txt, reply_markup=kb.new(kb.back(cb.data[0]+":find")))
            return
        await cb.message.edit_text("Доведеться трішки зачекати...", reply_markup=kb.new(kb.back(cb.data[0]+":find")))
        rates = []
        for entity, act in data:
            if cb.data[0] == 'r':
                rate = num_from_str(await ai.rate_r(info[3], act))
            else:
                rate = num_from_str(await ai.rate_e(act, info[3]))
            res.append([rate, entity])
            rates.append(str(rate))
        for i in range(len(res)):
            for j in range(i+1, len(res)):
                if res[i][0] < res[j][0]:
                    res[i], res[j] = res[j], res[i]
        if cb.data[0] == 'r':
            txt = f"На ринку вдалося знайти {len(res)} працівників з оцінками: {', '.join(rates)}\n"\
                  f"Найкращий варіант:\n@{res[0][1]} з оцінкою {res[0][0]}/10\n"\
                  f"Його резюме:\n{db.get(res[0][1], db.COLS[3])}"
        else:
            txt = f"На ринку вдалося знайти {len(res)} вакансій з оцінками: {', '.join(rates)}\n"\
                  f"Найкращий роботодавець:\n@{res[0][1]} з вакансією на {res[0][0]}/10 балів\n"\
                  f"Вакансія:\n{db.get(res[0][1], db.COLS[3])}"
        await cb.message.edit_text(txt, reply_markup=kb.new(kb.back(cb.data[0]+":find")))
    elif cb.data[-1] == 'a':
        if not data:
            txt = "На жаль, робітників немає(" if cb.data[0] == 'r' else "На ринку немає відповідних вакансій("
            await cb.message.edit_text(txt, reply_markup=kb.new(kb.back(cb.data[0]+":find")))
            return
        if cb.data[0] == 'r':
            txt = "Всі робітники, які підходять до вашої вакансії:\n"
            for entity, act in data:
                txt += f"Робітник @{entity}:\n{act}\n🔻🔺🔻🔺🔻🔺🔻🔻🔺🔻🔺🔻🔺🔻\n"
        else:
            txt = "Всі вакансії, які Вам підходять:\n"
            for entity, act in data:
                txt += f"Роботодавець @{entity}:\n{act}\n🔻🔺🔻🔺🔻🔺🔻🔻🔺🔻🔺🔻🔺🔻\n"
        await cb.message.edit_text(txt, reply_markup=kb.new(kb.back(cb.data[0]+":find")))
    elif cb.data[0] == 'r':
        await cb.message.edit_text("Ви можете переглянути всіх робітників, які підходять "\
            "під вашу вакансію.\nАбо відібрати найкращого, обирайте:", reply_markup=kbr_find)
    else:
        await cb.message.edit_text("Ви можете переглянути всі вакансії, які Вам підходять.\n"\
            "Або відібрати найкращу, обирайте:", reply_markup=kbe_find)
    return

def num_from_str(s: str):
    res = ''
    for i in s:
        if i.isdigit() or i == '.':
            res += i
    return float(res)