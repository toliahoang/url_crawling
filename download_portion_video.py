import time
import math
from functools import wraps
import yt_dlp
from yt_dlp.utils import download_range_func
import logging
import subprocess
import os
logger = logging.basicConfig(filename='log_file_name.log',level=logging.INFO)


def time_processing(f):
    def wrapped(*args, **kwargs):
        begin = time.time()
        f(*args, **kwargs)
        end = time.time()
        print(f"processing time of {f.__name__} is: {end - begin}")
        logging.info(f"processing time {end - begin}")
        return f(*args, **kwargs)
    return wrapped


def retry(ExceptionToCheck, tries=4, delay=5, backoff=2, logger=None):

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    f(*args, **kwargs)
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
        'force_keyframes_at_cuts': True,
        'format':"mp4",
        "outtmpl": 'video_download/outfile.%(ext)s'
    }
    # with yt_dlp.YoutubeDL(yt_opts) as ydl:
    #     ydl.download(f"{url}")
    try:
        yt_dlp.YoutubeDL(yt_opts).download(f"{url}")
    except Exception as e:
        print(e)
        return False
    else:
        return True




# list_videos = ['https://www.twitch.tv/videos/1959544588',
#                'https://www.twitch.tv/videos/1963260122',
#                'https://www.twitch.tv/videos/1958434416',
#                'https://www.twitch.tv/videos/1962786599',
#                'https://www.twitch.tv/videos/1960683307',
#                'https://www.twitch.tv/videos/1960945044']



@time_processing
def download_list_url(list_videos):
    for url in list_videos:
        download_file(url, "00:00:12", "00:00:59")


def special_character_removal(bad_chars, name_string, n_chars):
    filename, file_extension = os.path.splitext(name_string)
    for i in bad_chars:
        filename = filename.replace(i, '')

    length_filename = min(n_chars,len(filename))
    new_filename = filename[:length_filename]
    filtered_file_name = new_filename + file_extension
    return filtered_file_name


def get_filename(url):
    args = ['yt-dlp','--print','filename',url]
    command = subprocess.list2cmdline(args)
    someFilename = subprocess.getoutput(command)
    return someFilename


def rename_file(name):
    bad_chars = [';', ':', '!', "*", "'", '¼', "#", ".", "]", "[", "ï"]
    # abs_old_path = os.path.abspath(os.path.join(video_download, "new outfile.mp4"))
    # abs_new_path = os.path.abspath(os.path.join(video_download, name))
    name = special_character_removal(bad_chars, name, 110)
    print(name)
    logging.info(f"the orginal filename is: {name}")
    try:
        get_status = os.path.isfile("video_download/outfile.mp4")
    except:
        raise FileNotFoundError("File not found outfile.mp4")
    print("get_status: ",get_status)
    logging.info(f"get_status file exist: {get_status}")
    if get_status:
        os.rename("video_download/outfile.mp4", "video_download/" + name)


def download_and_rename(url):
    os.makedirs("video_download", exist_ok=True)
    download_status = download_file(url, "00:00:12", "00:00:59")
    name = get_filename(url)
    print("download_status: ", download_status)
    logging.info(f"get_download_status: {download_status}")
    if download_status:
        rename_file(name)

list_videos = ['https://www.twitch.tv/videos/1960683307']
download_and_rename(*list_videos)
