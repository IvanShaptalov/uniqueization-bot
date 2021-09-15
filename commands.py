import constant

# start
start_menu = '/start'
back = 'назад'
purchase_func = 'оплатить услугу'
new_signs = 'новые подписки'

# add command -> add statement -> add command-statement -> statement switcher -> add function


def select_statement_via_present_command(command_present):
    switcher = {
        # client
        start_menu: constant.StartMenu.START_MENU,
        back: constant.StartMenu.START_MENU,
        purchase_func: constant.Uniquezation.FUNC_PURCHASING,
        new_signs: constant.Admin.SHOW_NEW_SIGNS
    }
    return switcher.get(command_present)
