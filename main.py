# main.py - структура основных обработчиков
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
import asyncio
import logging

class GoldenCobraBot:
    def __init__(self):
        self.bot = Bot(token="8536282991:AAHUyTx0r7Q03bwDRokvogbmJAIbkAnYVpM")
        self.dp = Dispatcher(self.bot)
        self.setup_handlers()
        
    def setup_handlers(self):
        # Команда старта
        @self.dp.message_handler(commands=['start'])
        async def start_command(message: types.Message):
            welcome_text = """
🔥 *GOLDEN COBRA* 🔥

*Добро пожаловать в элитный клуб!*

Здесь статус измеряется в звёздах (XTR). 
Тратьте звёзды, чтобы:
• Подниматься в рейтинге
• Выигрывать эксклюзивные NFT
• Получать подарки от Telegram
• Понтоваться перед другими

*Текущий лидер:*
👑 @rich_user — 15,245 XTR

Ваш баланс: 0 XTR
Ваш ранг: Новичок 🐍
            """
            keyboard = InlineKeyboardMarkup(row_width=2)
            keyboard.add(
                InlineKeyboardButton("💰 Потратить звёзды", callback_data="spend_stars"),
                InlineKeyboardButton("📊 Рейтинг", callback_data="show_rating"),
                InlineKeyboardButton("🏆 Мой ранг", callback_data="my_rank"),
                InlineKeyboardButton("🎯 Цели сообщества", callback_data="community_goals"),
                InlineKeyboardButton("🎁 NFT Магазин", web_app=WebAppInfo(url="https://your-domain.com/nft-shop"))
            )
            await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)
        
        # Обработка траты звёзд
        @self.dp.callback_query_handler(lambda c: c.data == 'spend_stars')
        async def spend_stars(callback_query: types.CallbackQuery):
            keyboard = InlineKeyboardMarkup()
            amounts = [100, 500, 1000, 5000, 10000, "Другая сумма"]
            for amount in amounts:
                keyboard.add(InlineKeyboardButton(
                    f"{amount} XTR" if isinstance(amount, int) else amount,
                    callback_data=f"spend_{amount}"
                ))
            await callback_query.message.answer(
                "🔥 *Сколько звёзд хотите потратить?*\n\n"
                "Каждая потраченная звезда приближает вас к эксклюзивным наградам!",
                parse_mode="Markdown",
                reply_markup=keyboard
            )
