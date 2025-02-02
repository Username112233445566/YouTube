import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from yt_dlp import YoutubeDL
from decouple import config
from aiogram.types import FSInputFile

API_TOKEN = config("API_TOKEN")

bot = Bot(token=API_TOKEN)

dp = Dispatcher()

def download_audio(url):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(output_dir, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'noplaylist': True,
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(output_dir, f"{info['title']}.mp3")

@dp.message(Command("start"))
async def send_welcome(message: types.Message):

    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="Скачать аудио с YouTube"))
    builder.adjust(1)

    await message.reply(
        "Привет! Я бот для скачивания аудио с YouTube. Нажми кнопку ниже, чтобы начать.",
        reply_markup=builder.as_markup(resize_keyboard=True)
    )

@dp.message()
async def download_and_send_audio(message: types.Message):
    if message.text == "Скачать аудио с YouTube":
        await message.reply("Отправь мне ссылку на YouTube, и я скачаю аудио.")
        return

    url = message.text.strip()
    
    try:
        audio_path = download_audio(url)
        if os.path.exists(audio_path):
            audio_file = FSInputFile(audio_path)
            await message.reply_audio(audio_file)
            os.remove(audio_path)

            await message.delete()
        else:
            await message.reply("Ошибка: файл не был найден.")
    except Exception as e:
        await message.reply(f"Произошла ошибка при скачивании: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())