import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.core.external.controllers.user_controller import UserController
from src.core.domain.interactors.user_interactor import UserInteractor
from src.core.external.repositories.user.fake_user_repo import FakeUserRepo

from src.tgbot.config import load_config
from src.tgbot.handlers.user import register_user
from src.tgbot.handlers.admin import register_admin
from src.tgbot.handlers.errors import register_all_error_handlers
from src.core.external.orm.base import create_pool

from src.tgbot.dialogs.user_menu import main_dialog

logger = logging.getLogger(__name__)


def register_all_dialogs(dr: Dispatcher):
    dr.include_router(main_dialog)
    setup_dialogs(dr)


def register_all_middlewares(dp):
    pass


def register_all_handlers(dp):
    register_user(dp)
    register_admin(dp)
    register_all_error_handlers(dp)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    user_repo = FakeUserRepo()
    user_interactor = UserInteractor(user_repo)
    user_controller = UserController(user_interactor)

    dp = Dispatcher(storage=storage, config=config, user_controller=user_controller)
    # pool = await create_pool('sqlite+aiosqlite:///app.db')

    register_all_dialogs(dp)
    register_all_handlers(dp)
    register_all_middlewares(dp)

    try:
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")

#  todo Application
# ContentDownloader
# FileStorage
# ContentRepo
# UserRepo

# DownloaderWorker

# DownloaderController
# DownloaderInteractor
# - RequestDownload
# - GetRequestStatus

# UserController
# UserInteractor
# - EnsureUser
# - GrantBaseAccessUser
