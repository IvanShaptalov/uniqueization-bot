from icecream import ic
from sqlalchemy import Integer, Column, String, BOOLEAN, create_engine, DATETIME
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import commands
import config_interpreter
import constant

path_alchemy_local = config_interpreter.alchemy_db_path

Base = declarative_base()


# region db engine
def create_db():
    engine_db = get_engine_by_path(engine_path=path_alchemy_local)
    Base.metadata.create_all(bind=engine_db)


def get_session():
    engine_session = get_engine_by_path(engine_path=path_alchemy_local)
    session_creator = sessionmaker(bind=engine_session)
    session = session_creator()
    return session


def get_engine_by_path(engine_path):
    """put db path to create orm engine"""
    # --echo back to true, show all sqlalchemy debug info
    engine_path = create_engine(engine_path, echo=False)
    return engine_path


# endregion


# region tables
class UserStatements(Base):
    __tablename__ = "user_statements"

    chat_id = Column('chat_id', Integer, unique=True, primary_key=True)
    statement = Column('statement', String, unique=False)
    username = Column('username', String, unique=False)

    def __repr__(self):
        return '{}{}{}'.format(self.chat_id, self.statement, self.username)


# endregion


class Clients(Base):
    __tablename__ = 'clients'

    chat_id = Column('chat_id', Integer, unique=True)
    client_id = Column('client_id', Integer, unique=True, primary_key=True, autoincrement=True)
    free_tries = Column('free_tries', Integer, unique=False)

    def __eq__(self, other):
        if isinstance(other, Clients):
            return self.__str__() == other.__str__()

    def __str__(self):
        return 'cl_id = {}chat_id= {} unique code={}'.format(self.client_id,
                                                             self.chat_id,
                                                             self.unique_code)


class VideoQueue(Base):
    __tablename__ = "video_queue"

    order_id = Column('order_id', Integer, unique=True, primary_key=True, autoincrement=True)
    is_free = Column('is_free', BOOLEAN, unique=False)
    in_queue = Column('in_queue', Integer, unique=False)


class AdminAccounts(Base):
    __tablename__ = "admin_accounts"

    chat_id = Column('chat_id', Integer, unique=True, primary_key=True)
    first_name = Column('first_name', String, unique=False)
    last_name = Column('last_name', String, unique=False)


class UserSigns(Base):
    __tablename__ = 'user_signs'

    order_id = Column('order_id', Integer, unique=True, primary_key=True, autoincrement=True)
    photo_id = Column('photo_id', String, unique=False)
    username = Column('username', String, unique=False)
    client_chat_id = Column('client_chat_id', Integer, unique=False)
    is_submitted = Column('is_submitted', BOOLEAN, unique=False)
    expiration_date = Column('expiration_date', DATETIME, unique=False)


# region crud methods
def from_db_get_statement(chat_id, message_text, first_name):
    chat_id = chat_id
    message_is_command = commands.select_statement_via_present_command(message_text)
    # check for new user
    session = get_session()
    # if user not created
    user = session.query(UserStatements).filter_by(chat_id=chat_id).first()
    if not (user and user.statement):
        # user creating
        session.query(UserStatements).filter_by(chat_id=chat_id).delete()
        session.commit()
        user = UserStatements()
        # user created
        user.statement = constant.StartMenu.START_MENU
        user.chat_id = chat_id
        user.username = first_name
        session.add(user)
        command_st = user.statement
    else:
        assert isinstance(user, UserStatements)
        command_st = user.statement

    # get statement
    if message_is_command:
        command_st = message_is_command
        assert isinstance(user, UserStatements)
        #  must update statement
        user.statement = command_st
    session.commit()
    session.close()

    return command_st


# endregion


# region abstract get_from_db
def get_from_db_in_filter(table_class, identifier, value, get_type):
    """:param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'"""
    many = 'many'
    one = 'one'
    session = get_session()
    if get_type == one:
        obj = session.query(table_class). \
            filter(identifier.contains(value)).first()
        session.close()
        return obj
    elif get_type == many:
        objs = session.query(table_class). \
            filter(identifier.contains(value)).all()
        session.close()
        return objs
    session.close()


def get_from_db_eq_filter_not_editing(table_class, identifier=None, value=None, get_type='one', eq: bool = True,
                                      all_objects: bool = None):
    """WARNING! DO NOT USE THIS OBJECT TO EDIT DATA IN DATABASE! IT ISN`T WORK!
    USE ONLY TO SHOW DATA...
    :param table_class - select table
    :param identifier - select filter column
    :param value - enter value to column
    :param get_type - string 'many' or 'one'
    :param eq - choose the value equals to column or not
    :param all_objects - return all rows from table"""
    many = 'many'
    one = 'one'
    session = get_session()
    if all_objects is True:
        objs = session.query(table_class).all()
        session.close()
        return objs
    if get_type == one:
        if eq:
            obj = session.query(table_class). \
                filter(identifier == value).first()
        else:
            obj = session.query(table_class). \
                filter(identifier != value).first()

        session.close()
        return obj
    elif get_type == many:
        if eq:
            objs = session.query(table_class). \
                filter(identifier == value).all()
        else:
            objs = session.query(table_class). \
                filter(identifier != value).all()

        session.close()
        return objs
    session.close()


# endregion


# region abstract write


def write_obj_to_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get obj
    session = get_session()
    is_new = False
    if identifier:
        tab_obj = session.query(table_class).filter(identifier == value).first()
    else:
        tab_obj = table_class()
        is_new = True

    # is obj not exist in db, we create them
    if not tab_obj:
        tab_obj = table_class()
        is_new = True
    for col_name, val in column_name_to_value.items():
        tab_obj.__setattr__(col_name, val)
    # if obj created jet, we add his to db
    if is_new:
        session.add(tab_obj)
    # else just update
    session.commit()
    session.close()


# endregion


# region abstract edit
# test this method
def edit_obj_in_table(table_class, identifier=None, value=None, **column_name_to_value):
    """column name to value must be exist in table class in columns"""
    # get bj
    session = get_session()
    tab_obj = session.query(table_class).filter(identifier == value).first()

    if tab_obj:
        for col_name, val in column_name_to_value.items():
            tab_obj.__setattr__(col_name, val)
    session.commit()
    session.close()


# endregion


# region abstract delete from db
def delete_obj_from_table(table_class, identifier=None, value=None):
    """column name to value must be exist in table class in columns"""
    session = get_session()
    result = session.query(table_class).filter(identifier == value).delete()
    ic('affected {} rows'.format(result))
    session.commit()
    session.close()


# endregion


# region arithmetics
def get_count(table_class):
    session = get_session()
    rows = session.query(table_class).count()
    session.close()
    return rows


def get_first(table_class):
    # work on func min
    session = get_session()
    row = session.query(table_class).first()
    session.close()
    return row

# endregion
