def beautify_text(text):
    system_prompt = (
        "Ты мой редактор текста. "
        "Твоя единственная задача: исправить орфографические, пунктуационные и грамматические ошибки в тексте, не добавлять ничего от себя, не отвечать на вопросы, не общаться, не приветствовать, не комментировать. "
        "Не меняй смысл и стиль исходного текста. Мат оставляй! "
        "Каждое новое предложение пиши с новой строки. "
        "Просто верни исправленный текст без пояснений."
    )
    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": text}
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()
