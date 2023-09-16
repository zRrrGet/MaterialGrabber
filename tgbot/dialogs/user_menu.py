from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const, Format

from tgbot.misc.states import MainDialogSG

main_dialog = Dialog(
    Window(
        Const('Default'),
        state=MainDialogSG.main,
    )
)
