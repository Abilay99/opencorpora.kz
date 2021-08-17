"""Default configuration

Use env var to override
"""
import os
import datetime
ENV = os.getenv("FLASK_ENV")
DEBUG = ENV == "development"
SECRET_KEY = os.getenv("SECRET_KEY")


BASE_ROOT = os.path.dirname(os.path.abspath(__file__))
SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI")
SQLALCHEMY_TRACK_MODIFICATIONS = False
STATIC_ROOT = os.path.join(BASE_ROOT, 'static')
MEDIA_ROOT = os.path.join(BASE_ROOT, 'media')
TIME_ZONE = os.getenv("TZ")
IMG_ALLOWED_EXTENSIONS = set(['jpeg', 'png', 'gif', 'tiff', 'rgb', 'pbm', 'pgm',
                              'ppm', 'rast', 'xbm', 'bmp', 'webp', 'exr'])
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(days=10)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ["access", "refresh"]

REGEX_MOBILE_KZ = "^7[740][0125678][0-9][0-9][0-9][0-9][0-9][0-9][0-9]"
SEND_SMS_KZ = "QAZNA ONLINE, \nҚұрметті Қолдануші: \nСізге жіберлген код:"
SEND_SMS_RU = "QAZNA ONLINE, \nҚұрметті Қолдануші: \nСізге жіберлген код:"
