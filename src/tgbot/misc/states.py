from aiogram.fsm.state import StatesGroup, State


class MainDialogSG(StatesGroup):
    main = State()
    content_type_select = State()
    download_link_input = State()


class RulesAgreementDialogSG(StatesGroup):
    main = State()
    sub_control = State()


class SubAlertDialogSG(StatesGroup):
    warn_text = State()
    sub_control = State()
    exit_text = State()


class ProgressObserverDialogSG(StatesGroup):
    main = State()
