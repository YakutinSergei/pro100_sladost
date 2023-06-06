import asyncio
import logging

from handlers import other_handlers, user_handlers, admin_handlers, order_handler
from create_bot import bot, dp
from data_base import sqlite_bd

# Инициализируем логгер
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main():
    # Конфигурируем логирование
    logging.basicConfig(
        level=logging.INFO,
        format='%(filename)s:%(lineno)d #%(levelname)-8s '
               '[%(asctime)s] - %(name)s - %(message)s')

    # Выводим в консоль информацию о начале запуска бота
    logger.info('Starting bot')

    #Подключение к базе данных
    sqlite_bd.sql_start()
    sqlite_bd.sql_users()

    # Регистриуем роутеры в диспетчере




    dp.include_router(admin_handlers.router)
    dp.include_router(order_handler.router)
    dp.include_router(user_handlers.router)
    dp.include_router(other_handlers.router)

    # Пропускаем накопившиеся апдейты и запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())