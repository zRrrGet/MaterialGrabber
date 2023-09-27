from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    main = State()
    download_link_input = State()
    download_progress = State()


class SubAlertDialogSG(StatesGroup):
    main = State()


class ProgressObserverDialogSG(StatesGroup):
    main = State()
