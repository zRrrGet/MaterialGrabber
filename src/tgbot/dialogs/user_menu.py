from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Row, Button

from src.tgbot.misc.states import MainDialogSG

main_dialog = Dialog(
    Window(
        Const('Выберите сервис, с которого нужно скачать материалы'),
        Row(
            Button(Const('Тест 1'), id='src_1'),
            Button(Const('Тест 2'), id='src_2')
        ),
        state=MainDialogSG.main,
    )
)
