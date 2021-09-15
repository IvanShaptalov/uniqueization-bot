import time

import telebot
from icecream import ic

from statements import useful_methods
from utils import photo_working, video_working, db_util
from utils.file_util import delete_file
from utils.photo_working import change_photo

megabyte_20 = 1048576 * 20


# region work with video
def make_video_unique(message_with_video: telebot.types.Message, bot: telebot.TeleBot):
    # change video and create queue
    """video uniqueization process"""
    # threading.Thread(target=_async_queue, args=[message_with_video, bot]).start()
    _async_queue(message_with_video, bot)


def _async_queue(message_with_video, bot):
    try:
        chat_id = useful_methods.id_from_message(message_with_video)
        queue = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.VideoQueue,
                                                          identifier=db_util.VideoQueue.order_id,
                                                          value=1)
        if isinstance(queue, db_util.VideoQueue):
            ic(queue.is_free)
            if queue.is_free:
                video_starter(message_with_video, bot)
            else:
                time.sleep(int(queue.in_queue) * 5)
                print('waiting...')
                make_video_unique(message_with_video, bot)
    except Exception as e:
        print(type(e), 'error with handling video: ', e)
        edit_queue(-1, True)


def get_extension(file_path, type):
    """@type - select 'video' or 'photo' """
    file_ex = file_path[::-1]
    if '.' in file_ex:
        index = file_ex.index('.') + 1
        file_ex = file_ex[0:index]
        file_ex = file_ex[::-1]
        return file_ex
    elif type == 'photo':
        return '.png'
    elif type == 'video':
        return '.mp4'
    else:
        raise AttributeError('maybe you entered something else than \'photo\' or \'video\'')


def edit_queue(count: int, is_free: bool) -> bool:
    """@parameter count to orders in queue"""
    queue = db_util.get_from_db_eq_filter_not_editing(table_class=db_util.VideoQueue,
                                                      identifier=db_util.VideoQueue.order_id,
                                                      value=1)
    if isinstance(queue, db_util.VideoQueue):
        new_count = (int(queue.in_queue) + count)
        if new_count < 0:
            new_count = 0
        db_util.edit_obj_in_table(table_class=db_util.VideoQueue,
                                  identifier=db_util.VideoQueue.order_id,
                                  value=1,
                                  is_free=is_free,
                                  in_queue=new_count)
        ic(is_free, new_count)
        return True
    return False


def video_starter(message_with_video: telebot.types.Message, bot: telebot.TeleBot):
    if edit_queue(+1, False):

        ic(message_with_video)
        print('video')
        chat_id = useful_methods.id_from_message(message_with_video)
        video = get_video_from_message(message_with_video, bot)
        if video is None:
            bot.send_message(chat_id=chat_id,
                             text='Размер файла превышает 20 мб!')
            return
        d_video = bot.download_file(video.file_path)
        # Working on video
        path = video_working.change_video(d_video)
        ic(path)
        del d_video
        if path:
            try:
                with open(path, 'rb') as video:
                    bot.send_video(chat_id=chat_id,
                                   data=video,
                                   caption='Готово!')
                    ic('sended', path)
                ic('try delete out')
                delete_file(path)
                ic('succesfully deleted', path)
            except Exception as e:
                ic(e)
            finally:
                edit_queue(-1, True)


# region work with photo
def make_photo_unique(message_with_photo: telebot.types.Message, bot: telebot.TeleBot):
    """photo uniqueization process"""
    photo_starter(bot=bot, file_photo=message_with_photo)


def photo_starter(bot: telebot.TeleBot,
                  file_photo: telebot.types.Message):
    file_ex = None
    d_file = None

    print(file_photo)
    ic('work with photo *async*')
    photo = file_photo.photo[-1]
    chat_id = useful_methods.id_from_message(file_photo)
    ic(photo)
    result = get_photo_from_message(photo, bot)
    if result is None:
        bot.send_message(chat_id=chat_id,
                         text='Размер файла превышает 20 мб!')
        return
    if isinstance(result, telebot.types.File):
        d_file = bot.download_file(file_path=result.file_path)

    file_ex = get_extension(result.file_path, 'photo')
    path = change_photo(d_file, file_ex)
    del d_file
    try:
        with open(path, 'rb') as send_photo:
            bot.send_photo(chat_id=chat_id,
                           photo=send_photo,
                           caption='Готово')
            delete_file(path)
            ic('deleted')
    except Exception as e:
        ic(type(e))
        delete_file(path)
        print('try delete')
    finally:
        print('deleted or not')
        # notify that query is free


# endregion


# region helping methods
def get_photo_from_message(file_photo, bot):
    if isinstance(file_photo, telebot.types.PhotoSize):
        if file_photo.file_size <= megabyte_20:
            print('all is ok')
            result = bot.get_file(file_photo.file_id)
            return result
    return None


def get_video_from_message(file_video: telebot.types.Message, bot):
    video = file_video.video
    if isinstance(video, telebot.types.Video):
        if video.file_size <= megabyte_20:
            print('all is ok')
            result = bot.get_file(video.file_id)
            return result
    return None

# endregion
