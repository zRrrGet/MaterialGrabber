from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const
from aiogram_dialog.widgets.kbd import Button, Row
from aiogram_dialog import DialogManager, ShowMode

from src.core.external.controllers.user_controller import UserController
from src.tgbot.misc.states import RulesAgreementDialogSG


async def on_accept(callback: CallbackQuery, button: Button, manager: DialogManager):
    user_controller: UserController = manager.middleware_data['user_controller']
    user_controller.accept_rules(manager)

    await callback.message.delete()
    await manager.done(manager.dialog_data['garbage_msg_ids'], show_mode=ShowMode.SEND)


async def on_discard(callback: CallbackQuery, button: Button, manager: DialogManager):
    msg = await callback.message.answer('Для продолжения необходимо подтвердить '
                                        'свое согласие с пользовательским соглашением!')
    manager.dialog_data['garbage_msg_ids'].append(msg.message_id)


async def on_dialog_start(start_data: dict, manager: DialogManager):
    manager.dialog_data['garbage_msg_ids'] = []


rules_agreement_dialog = Dialog(
    Window(

        Const('Перед началом использования бота нейросети YOLICO пользователь обязан ознакомиться с '
              'Условиями использования данного сервиса. Оплата ( без оплата ) пользователем услуг YOLICO бота '
              'означает, что пользователь полностью согласен и принимает все условия Соглашения.\n\n'

              '1. YOLICO - нейросеть, вся обработка медиаматериалов носит ознакомительный характер!\n\n'
              '2. Все обработки пользователь совершает на свой страх и риск.\n\n'
              '3. Запрещено использовать медиаматериалы в коммерческих целях.\n\n'
              '4. Все пополнения приравниваются к пожертвованию на развитие проекта и идеи, не подлежат возврату.\n\n'
              '5. Претензии по качеству обработанных фото/видео не принимаются.\n\n'

              'Ограничение ответственности:\n\n'
              '1. YOLICO бот совершает обработку фото/видео в ознакомительных целях, и не несет ответственности за '
              'эти материалы.\n\n'
              '2. Пользователь, получивший обработанные фото/видео, несет полную ответственность за использование '
              'полученных медиаданных!\n\n'
              '3. YOLICO бот не несет ответственности за любые потери пользователя и любые перебои в работе системы.'),

        Row(
            Button(Const('✅ Согласен'), id='accept_rules', on_click=on_accept),
            Button(Const('❌ Не согласен'), id='discard_rules', on_click=on_discard)
        ),
        state=RulesAgreementDialogSG.main,
    ),
    on_start=on_dialog_start,
)
