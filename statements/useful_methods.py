import random
import string

import telebot

import commands
from statements.start_menu import start_menu
from utils import db_util, key_util


def go_to_main_cabinet(message, bot):
    message.text = commands.start_menu
    start_menu.handle_message(message, bot)


def id_from_message(message: telebot.types.Message) -> int:
    """get chat id from message -> message.text.id, returns int or None"""
    assert message.chat.id
    chat_id = message.chat.id
    return chat_id


def id_from_user(from_user: telebot.types.User):
    """get chat id using from_user object -> message.text.id, returns int or None"""
    assert from_user.id
    chat_id = from_user.id
    return chat_id


def create_client_cabinet(message: telebot.types.Message):
    chat_id = id_from_message(message)
    client = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.Clients,
                                                       identifier=db_util.Clients.chat_id,
                                                       value=chat_id)
    if message.from_user and chat_id and client is None:
        free_tries = 5
        if isinstance(client, db_util.Clients) and client.free_tries is not None:
            free_tries = 5
        db_util.write_obj_to_table(table_class=db_util.Clients,
                                   identifier=db_util.Clients.chat_id,
                                   value=chat_id,  # start write client
                                   chat_id=chat_id,
                                   free_tries=free_tries)


def admin_account_verification(message: telebot.types.Message, bot: telebot.TeleBot):
    """check is it really admin, or send to choosing profile"""
    chat_id = id_from_message(message)
    if not db_util.get_from_db_eq_filter_not_editing(table_class=db_util.AdminAccounts,
                                                     identifier=db_util.AdminAccounts.chat_id,
                                                     value=chat_id):
        # go to client cabinet
        go_to_main_cabinet(message, bot)


def replace_call_data(call: telebot.types.CallbackQuery):
    inline_symbols = key_util.inline_symbols
    for inline_symbol in inline_symbols:
        if inline_symbol in call.data:
            call.data = call.data.replace(inline_symbol, '')


def rand_string(str_length):
    letters = string.ascii_letters
    st = ''
    st = st.join(random.choice(letters) for i in range(str_length))
    return st


def rand_num(n_min, n_max):
    number = random.randint(n_min, n_max)
    return number
