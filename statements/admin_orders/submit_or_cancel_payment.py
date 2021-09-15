from datetime import datetime

import telebot

from statements import useful_methods
from utils import db_util
from datetime import timedelta


def cancel_payment_call(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    """cancel payment call"""
    # VALIDATION
    if isinstance(call, telebot.types.CallbackQuery):
        if call.data and call.message:
            order_id = call.data
            message = call.message
            if isinstance(message, telebot.types.Message):
                chat_id = useful_methods.id_from_message(message=message)
                user = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.UserSigns,
                                                                 identifier=db_util.UserSigns.order_id,
                                                                 value=order_id)

                if isinstance(user, db_util.UserSigns):
                    db_util.delete_obj_from_table(table_class=db_util.UserSigns,
                                                  identifier=db_util.UserSigns.order_id,
                                                  value=user.order_id)
                    bot.delete_message(chat_id=chat_id,
                                       message_id=message.message_id)
                    bot.send_message(chat_id=user.client_chat_id,
                                     text='ваша заявка отменена,\nдля получения более детальной информации\n'
                                          'свяжитесь со службой поддержки')


def submit_payment_call(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    """submit payment call"""
    # VALIDATION
    if isinstance(call, telebot.types.CallbackQuery):
        if call.data and call.message:
            order_id = call.data
            message = call.message
            if isinstance(message, telebot.types.Message):
                chat_id = useful_methods.id_from_message(message=message)


                end_date = datetime.now() + timedelta(days=30)

                db_util.edit_obj_in_table(table_class=db_util.UserSigns,
                                          identifier=db_util.UserSigns.order_id,
                                          value=order_id,
                                          is_submitted=True,
                                          expiration_date=end_date)
                user = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.UserSigns,
                                                                 identifier=db_util.UserSigns.order_id,
                                                                 value=order_id)
                if isinstance(user, db_util.UserSigns):
                    bot.delete_message(chat_id=chat_id,
                                       message_id=message.message_id)
                    bot.send_message(chat_id=user.client_chat_id,
                                     text='пакет на месяц подключен!')

