from aiogram import Bot, Dispatcher, types

TELEGRAM_TOKEN = "8300573220:AAGJIgJfHp_PV71Mm4wETY8s2QTy1cENrFc"

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

@dp.message()
async def start_command(message: types.Message):
    if message.text == "/start":
        await message.reply("Привет, забредший сюда путник. Скоро здесь появится много всего интересного!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())



