import time
import math
from functools import wraps
import yt_dlp
from yt_dlp.utils import download_range_func
import logging



logger = logging.basicConfig(filename='log_file_name.log',level=logging.INFO)


def time_processing(f):
    def wrapped(*args, **kwargs):
        begin = time.time()
        f(*args, **kwargs)
        end = time.time()
        print(f"processing time of {f.__name__} is: {end - begin}")
        logging.info(f"processing time {end - begin}")
    return wrapped


def retry(ExceptionToCheck, tries=4, delay=3, backoff=2, logger=None):

    def deco_retry(f):

        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as e:
                    msg = "%s, Retrying in %d seconds..." % (str(e), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    mdelay *= backoff
            return f(*args, **kwargs)

        return f_retry

    return deco_retry


def convert_hhmmss_to_second(time_str):
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + int(s)


@time_processing
@retry(Exception, tries=6)
def download_file(url, start_time_str, end_time_str):
    start_time = int(convert_hhmmss_to_second(start_time_str))
    end_time = int(convert_hhmmss_to_second(end_time_str))

    yt_opts = {
        "ytsearch": True,
        'verbose': True,
        'download_ranges': download_range_func(None, [(start_time, end_time)]),
        'force_keyframes_at_cuts': False,
        'format':"mp4"
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download(f"{url}")




list_videos = ['https://www.twitch.tv/videos/1959544588',
               'https://www.twitch.tv/videos/1963260122',
               'https://www.twitch.tv/videos/1958434416',
               'https://www.twitch.tv/videos/1962786599',
               'https://www.twitch.tv/videos/1960683307',
               'https://www.twitch.tv/videos/1960945044']


@time_processing
def download_list_url(list_videos):
    for url in list_videos:
        download_file(url, "00:00:10", "00:00:60")


download_list_url(list_videos)
