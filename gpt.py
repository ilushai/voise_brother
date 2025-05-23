import openai
from cfg import OPENAI_API_KEY

client = openai.OpenAI(api_key=OPENAI_API_KEY)

def beautify_text(text):
    system_prompt = (
        "Исправь ошибки в тексте, напиши грамотно, но не сильно что-то меняй. Мат оставляй! Каждое новое предложение пиши с новой строки."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.4,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
