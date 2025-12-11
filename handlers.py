from aiogram import types
from aiogram.filters import Command
from deezer import search_song
from messages import START_MESSAGE, HELP_MESSAGE, NO_QUERY_MESSAGE, NO_SONGS_MESSAGE, API_ERROR_MESSAGE
from bot import dp

@dp.message(Command("start"))
async def start_command(message: types.Message):
    await message.answer(START_MESSAGE)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    await message.answer(HELP_MESSAGE)

@dp.message(Command("song"))
async def song_command(message: types.Message):
    query = message.text.replace("/song", "").strip()
    if not query:
        await message.answer(NO_QUERY_MESSAGE)
        return

    results = await search_song(query)
    if results is None:
        await message.answer(API_ERROR_MESSAGE)
        return

    filtered = [track for track in results if query.lower() in track.get("title", "").lower()]

    if not filtered:
        await message.answer(NO_SONGS_MESSAGE)
        return

    for track in filtered:
        title = track.get("title")
        artist = track.get("artist", {}).get("name")
        link = track.get("link")
        cover = track.get("album", {}).get("cover_medium")

        caption = f"{title} — {artist}\nСсылка: {link}"

        if cover:
            await message.answer_photo(photo=cover, caption=caption)
        else:
            await message.answer(caption)