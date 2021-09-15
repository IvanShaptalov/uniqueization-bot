import telebot
from icecream import ic

import commands
import config_interpreter
from statements import useful_methods
from utils import uniquezation_util, db_util, key_util


def handle_message(message: telebot.types.Message, bot: telebot.TeleBot):
    if isinstance(message, telebot.types.Message):
        chat_id = useful_methods.id_from_message(message)
        if message.text == commands.purchase_func:
            bot.send_message(chat_id=chat_id,
                             text='Отправьте {} грн на указанную карту:\n<b>{}</b>\n'
                                  'после отправьте скриншот для подключения услуги на месяц'.
                             format(config_interpreter.total_cost,
                                    config_interpreter.card),
                             parse_mode='html',
                             reply_markup=key_util.remove_keyboard())

