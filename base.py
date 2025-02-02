import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import InputFile
from yt_dlp import YoutubeDL
from decouple import config

API_TOKEN = config("API_TOKEN")

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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
    }

    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return os.path.join(output_dir, f"{info['title']}.mp3")

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Отправь мне ссылку на YouTube, и я скачаю аудио.")

@dp.message_handler()
async def download_and_send_audio(message: types.Message):
    try:
        url = message.text
        audio_path = download_audio(url)
        audio = InputFile(audio_path)

        await message.reply_audio(audio)
        os.remove(audio_path)
    except Exception as e:
        await message.reply(f"Ошибка при скачивании: {e}")

async def main():
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
