import yt_dlp
import time
import sys

link = input('Введите ссылку: ').strip()

if not link:
    raise ValueError('Ссылка не может быть пустой!')


DEFAULT_TIMEOUT = 10
MAX_RETRIES = 3
RETRY_DELAY = 5
DOWNLOAD_SPEED = 204800

save_option = {
    "format": "best[ext=mp4]/best",
    "outtmpl": "%(title)s.%(ext)s",
    "noplaylist": True,
    "progress_hooks": [lambda d: print(f"\r{d['progress']:.2f}% ({d['_percent_str']})", end='') if d['status'] == 'downloading' else None],
    "fragment_retries": 5,
    "socket_timeout": DEFAULT_TIMEOUT,
    "download_rate_limit": DOWNLOAD_SPEED,
}

for attempt in range(MAX_RETRIES):
    try:
        with yt_dlp.YoutubeDL(save_option) as ydl:
             ydl.download([link])
             print("\nЗагрузка завершена!")
             break
    except yt_dlp.utils.DownloadError as e:
        print(f"\nОшибка загрузки (попытка {attempt + 1}/{MAX_RETRIES}): {e}")
    except ConnectionResetError as e:
         print(f"\nОшибка сети (попытка {attempt + 1}/{MAX_RETRIES}): Соединение разорвано сервером. {e}")
    except ValueError as e:
        print(f"\nОшибка: {e}")
    except Exception as e:
        print(f"\nНепредвиденная ошибка (попытка {attempt + 1}/{MAX_RETRIES}): {e}")
        sys.exit(1)
    else:
            break
    time.sleep(RETRY_DELAY)

else:
    print(f'\nСкачивание не удалось после {MAX_RETRIES} попыток.')
