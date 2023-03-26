import openai

model = "text-davinci-003"
openai.api_key = "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"

async def ract_example():
    completions = await openai.Completion.acreate(
        engine=model,
        prompt=
        "Опиши вакансію, бажано вказати наступні деталі:"\
        "• Опис обов'язків\n"\
        "• Які навички необхідні робітнику\n"\
        "• Режим роботи\n"\
        "• Коротка інформація щодо процесу найму\n",
        max_tokens=5,
        stop=None,
        top_p=0.1,
        stream=True,
    )
    async for c in completions:
        yield c["choices"][0]["text"]

async def eact_example():
    completions = await openai.Completion.acreate(
        engine=model,
        prompt=
            "Напиши резюме, вказавши:\n"\
            "- Свої вміння та навички\n"\
            "- На який режим роботи розраховуєш\n"\
            "- Найцікавіші завдання."
        ,
        max_tokens=1000,
        stop=None,
        top_p=0.5,
        stream=True,
    )
    async for c in completions:
        yield c["choices"][0]["text"]

async def rate_r(txt_vac: str, txt_res: str):
    completions = await openai.Completion.acreate(
        engine=model,
        prompt=
            "Rate how the CV matches the Vacancy.\n"\
            f"Vacancy:\n{txt_vac}.\n"\
            f"CV:\n{txt_res}\n"\
            "Output only one number which is rate from 0 to 10,"\
            "where 0 - cv doesn`t match a vacancy, 10 - perfect match."\
            "If exists information that is mentioned in Vacancy but not in CV,"\
            "lower rate."\
        ,
        max_tokens=5,
        stop=None,
        top_p=0.3,
        stream=False,
    )
    return completions['choices'][0]['text']

async def rate_e(txt_vac: str, txt_res: str):
    completions = await openai.Completion.acreate(
        engine=model,
        prompt=
            "Rate how the CV matches the Vacancy.\n"\
            f"Vacancy:\n{txt_vac}.\n"\
            f"CV:\n{txt_res}\n"\
            "Output only one number which is rate from 0 to 10,"\
            "where 0 - vacancy doesn't match CV, 10 - perfect match."\
            "If exists requirement in Vacancy text but I can't do it according to CV"\
            "lower rate."\
        ,
        max_tokens=5,
        stop=None,
        top_p=0.3,
        stream=False,
    )
    return completions['choices'][0]['text']
