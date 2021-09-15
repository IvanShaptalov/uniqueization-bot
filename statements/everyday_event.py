from datetime import datetime, timedelta
from threading import Timer

from utils import db_util


def start_event():
    x = datetime.today()
    y = x.replace(day=x.day, hour=1, minute=0, second=0, microsecond=0) + timedelta(days=1)
    delta_t = y - x

    secs = delta_t.total_seconds()
    t = Timer(secs, start_event)

    delete_expired(datetime.now())
    t.start()


def delete_expired(today):
    session = db_util.get_session()
    signs = session.query(db_util.UserSigns).all()
    ids_to_delete = []
    for sign in signs:
        if isinstance(sign, db_util.UserSigns) and sign.expiration_date:
            ex_date = sign.expiration_date
            if ex_date <= today:
                ids_to_delete.append(sign.order_id)
    for id in ids_to_delete:
        db_util.delete_obj_from_table(table_class=db_util.UserSigns,
                                      identifier=db_util.UserSigns.order_id,
                                      value=id)

    print(ids_to_delete)
    session.close()


