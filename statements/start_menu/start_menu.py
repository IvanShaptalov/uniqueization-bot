"""choose profile - first statement in bot,
(you can choose admin account if your account exists in admin_accounts db)"""
import telebot

import commands
from statements import useful_methods
from utils import db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    chat_id = useful_methods.id_from_message(message)
    admin = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.AdminAccounts,
                                                      identifier=db_util.AdminAccounts.chat_id,
                                                      value=chat_id)
    # check for admin
    if message.text == commands.start_menu:
        bot.send_message(chat_id=chat_id,
                         text='Приветствую!')
    markup = key_util.remove_keyboard()
    if isinstance(admin, db_util.AdminAccounts):
        markup = key_util.create_reply_keyboard([commands.new_signs])
    bot.send_message(chat_id=chat_id,
                     text='отправьте видео или фото размером до 20 мб для его уникализации.',
                     reply_markup=markup)
