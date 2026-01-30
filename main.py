"""
Golden Cobra Bot - Main File
Запуск: python main.py
"""

import asyncio
import logging
import os
import sys
from pathlib import Path
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web
import asyncpg
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Импортируем твои модули
from goals import COMMUNITY_GOALS
from rank import RANKS, get_user_rank

# Глобальные переменные
db_pool = None

# ========== БАЗА ДАННЫХ ==========
async def init_database():
    """Инициализация базы данных"""
    global db_pool
    
    DATABASE_URL = os.getenv('DATABASE_URL')
    if not DATABASE_URL:
        logger.warning("DATABASE_URL not set, using SQLite fallback")
        return None
    
    try:
        db_pool = await asyncpg.create_pool(DATABASE_URL)
        
        # Создаем таблицы
        async with db_pool.acquire() as conn:
            # Таблица пользователей
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    telegram_id BIGINT UNIQUE NOT NULL,
                    username VARCHAR(255),
                    first_name VARCHAR(255),
                    last_name VARCHAR(255),
                    spent_stars DECIMAL(20, 2) DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # Таблица транзакций
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS transactions (
                    id SERIAL PRIMARY KEY,
                    user_id INT REFERENCES users(id),
                    amount DECIMAL(20, 2) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
        
        logger.info("Database initialized successfully")
        return db_pool
        
    except Exception as e:
        logger.error(f"Database error: {e}")
        return None

async def get_or_create_user(telegram_id, username, first_name, last_name):
    """Получаем или создаем пользователя"""
    if not db_pool:
        return None
    
    async with db_pool.acquire() as conn:
        user = await conn.fetchrow(
            'SELECT * FROM users WHERE telegram_id = $1',
            telegram_id
        )
        
        if not user:
            user = await conn.fetchrow(
                '''INSERT INTO users 
                   (telegram_id, username, first_name, last_name) 
                   VALUES ($1, $2, $3, $4) 
                   RETURNING *''',
                telegram_id, username, first_name, last_name
            )
        
        return user

async def add_stars_transaction(user_id, amount):
    """Добавляем транзакцию и обновляем баланс"""
    if not db_pool:
        return False
    
    async with db_pool.acquire() as conn:
        async with conn.transaction():
            # Добавляем транзакцию
            await conn.execute(
                'INSERT INTO transactions (user_id, amount) VALUES ($1, $2)',
                user_id, amount
            )
            
            # Обновляем потраченные звезды пользователя
            await conn.execute(
                'UPDATE users SET spent_stars = spent_stars + $1 WHERE id = $2',
                amount, user_id
            )
        
        return True

async def get_top_users(limit=10):
    """Получаем топ пользователей"""
    if not db_pool:
        return []
    
    async with db_pool.acquire() as conn:
        users = await conn.fetch(
            '''SELECT username, spent_stars 
               FROM users 
               WHERE spent_stars > 0 
               ORDER BY spent_stars DESC 
               LIMIT $1''',
            limit
        )
        return users

# ========== TELEGRAM BOT ==========
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    user = await get_or_create_user(
        message.from_user.id,
        message.from_user.username,
        message.from_user.first_name,
        message.from_user.last_name
    )
    
    # Получаем топ пользователей
    top_users = await get_top_users(limit=1)
    top_user_text = "Нет данных"
    if top_users:
        top_user_text = f"👑 @{top_users[0]['username'] or 'user'} — {top_users[0]['spent_stars']:,.0f} XTR"
    
    # Определяем ранг пользователя
    spent = user['spent_stars'] if user else 0
    rank = get_user_rank(spent)
    
    welcome_text = f"""
🔥 *GOLDEN COBRA* 🔥

*Добро пожаловать в элитный клуб!*

Здесь статус измеряется в звёздах (XTR). 
Тратьте звёзды, чтобы:
• Подниматься в рейтинге
• Выигрывать эксклюзивные NFT
• Получать подарки от Telegram
• Понтоваться перед другими

*Текущий лидер:*
{top_user_text}

*Ваш статус:*
Баланс: {spent:,.0f} XTR
Ранг: {rank['name']} {rank.get('icon', '')}
    """
    
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("💰 Потратить звёзды", callback_data="spend_stars"),
        InlineKeyboardButton("📊 Рейтинг", callback_data="show_rating"),
        InlineKeyboardButton("🏆 Мой ранг", callback_data="my_rank"),
        InlineKeyboardButton("🎯 Цели", callback_data="community_goals"),
        InlineKeyboardButton("🎁 NFT Магазин", web_app=WebAppInfo(url=f"{os.getenv('WEB_URL', '')}/nft-shop.html"))
    )
    
    await message.answer(welcome_text, parse_mode="Markdown", reply_markup=keyboard)

async def spend_stars_callback(callback_query: types.CallbackQuery):
    """Обработчик траты звезд"""
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
    await callback_query.answer()

async def handle_spend_amount(callback_query: types.CallbackQuery):
    """Обработчик выбора суммы"""
    data = callback_query.data.replace("spend_", "")
    
    if data == "Другая сумма":
        await callback_query.message.answer(
            "Введите количество звезд цифрами (например: 1500):"
        )
    else:
        try:
            amount = int(data)
            user_id = callback_query.from_user.id
            
            # Получаем пользователя
            user = await get_or_create_user(
                user_id,
                callback_query.from_user.username,
                callback_query.from_user.first_name,
                callback_query.from_user.last_name
            )
            
            if user:
                # Добавляем транзакцию
                success = await add_stars_transaction(user['id'], amount)
                
                if success:
                    # Получаем новый ранг
                    new_spent = user['spent_stars'] + amount
                    new_rank = get_user_rank(new_spent)
                    old_rank = get_user_rank(user['spent_stars'])
                    
                    response = f"""
✅ *Успешно потрачено {amount:,} XTR!*

Новый баланс: {new_spent:,.0f} XTR
Ранг: {new_rank['name']} {new_rank.get('icon', '')}
                    """
                    
                    # Проверяем повышение ранга
                    if new_rank['id'] > old_rank['id']:
                        response += f"\n\n🎉 *Поздравляем! Вы получили новый ранг!*"
                    
                    # Проверяем цели сообщества
                    total_spent = await get_total_spent()
                    for goal in COMMUNITY_GOALS:
                        if total_spent < goal['target'] <= total_spent + amount:
                            response += f"\n\n🎯 *Достигнута цель сообщества!*\n{goal['reward']}"
                    
                else:
                    response = "❌ Ошибка при обработке транзакции"
            else:
                response = "❌ Пользователь не найден"
            
            await callback_query.message.answer(response, parse_mode="Markdown")
            
        except ValueError:
            await callback_query.message.answer("❌ Неверный формат суммы")
    
    await callback_query.answer()

async def show_rating_callback(callback_query: types.CallbackQuery):
    """Показываем рейтинг"""
    top_users = await get_top_users(limit=10)
    
    if not top_users:
        text = "📊 *Рейтинг пуст*\n\nСтаньте первым, потратив звезды!"
    else:
        text = "🏆 *ТОП-10 ПОТРАТИВШИХ*\n\n"
        for i, user in enumerate(top_users, 1):
            rank_icon = "👑" if i == 1 else f"{i}."
            username = user['username'] or f"Пользователь {i}"
            text += f"{rank_icon} @{username} — {user['spent_stars']:,.0f} XTR\n"
    
    await callback_query.message.answer(text, parse_mode="Markdown")
    await callback_query.answer()

async def get_total_spent():
    """Получаем общее количество потраченных звезд"""
    if not db_pool:
        return 0
    
    async with db_pool.acquire() as conn:
        result = await conn.fetchval('SELECT COALESCE(SUM(spent_stars), 0) FROM users')
        return result or 0

# ========== WEB SERVER ==========
async def web_server():
    """Веб-сервер для NFT магазина"""
    app = web.Application()
    
    # Отдаем NFT магазин
    async def handle_nft_shop(request):
        with open('nft-shop.html', 'r', encoding='utf-8') as f:
            html = f.read()
        
        # Динамически вставляем данные
        top_users = await get_top_users(limit=5)
        leaderboard_data = []
        
        for i, user in enumerate(top_users, 1):
            leaderboard_data.append({
                'position': i,
                'username': user['username'] or f"user_{i}",
                'spent': float(user['spent_stars']),
                'rank': get_user_rank(user['spent_stars'])['name']
            })
        
        # Заменяем placeholder данными
        import json
        html = html.replace(
            'const leaderboardData = [];',
            f'const leaderboardData = {json.dumps(leaderboardData, ensure_ascii=False)};'
        )
        
        return web.Response(text=html, content_type='text/html')
    
    # API для получения данных
    async def handle_api_data(request):
        top_users = await get_top_users(limit=10)
        total_spent = await get_total_spent()
        
        data = {
            'total_spent': total_spent,
            'top_users': [
                {
                    'username': user['username'],
                    'spent_stars': float(user['spent_stars'])
                }
                for user in top_users
            ],
            'goals': COMMUNITY_GOALS
        }
        
        return web.json_response(data)
    
    app.router.add_get('/nft-shop.html', handle_nft_shop)
    app.router.add_get('/api/data', handle_api_data)
    
    return app

# ========== MAIN ==========
async def main():
    """Основная функция запуска"""
    logger.info("Starting Golden Cobra Bot...")
    
    # Проверяем токен бота
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not found in environment variables")
        logger.info("Create .env file with BOT_TOKEN=your_token_here")
        return
    
    # Инициализируем базу данных
    await init_database()
    
    # Создаем бота
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    
    # Регистрируем обработчики
    dp.register_message_handler(start_command, commands=['start'])
    dp.register_callback_query_handler(spend_stars_callback, lambda c: c.data == 'spend_stars')
    dp.register_callback_query_handler(handle_spend_amount, lambda c: c.data.startswith('spend_'))
    dp.register_callback_query_handler(show_rating_callback, lambda c: c.data == 'show_rating')
    
    # Запускаем веб-сервер
    web_app = await web_server()
    runner = web.AppRunner(web_app)
    await runner.setup()
    
    port = int(os.getenv('PORT', 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    logger.info(f"Web server started on port {port}")
    logger.info(f"Bot started: @{(await bot.get_me()).username}")
    
    # Запускаем бота
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()
        await runner.cleanup()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped")
