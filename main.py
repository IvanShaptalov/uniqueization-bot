from datetime import datetime

from bot_engine import delete_expired, start_bot_work
from utils import db_util
from utils.uniquezation_util import edit_queue

if __name__ == '__main__':
    db_util.create_db()
    delete_expired(today=datetime.now())
    edit_queue(-1, True)
    start_bot_work()
