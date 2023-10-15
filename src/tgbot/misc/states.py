from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    main = State()
    in_dev = State()


class DownloaderDialogSG(StatesGroup):
    main = State()
    content_type_select = State()
    download_link_input = State()


class RulesAgreementDialogSG(StatesGroup):
    main = State()


class SubAlertDialogSG(StatesGroup):
    warn_text = State()
    sub_control = State()


class ProgressObserverDialogSG(StatesGroup):
    main = State()
