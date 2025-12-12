from aiogram import types
from aiogram.filters import Command

from bot import dp
from deezer import search_song, search_artist
from messages import *

last_command = {}
user_tracks = {}


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


@dp.message(Command("info"))
async def info_wait(message: types.Message):
    user_id = message.from_user.id
    last_command[user_id] = "info"
    await message.answer(INFO_MESSAGE)


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

    elif state == "info":
        await process_info(message)
        last_command[user_id] = None

async def process_song(message: types.Message):
    user_id = message.from_user.id
    query = message.text.strip()

    results = await search_song(query, limit=20)
    if results is None:
        await message.answer(API_ERROR_MESSAGE)
        return

    filtered = [t for t in results if query.lower() in t.get("title", "").lower()]

    if not filtered:
        await message.answer(NO_SONGS_MESSAGE)
        return

    user_tracks[user_id] = {"tracks": filtered, "index": 0}

    await send_next_songs(message)


async def send_next_songs(message: types.Message):
    user_id = message.chat.id

    data = user_tracks[user_id]
    tracks = data["tracks"]
    index = data["index"]

    count = 3
    chunk = tracks[index:index + count]

    data["index"] += count

    for track in chunk:
        title = track["title"]
        artist = track["artist"]["name"]
        link = track["link"]
        cover = track["album"]["cover_medium"]

        caption = f"{title} — {artist}\nСсылка: {link}"

        if cover:
            await message.answer_photo(photo=cover, caption=caption)
        else:
            await message.answer(caption)

    if data["index"] < len(tracks):
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="Показать ещё", callback_data="more_songs")]
            ]
        )
        await message.answer("Ещё?", reply_markup=keyboard)


@dp.callback_query(lambda c: c.data == "more_songs")
async def more_songs_callback(callback: types.CallbackQuery):
    await callback.answer()
    await send_next_songs(callback.message)


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
    fans = artist.get("nb_fan", 0)
    link = artist.get("link")
    picture = artist.get("picture_medium")

    caption = f"{name}\nФанатов - {fans}\nСсылка - {link}"

    if picture:
        await message.answer_photo(photo=picture, caption=caption)
    else:
        await message.answer(caption)

async def process_info(message: types.Message):
    query = message.text.strip()

    results = await search_song(query, limit=20)

    if not results:
        await message.answer(NO_INFO_MESSAGE)
        return

    query_lower = query.lower()

    filtered = [
        track for track in results
        if query_lower in (track.get("artist", {}).get("name", "").lower() + " " + track.get("title", "").lower())
    ]

    track = filtered[0] if filtered else results[0]

    title = track.get("title")
    artist = track.get("artist", {}).get("name")
    album = track.get("album", {}).get("title")
    cover = track.get("album", {}).get("cover_big")
    duration = track.get("duration")
    link = track.get("link")
    rank = track.get("rank")

    minutes = duration // 60
    seconds = duration % 60

    caption = (
        f"<b>{title}</b>\n"
        f"Исполнитель - {artist}\n"
        f"Альбом - {album}\n"
        f"Длительность - {minutes}:{seconds:02d}\n"
        f"Рейтинг Deezer - {rank}\n"
        f"{link}"
    )

    if cover:
        await message.answer_photo(photo=cover, caption=caption, parse_mode="HTML")
    else:
        await message.answer(caption, parse_mode="HTML")