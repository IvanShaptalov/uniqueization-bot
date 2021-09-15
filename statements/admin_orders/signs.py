"""show non submitted order for clients"""
import threading

import telebot
from icecream import ic

import commands
from statements import useful_methods
from statements.admin_orders import submit_or_cancel_payment
from utils import db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    useful_methods.admin_account_verification(message, bot)
    chat_id = useful_methods.id_from_message(message)
    if message.text == commands.new_signs:
        signs = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.UserSigns,
                                                          identifier=db_util.UserSigns.is_submitted,
                                                          value=False,
                                                          get_type='many')
        if signs:
            bot.send_message(chat_id=chat_id,
                             text='новые подписки:',
                             reply_markup=key_util.create_reply_keyboard([commands.back]))
            thread = threading.Thread(target=send_signs_async, args=(signs, bot, chat_id))
            thread.start()

        else:
            bot.send_message(chat_id=chat_id,
                             text='На данный момент новые подписки отсутствуют\nожидайте...',
                             reply_markup=key_util.create_reply_keyboard([commands.back]))


def notify_admins(bot: telebot.TeleBot):
    admins = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.AdminAccounts,
                                                       all_objects=True)
    admin_ids = [admin.chat_id for admin in admins]
    print(admin_ids)
    markup = key_util.create_reply_keyboard([commands.new_signs])
    for admin_id in admin_ids:

        try:
            bot.send_message(chat_id=admin_id,
                             text='Появились новые подписки!',
                             reply_markup=markup)
        except Exception as e:
            ic(type(e))
            continue


def send_signs_async(signs, bot, chat_id):
    for payment in signs:
        if isinstance(payment, db_util.UserSigns):
            bot.send_photo(chat_id=chat_id,
                           photo=payment.photo_id,
                           caption=payment.username,
                           reply_markup=key_util.get_inline_admin_submit_cancel(payment.order_id))


# region callback handling
def callback_select_submit_or_cancel(call: telebot.types.CallbackQuery, bot: telebot.TeleBot):
    if isinstance(call.message, telebot.types.Message):
        ic('hello')
        message = call.message
        useful_methods.admin_account_verification(message=message, bot=bot)
        # SELECT SUBMIT OR CANCEL
        if key_util.inline_submit in call.data:
            useful_methods.replace_call_data(call)
            submit_or_cancel_payment.submit_payment_call(call=call, bot=bot)

        elif key_util.inline_cancel in call.data:
            useful_methods.replace_call_data(call)
            submit_or_cancel_payment.cancel_payment_call(call=call, bot=bot)
