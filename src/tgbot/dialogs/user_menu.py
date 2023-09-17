from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from src.tgbot.misc.states import MainDialogSG

main_dialog = Dialog(
    Window(
        Const('Default'),
        state=MainDialogSG.main,
    )
)
