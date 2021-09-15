import telebot

import commands
from statements import useful_methods
from statements.admin_orders import signs
from utils import db_util, key_util


def save_order(message: telebot.types.Message, bot: telebot.TeleBot):
    print('saving')
    chat_id = useful_methods.id_from_user(message.from_user)
    if message.content_type == 'photo':
        db_util.write_obj_to_table(table_class=db_util.UserSigns,
                                   identifier=db_util.UserSigns.client_chat_id,
                                   value=chat_id,
                                   photo_id=message.photo[-1].file_id,
                                   username=message.from_user.first_name,
                                   client_chat_id=chat_id,
                                   is_submitted=False)
        bot.send_message(chat_id=chat_id,
                         text='ожидайте подтверждения',
                         reply_markup=key_util.create_reply_keyboard([commands.back]))
        signs.notify_admins(bot)
    else:
        bot.send_message(chat_id=chat_id,
                         text='Отправьте скриншот')
