import threading
import time
from datetime import datetime

import telebot
from icecream import ic

import commands
import config_interpreter
import constant
from statements import statement_switcher, useful_methods
from statements.everyday_event import start_event, delete_expired
from statements.pass_purchasing import add_order_to_admin
from statements.uniquezation_menu import un_menu_statement
from utils import db_util
from utils.uniquezation_util import edit_queue

error_counter = 0


def start_polling():
    ic('bot started')
    db_util.create_db()
    ic('db created (if not exist)')
    global error_counter
    try:
        bot.polling()
    except Exception as error:
        print(error)
        time.sleep(5)
        ic(error_counter)
        error_counter += 1
        if error_counter > 5:
            print('end')
            return
        start_polling()


bot = telebot.TeleBot(config_interpreter.BOT_TOKEN)


def start_bot_work():
    # text handling (just message,text)
    # user not blocked bot
    @bot.message_handler(content_types=['photo', 'video', 'document'])
    def handle(message):
        if isinstance(message, telebot.types.Message):
            ic('media handling')
            user_st_m = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)
            if user_st_m == constant.Uniquezation.FUNC_PURCHASING:
                add_order_to_admin.save_order(message=message, bot=bot)
            else:
                un_menu_statement.handle_message(message, bot)

    @bot.message_handler(content_types=['text'])
    def answer(message):

        if isinstance(message, telebot.types.Message):
            # select current user statement
            user_st_m = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)

            # select func to call
            func_message = statement_switcher.select_statement_message(user_st_m)

            # create client cabinet if not exist
            useful_methods.create_client_cabinet(message)

            ic(user_st_m, func_message)
            # in argument : [message|callback], bot only, call function
            if func_message:
                func_message(message=message, bot=bot)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_answer(call):
        user_st_c = None
        if call.message:
            message = call.message
            user_st_c = db_util.from_db_get_statement(message.chat.id, message.text, message.from_user.first_name)
        elif call.from_user:
            user_st_c = db_util.from_db_get_statement(call.from_user.id, commands.start_menu, call.from_user.first_name)

        if user_st_c:
            func_callback = statement_switcher.select_statement_callback(user_st_c)
            ic(user_st_c, func_callback)
            # in argument : [message|callback], bot only
            if func_callback:
                func_callback(call=call, bot=bot)

    start_polling()



