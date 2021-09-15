import threading

import telebot

import commands
from statements import useful_methods
from utils import uniquezation_util, db_util, key_util


def async_video_starter(file, bot):
    print('is real')
    # uniquezation_util.make_video_unique(file, bot)
    thread = threading.Thread(target=uniquezation_util.make_video_unique, args=[file, bot])
    thread.start()


def handle_unique_in_sign(file, client, chat_id, bot):
    if file.content_type == 'video':
        tries_cancellation(text='видео поставлено в очередь на обработку!',
                           client=client,
                           chat_id=chat_id,
                           bot=bot)
        async_video_starter(file, bot)

    elif file.content_type == 'photo':
        tries_cancellation(text='фото поставлено в очередь на обработку!',
                           client=client,
                           chat_id=chat_id,
                           bot=bot)
        uniquezation_util.make_photo_unique(file, bot)

    else:

        bot.send_message(chat_id=chat_id,
                         text='Вы должны отправлять файлы исключительно в формате фото или видео!')


def handle_unique_in_tries(file, client, chat_id, bot):
    if file.content_type == 'video':
        tries_cancellation(text='видео поставлено в очередь на обработку!\n'
                                'осталось бесплатных попыток: {}',
                           client=client,
                           chat_id=chat_id,
                           bot=bot)
        async_video_starter(file, bot)
    elif file.content_type == 'photo':
        tries_cancellation(text='фото поставлено в очередь на обработку!\n'
                                'осталось бесплатных попыток: {}',
                           client=client,
                           chat_id=chat_id,
                           bot=bot)
        uniquezation_util.make_photo_unique(file, bot)
    else:

        bot.send_message(chat_id=chat_id,
                         text='Вы должны отправлять файлы исключительно в формате фото или видео!')


def tries_expired(chat_id, bot):
    markup = key_util.create_reply_keyboard([commands.purchase_func])
    bot.send_message(chat_id=chat_id,
                     text='Ваши попытки закончились, оплатите пакет услуг на месяц\n'
                          'для дальнейшего использования функции уникализации',
                     reply_markup=markup)


def handle_message(file: telebot.types.Message, bot: telebot.TeleBot):
    if isinstance(file, telebot.types.Message):
        chat_id = useful_methods.id_from_message(file)
        client = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.Clients,
                                                           identifier=db_util.Clients.chat_id,
                                                           value=chat_id)
        sign = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.UserSigns,
                                                         identifier=db_util.UserSigns.client_chat_id,
                                                         value=chat_id)
        if isinstance(sign, db_util.UserSigns) and sign.is_submitted is True:
            handle_unique_in_sign(file, client, chat_id, bot)

        elif isinstance(client, db_util.Clients) and (client.free_tries > 0):
            handle_unique_in_tries(file, client, chat_id, bot)

        else:
            tries_expired(chat_id, bot)


def tries_cancellation(text, client, chat_id, bot):
    if client.free_tries != 0:
        client.free_tries -= 1
    db_util.write_obj_to_table(table_class=db_util.Clients,
                               identifier=db_util.Clients.chat_id,
                               value=chat_id,
                               free_tries=client.free_tries)

    bot.send_message(chat_id=chat_id,
                     text=text.format(client.free_tries))
