from telebot import types


def create_reply_keyboard(*titles, is_resize: bool = True, row_width: int = 1, request_contact=None):
    """@:param args - button titles"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=is_resize, row_width=row_width)
    for title in titles[0]:
        button = types.KeyboardButton(title, request_contact=request_contact)
        markup.add(button)

    return markup


def create_inline_keyboard(row_width: int = 1, switch_inline_query_current_chat=None, callback_data=False,
                           **title_to_data):
    markup = types.InlineKeyboardMarkup(row_width=row_width)
    for title, data in title_to_data.items():
        inline_button = types.InlineKeyboardButton(switch_inline_query_current_chat=switch_inline_query_current_chat,
                                                   text=title,
                                                   callback_data=data if callback_data else None)
        markup.add(inline_button)
    return markup


def remove_keyboard():
    markup = types.ReplyKeyboardRemove()
    return markup


inline_submit = 'submit'
inline_cancel = 'cancel'
inline_symbols = [inline_cancel, inline_submit]


def get_inline_admin_submit_cancel(payment_id):
    markup = types.InlineKeyboardMarkup(row_width=1)
    submit = types.InlineKeyboardButton(text='Подтвердить подписку', callback_data=inline_submit + str(payment_id))
    cancel = types.InlineKeyboardButton(text='Отказать в подтверждении', callback_data=inline_cancel + str(payment_id))
    markup.add(submit, cancel)
    return markup
