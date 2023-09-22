from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    main = State()


class SubAlertDialogSG(StatesGroup):
    main = State()
