import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
from cfg import TELEGRAM_BOT_TOKEN
from gpt import beautify_text
from speech import audio_to_text
import os

logging.basicConfig(level=logging.INFO)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    if message.voice:
        file = await message.voice.get_file()
        audio_path = f"voice_{message.message_id}.ogg"
        await file.download_to_drive(audio_path)
        # Проверка, скачался ли файл и его размер
        if os.path.exists(audio_path):
            logging.info(f"[AUDIO] Файл скачан: {audio_path}, размер {os.path.getsize(audio_path)} байт")
        else:
            logging.error(f"[AUDIO] Файл {audio_path} не скачался")
            await message.reply_text("Ошибка загрузки аудиофайла.")
            return
        try:
            text = audio_to_text(audio_path)
            logging.info(f"[AUDIO] Whisper распознал: '{text}'")
        except Exception as e:
            await message.reply_text("Ошибка распознавания аудио.")
            logging.error(e)
            os.remove(audio_path)
            return
        os.remove(audio_path)
    elif message.text:
        text = message.text
        logging.info(f"[TEXT] Получен текст: '{text}'")
    else:
        await message.reply_text("Пришли голосовое или текстовое сообщение!")
        return

    # Логируем, что отправляем в GPT
    logging.info(f"[GPT] Отправляем текст: '{text}'")
    try:
        beautified = beautify_text(text)
        logging.info(f"[GPT] Получен ответ: '{beautified}'")
    except Exception as e:
        await message.reply_text("Ошибка обработки через GPT.")
        logging.error(e)
        return

    await message.reply_text(beautified)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT | filters.VOICE, handle_message))
    app.run_polling()
