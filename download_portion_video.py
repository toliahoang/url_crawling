import time
import math
from functools import wraps
import yt_dlp
from yt_dlp.utils import download_range_func


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


@retry(Exception, tries=4)
def download_file(url, start_time_str, end_time_str):
    start_time = int(convert_hhmmss_to_second(start_time_str))
    end_time = int(convert_hhmmss_to_second(end_time_str))

    yt_opts = {
        "ytsearch": True,
        'verbose': True,
        'download_ranges': download_range_func(None, [(start_time, end_time)]),
        'force_keyframes_at_cuts': True,
        'format':"mp4"
    }
    with yt_dlp.YoutubeDL(yt_opts) as ydl:
        ydl.download(f"{url}")


download_file('https://www.twitch.tv/videos/1961098587', "00:30:00", "00:30:10")

