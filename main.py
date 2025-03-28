from pathlib import Path
from config import debug, logger, TOKEN, CAMERA_FOLDER, PATH, DAYS_BEFORE_CLEANING, RUN_IN_LOOP, DATE_FROM
import datetime
from time import sleep
import yadisk
import json

DOWNLOADED_FILES_LIST_FILE_NAME = 'downloaded_files.json'


def start_downloading_in_loop():
    while True:
        if debug:
            start_downloading()
        else:
            try:
                start_downloading()
            except Exception as ex:
                logger.error(f'При загрузке файлов возникла ошибка: {ex}')
        sleep(10)


def start_downloading():
    yd = yadisk.YaDisk(token=TOKEN)

    if not yd.check_token():
        logger.error('Токен отклонён')
        raise 'check token!'

    catalog = photo_catalog()
    file_list = read_downloaded_file_list()
    date_for_deletion = datetime.date.today() - datetime.timedelta(days=DAYS_BEFORE_CLEANING)

    for mediafile in yd.listdir(CAMERA_FOLDER):
        media_type = mediafile.FIELDS.get('media_type', '')
        mediafile_time = mediafile.FIELDS.get('photoslice_time')
        if not mediafile_time:
            mediafile_time = mediafile.FIELDS.get('created')
        if mediafile_time and mediafile_time.date() < DATE_FROM:
            continue
        if media_type not in ('image', 'video'):
            continue

        file_name = mediafile.FIELDS.get('name', '')

        is_downloaded = file_name in file_list
        if not is_downloaded:
            try:
                yd.download(mediafile.FIELDS.get('path', ''), catalog + file_name)
                file_list.append(file_name)
                is_downloaded = True
                logger.info(f'Загружен файл {file_name}')
            except Exception as ex:
                logger.error(f'Ошибка загрузки файла {file_name} по причине: {ex}')

        modified = mediafile.FIELDS.get('modified')
        if is_downloaded and isinstance(modified, datetime.datetime) and modified.date() < date_for_deletion:
            yd.remove(path=mediafile.FIELDS.get('path'), permanently=True)
            logger.info(f'Файл {file_name} удалён с диска')

    write_downloaded_file_list(file_list)


def photo_catalog() -> str:
    catalog = PATH
    if not isinstance(catalog, str):
        catalog = ''
    catalog = catalog.replace('\\', '/')
    if catalog[-1] != '/':
        catalog += '/'
    Path(catalog).mkdir(parents=True, exist_ok=True)
    return catalog


def read_downloaded_file_list() -> list:
    try:
        open(DOWNLOADED_FILES_LIST_FILE_NAME, 'r')
    except FileNotFoundError:
        write_downloaded_file_list([])

    file_list = []
    with open(DOWNLOADED_FILES_LIST_FILE_NAME, 'r') as f:
        file_list = json.load(f)
    return file_list


def write_downloaded_file_list(file_list: list):
    with open(DOWNLOADED_FILES_LIST_FILE_NAME, 'w+') as f:
        json.dump(obj=file_list, fp=f, sort_keys=True, indent=4)


if __name__ == '__main__':
    if RUN_IN_LOOP:
        logger.info('Начата загрузка файлов в цикле...')
        start_downloading_in_loop()
    else:
        logger.info('Загрузка файлов начата...')
        start_downloading()
        logger.info('Загрузка файлов завершена!')
