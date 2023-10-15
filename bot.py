import asyncio
import urllib3
import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.core.external.components.mega_storage import MegaStorage
from src.core.external.components.content_downloader.beatsnoop_downloader import BeatsnoopDownloader
from src.core.external.components.content_downloader.session_factory.base_session_factory import BaseSessionFactory

from src.core.domain.interactors.day_limit.base_limit_interactor import DayLimitInteractor
from src.core.domain.interactors.content_downloader.downloader_worker import DownloaderWorker
from src.core.domain.interactors.content_downloader.base_downloader_interactor import DownloaderInteractor
from src.core.domain.interactors.user.base_user_interactor import UserInteractor

from src.core.external.controllers.day_limit_controller import DayLimitController
from src.core.external.controllers.user_controller import UserController
from src.core.external.controllers.downloader_controller import DownloaderController

from src.core.external.repositories.alchemy_repo_factory import AlchemyRepoFactory
from src.core.external.components.sub_validator import SubValidator
from src.core.domain.req_handler.chain_factory import ChainFactory

from src.tgbot.config import load_config, Config
from src.tgbot.handlers.user import register_user
from src.tgbot.handlers.admin import register_admin
from src.tgbot.handlers.errors import register_all_error_handlers

from src.tgbot.middlewares.user_middleware import UserMiddleware

from src.tgbot.dialogs.main_menu import main_dialog
from src.tgbot.dialogs.downloader.downloader_menu import downloader_dialog
from src.tgbot.dialogs.pre_events.sub_alert import sub_alert_dialog
from src.tgbot.dialogs.pre_events.rules_agreement import rules_agreement_dialog
from src.tgbot.dialogs.progress.progress_observer import progress_observer_dialog

logger = logging.getLogger(__name__)


def register_all_dialogs(dr: Dispatcher):
    dr.include_router(main_dialog)
    dr.include_router(downloader_dialog)
    dr.include_router(sub_alert_dialog)
    dr.include_router(rules_agreement_dialog)
    dr.include_router(progress_observer_dialog)
    setup_dialogs(dr)


def register_all_middlewares(dp):
    dp.update.middleware(UserMiddleware())


def register_all_handlers(dp):
    register_user(dp)
    register_admin(dp)
    register_all_error_handlers(dp)


async def set_default_commands(bot):
    await bot.set_my_commands([
        BotCommand(command='start', description='Меню')
    ])


async def main():
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config: Config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.token, parse_mode='HTML')

    repo_factory = AlchemyRepoFactory(config.db_url)
    user_repo = repo_factory.create_user_repo()
    channel_repo = repo_factory.create_channel_repo()
    request_repo = repo_factory.create_download_request_repo()

    sub_validator = SubValidator(bot)
    user_interactor = UserInteractor(user_repo, channel_repo, sub_validator)
    user_controller = UserController(user_interactor)

    day_limit_interactor = DayLimitInteractor(request_repo)
    day_limit_controller = DayLimitController(day_limit_interactor)

    content_downloader = BeatsnoopDownloader(BaseSessionFactory())
    downloader_interactor = DownloaderInteractor(user_interactor, day_limit_interactor, request_repo, ChainFactory())
    downloader_controller = DownloaderController(downloader_interactor)

    mega_storage = MegaStorage('C:\\Users\\Administrator\\AppData\\Local\\MEGAcmd', 'data')
    DownloaderWorker(request_repo, content_downloader, mega_storage).start()

    dp = Dispatcher(storage=storage, config=config, user_controller=user_controller,
                    downloader_controller=downloader_controller, day_limit_controller=day_limit_controller)

    await set_default_commands(bot)
    register_all_dialogs(dp)
    register_all_handlers(dp)
    register_all_middlewares(dp)

    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)
    finally:
        await dp.storage.close()
        await bot.session.close()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
