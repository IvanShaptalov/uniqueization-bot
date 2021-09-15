import constant
from statements.admin_orders import signs
from statements.pass_purchasing import purchase_func_statement
from statements.start_menu import start_menu


def select_statement_message(statement):
    switcher = {
        constant.StartMenu.START_MENU: start_menu.handle_message,
        constant.Uniquezation.FUNC_PURCHASING: purchase_func_statement.handle_message,
        constant.Admin.SHOW_NEW_SIGNS: signs.handle_message
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func


def select_statement_callback(statement):
    switcher = {
        constant.Admin.SHOW_NEW_SIGNS: signs.callback_select_submit_or_cancel
    }
    try:
        message_func = switcher.get(statement)
        return message_func
    except AttributeError:
        message_func = switcher.get('default value')
        return message_func