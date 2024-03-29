from environs import Env
import loguru

logger = loguru.logger
logger.add('Logs/yd.log', format='{time} {level} {message}', rotation='512 KB', compression='zip')

env = Env()
env.read_env()
TOKEN = env.str('TOKEN_YD')
PATH = env.str('PATH_YD')
DAYS_BEFORE_CLEANING = env.int('DAYS_BEFORE_CLEANING')
RUN_IN_LOOP = env.int('RUN_IN_LOOP')
DATE_FROM = env.date('DATE_FROM')

debug = False

CAMERA_FOLDER = 'disk:/Фотокамера'