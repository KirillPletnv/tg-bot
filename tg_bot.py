import logging
import json
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.utils.token import TokenValidationError
from check_imei import check_imei, format_dict_to_string

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "7826423138:AAF4kzMayx1VUY_f8tXpxT8nqqUwsnZjzX8"
# Мой бот @verify_mey_bot id=7826423138 - 'verifybot'
#"deviceId": "350356670657487"
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привет! Отправь мне IMEI, и я проверю его. На тестовом сервисе N15, потому что он дает смешанные рандомизированные результаты, что подходит для проверки одного и того же imei для разных ситуаций")

@dp.message()
async def handle_message(message: types.Message):
    imei = message.text
    if imei.isdigit() and len(imei) == 15:  # Проверка, что IMEI состоит из 15 цифр
        response = check_imei(imei)
        json_data = json.dumps(response, ensure_ascii=False,)
        formatted_string = format_dict_to_string(response)
        #Строка ответа если требуется непосредственно json
        #await message.answer(json_data, indent=4)

        #Строка ответа если требуется человекочитаемый json, с использованием построчного вывода функцией formatted_string
        await message.answer(formatted_string)
    else:
        await message.answer("Некорректный IMEI. Пожалуйста, отправьте 15-значный IMEI.")


async def main():
    try:
        await dp.start_polling(bot)
    except TokenValidationError:
        logger.error("Неверный токен")
    except Exception as e:
        logger.error(f"Ошибка: {e}")


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
