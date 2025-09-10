import os
import asyncio
from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ParseMode
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from config import TOKEN, CHAT_ID
from parsers.oil import get_oil_prices
from parsers.currency import get_currency_rates
from parsers.moex import get_moex_index
from parsers.metals import get_metal_prices
from parsers.wheat import get_wheat_price
from parsers.fuel import get_fuel_prices
from datetime import datetime

bot = Bot(token=TOKEN)
dp = Dispatcher()
router = Router()
MESSAGE_FILE = "message_id.txt"


# === Сборка отчёта ===
async def build_report() -> str:
    try:
        brent, crude = await get_oil_prices()
        rates = get_currency_rates()
        imoex = get_moex_index()
        metals = get_metal_prices()
        wheat_price = await get_wheat_price()
        fuel = get_fuel_prices()

        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        fuel_text = (
        f"• ДТ — {fuel.get('Дизель', 'н/д')} ₽\n"
        f"• АИ-92 — {fuel.get('АИ-92', 'н/д')} ₽\n"
        f"• АИ-95 — {fuel.get('АИ-95', 'н/д')} ₽\n"
        f"• АИ-98 — {fuel.get('АИ-98', 'н/д')} ₽"
        )

        return f"""
    Brent {brent} – $ {rates['USD']} – Moex {imoex}// Пшеница - {wheat_price}
    
🛢 Нефть: 
• Brent — ${brent}
• Crude — ${crude}

💱 Валюта:
• ₽ / $ — {rates['USD']}
• ₽ / € — {rates['EUR']}
• ₽ / ¥ — {rates['JPY']}

📈 Индекс:
• МосБиржа — {imoex}

🪙 Металлы:
• Золото — ${metals['Gold']}
• Серебро — ${metals['Silver']}
• Платина — ${metals['Platinum']}

🌾 Пшеница:
• Wheat — ${wheat_price}

⏰ Обновлено: {now}

⛽️ Топливо:
{fuel_text}
"""
    except Exception as e:
        return f"⚠️ Ошибка при сборке отчета: {e}"

def save_message_id(message_id: int):
    with open(MESSAGE_FILE, "w") as f:
        f.write(str(message_id))


def load_message_id() -> int | None:
    if not os.path.exists(MESSAGE_FILE):
        return None
    with open(MESSAGE_FILE, "r") as f:
        return int(f.read().strip())


async def send_new_message(text: str) -> int:
    msg = await bot.send_message(chat_id=CHAT_ID, text=text, parse_mode=ParseMode.HTML)
    save_message_id(msg.message_id)
    return msg.message_id


async def send_or_update():
    print(f"[{datetime.now().strftime('%H:%M:%S')}] 🔁 Обновление сообщения...")
    text = await build_report()
    message_id = load_message_id()

    if message_id:
        try:
            await bot.edit_message_text(
                chat_id=CHAT_ID,
                message_id=message_id,
                text=text,
                parse_mode=ParseMode.HTML
            )
            print("✅ Сообщение обновлено.")
        except Exception as e:
            print(f"⚠️ Ошибка при обновлении: {e}")
            new_id = await send_new_message(text)
            print(f"📤 Создано новое сообщение с ID {new_id}.")
    else:
        new_id = await send_new_message(text)
        print(f"📤 Отправлено новое сообщение с ID {new_id}.")


# === Команда /reset ===
@router.message(F.text == "/reset")
async def reset_message(msg: Message):
    message_id = load_message_id()
    if message_id:
        try:
            await bot.delete_message(chat_id=CHAT_ID, message_id=message_id)
            os.remove(MESSAGE_FILE)
            await msg.answer("Сообщение удалено. Отправляю новое...")
        except Exception as e:
            await msg.answer(f"Не удалось удалить сообщение: {e}")
    else:
        await msg.answer("Сообщение не найдено, создаю новое...")

    new_text = await build_report()
    new_id = await send_new_message(new_text)
    await msg.answer("Новое сообщение создано и отслеживается.")


# === Основной запуск ===
async def main():
    dp.include_router(router)

    # 1. Стартовое обновление
    await send_or_update()

    # 2. Планировщик обновлений
    scheduler = AsyncIOScheduler()
    scheduler.add_job(send_or_update, "interval", minutes=1)
    scheduler.start()

    # 3. Запуск бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
