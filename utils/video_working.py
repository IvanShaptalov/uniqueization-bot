from moviepy.video.io.VideoFileClip import VideoFileClip

from utils.file_util import *
import moviepy.editor as mp

# to ubuntu
input_filename = 'src.mp4'
input_audio = 'src.mp3'
output_filename = 'out.mp4'


def change_video(video_file):
    delete_video_files()
    save_file(video_file, input_filename)
    ic('main file saved', input_filename)
    del video_file

    result_path = handle_video(input_filename)
    ic('get result path', result_path)
    return result_path


def handle_video(path):
    save_audio(input_filename, input_audio)

    out_path = unite_audio_video(audio_path=input_audio,
                                 video_path=input_filename)
    ic('out created', out_path)
    ic('try delete main file')
    try:
        delete_file(path)
        ic('deleted')
    except OSError as e:
        ic(e)
        ic('exception while main file deleting')
    ic('deleted or not')

    return out_path


def save_audio(src_path, result_path):
    ic('save audio')
    video = mp.VideoFileClip(src_path)
    assert isinstance(video, VideoFileClip)
    if video.audio:
        ic('audio exist')
        audio = video.audio
        # Replace the parameter with the location along with filename
        ic("!saving audio file!")
        audio.write_audiofile(result_path, verbose=False, logger=None)
        audio.close()
        ic('audio saved and closed')
    video.close()
    ic('video closed')

    del video


def unite_audio_video(audio_path, video_path):
    try:
        audio = mp.AudioFileClip(audio_path)
    except OSError as e:
        print(type(e))
        return video_path
    video1 = mp.VideoFileClip(video_path)
    final = None
    try:
        final = video1.set_audio(audio)
        ic("!writing video file!")
        final.write_videofile(output_filename, logger=None)
        ic(type(final))
        final.close()
        video1.close()
    except Exception as e:
        ic(type(e), e)
        if final:
            final.close()
        if video1:
            video1.close()
        if audio:
            audio.close()
    return output_filename


def delete_video_files():
    ic('delete files')
    try:
        delete_file(input_filename)
        delete_file(input_audio)
        delete_file(output_filename)
    except OSError as e:
        ic(type(e), e)
        ic('not deleted or not exist: ', input_filename, input_audio, output_filename)
