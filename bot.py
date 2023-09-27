import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs

from src.core.external.components.content_downloader.fake_downloader import FakeContentDownloader
from src.core.external.components.content_downloader.content_downloader import ContentDownloader
from src.core.domain.entities.download_request import ContentType
from src.core.external.components.content_downloader.sources.downloader_client import IDownloaderClient

from src.core.domain.interactors.content_downloader.downloader_worker import DownloaderWorker
from src.core.domain.interactors.content_downloader.base_downloader_interactor import DownloaderInteractor
from src.core.domain.interactors.user.base_user_interactor import UserInteractor

from src.core.external.controllers.user_controller import UserController
from src.core.external.controllers.downloader_controller import DownloaderController

from src.core.external.repositories.sqlite_repo_factory import SqliteRepoFactory
from src.core.external.components.sub_validator import SubValidator
from src.core.domain.req_handler.chain_factory import ChainFactory

from src.tgbot.config import load_config
from src.tgbot.handlers.user import register_user
from src.tgbot.handlers.admin import register_admin
from src.tgbot.handlers.errors import register_all_error_handlers

from src.tgbot.middlewares.user_middleware import UserMiddleware

from src.tgbot.dialogs.user_menu import main_dialog
from src.tgbot.dialogs.sub_alert import sub_alert_dialog
from src.tgbot.dialogs.progress_observer import progress_observer_dialog

logger = logging.getLogger(__name__)


def register_all_dialogs(dr: Dispatcher):
    dr.include_router(main_dialog)
    dr.include_router(sub_alert_dialog)
    dr.include_router(progress_observer_dialog)
    setup_dialogs(dr)


def register_all_middlewares(dp):
    dp.update.middleware(UserMiddleware())


def register_all_handlers(dp):
    register_user(dp)
    register_admin(dp)
    register_all_error_handlers(dp)


async def main():

    content_downloader = ContentDownloader()
    content_downloader.download(input('shit: '),
                                ContentType.video)

    return

    logging.basicConfig(
        level=logging.INFO,
        format=u'%(filename)s:%(lineno)d #%(levelname)-8s [%(asctime)s] - %(name)s - %(message)s',
    )
    logger.info("Starting bot")
    config = load_config(".env")

    storage = MemoryStorage()
    bot = Bot(token=config.tg_bot.token, parse_mode='HTML')

    repo_factory = SqliteRepoFactory('app.db')
    user_repo = repo_factory.create_user_repo()
    channel_repo = repo_factory.create_channel_repo()
    request_repo = repo_factory.create_download_request_repo()

    sub_validator = SubValidator(bot)
    user_interactor = UserInteractor(user_repo, channel_repo, sub_validator)
    user_controller = UserController(user_interactor)

    content_downloader = FakeContentDownloader()
    downloader_interactor = DownloaderInteractor(user_interactor, request_repo, ChainFactory())
    downloader_controller = DownloaderController(downloader_interactor)

    DownloaderWorker(request_repo, content_downloader).start()

    dp = Dispatcher(storage=storage, config=config, user_controller=user_controller,
                    downloader_controller=downloader_controller)

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
