from aiogram import types
from aiogram.filters import Command

from bot import dp
from deezer import search_song, search_artist
from messages import START_MESSAGE, HELP_MESSAGE, SONG_MESSAGE, NO_SONGS_MESSAGE, ARTIST_MESSAGE, NO_ARTISTS_MESSAGE, API_ERROR_MESSAGE

last_command = {}

@dp.message(Command("start"))
async def start_command(message: types.Message):
    last_command[message.from_user.id] = None
    await message.answer(START_MESSAGE)

@dp.message(Command("help"))
async def help_command(message: types.Message):
    last_command[message.from_user.id] = None
    await message.answer(HELP_MESSAGE)

@dp.message(Command("song"))
async def song_wait(message: types.Message):
    user_id = message.from_user.id
    last_command[user_id] = "song"
    await message.answer(SONG_MESSAGE)

@dp.message(Command("artist"))
async def artist_wait(message: types.Message):
    user_id = message.from_user.id
    last_command[user_id] = "artist"
    await message.answer(ARTIST_MESSAGE)

@dp.message()
async def text_handler(message: types.Message):
    user_id = message.from_user.id
    state = last_command.get(user_id)

    if not state:
        return
    if state == "song":
        await process_song(message)
        last_command[user_id] = None

    elif state == "artist":
        await process_artist(message)
        last_command[user_id] = None

async def process_song(message: types.Message):
    query = message.text.strip()

    results = await search_song(query, limit=20)
    if results is None:
        await message.answer(API_ERROR_MESSAGE)
        return

    filtered = [track for track in results if query.lower() in track.get("title", "").lower()]

    if not filtered:
        await message.answer(NO_SONGS_MESSAGE)
        return

    track = filtered[0]

    title = track["title"]
    artist = track["artist"]["name"]
    link = track["link"]
    cover = track["album"]["cover_medium"]

    caption = f"{title} — {artist}\nСсылка: {link}"

    if cover:
        await message.answer_photo(photo=cover, caption=caption)
    else:
        await message.answer(caption)

async def process_artist(message: types.Message):
    query = message.text.strip()

    results = await search_artist(query)
    if results is None:
        await message.answer(API_ERROR_MESSAGE)
        return

    if not results:
        await message.answer(NO_ARTISTS_MESSAGE)
        return

    artist = results[0]

    name = artist.get("name")
    fans = artist.get("nb_fan") or 0
    link = artist.get("link")
    picture = artist.get("picture_medium")

    caption = f"{name}\n Фанатов - {fans}\nСсылка - {link}"

    if picture:
        await message.answer_photo(photo=picture, caption=caption)
    else:
        await message.answer(caption)
