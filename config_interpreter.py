import configparser

config = configparser.ConfigParser()
config.read("config.ini")
BOT_TOKEN = config['Bot']['bot_token']

alchemy_db_path = config['DataBase']['path_alchemy_local']

card = config['Money']['card']
total_cost = config['Money']['total_cost']
