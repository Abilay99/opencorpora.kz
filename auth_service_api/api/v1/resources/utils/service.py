# region libs
from auth_service_api.config import STATIC_ROOT, MEDIA_ROOT, IMG_ALLOWED_EXTENSIONS
import os
import pandas as pd
import datetime
from flask import request
from werkzeug.utils import secure_filename
import imghdr
import shutil
# endregion

pathImage = os.path.join(MEDIA_ROOT, 'image')
pathTemp = os.path.join(STATIC_ROOT, 'tmp')

def _create_new_folder(local_dir):
    new_path = local_dir
    if not os.path.exists(new_path):
        os.makedirs(new_path)
    return new_path


def _img_allowed_file(file):
    return imghdr.what(file=file) in IMG_ALLOWED_EXTENSIONS


def _file_clear(filename):
    if '.' in filename:
        s = ''
        for i in filename.rsplit('.', 1)[1].lower():
            if i.isalpha():
                s += i

        return _get_unique_string() + '.' + s

    return False


def _get_unique_string(get_password_len=12):
    import time
    import random
    import hashlib

    chars = 'abcdefghijklnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'
    length, password = get_password_len, ''

    for i in range(length):
        password += random.choice(chars)

    # TODO: Это адская дичь! =)
    if get_password_len != 12:
        return password

    hex_dig = hashlib.sha256((password + str(round(time.time() * 1000))).encode('utf-8')).hexdigest()

    return hex_dig


class UploadFile:
    @staticmethod
    def rs_file(values: list = False, remove: bool = False):

        if values and type(values) == list:
            if remove is True:
                for value in values:
                    url_file = pathImage + '/' + value[0:2] + '/' + value[2:4] + '/' + value[4:6] + '/' + value
                    if os.path.isfile(url_file):
                        os.remove(url_file)
                        shutil.rmtree(pathImage + '/' + value[0:2], ignore_errors=True)
                return True
            else:
                result = {}
                for value in values:
                    file = request.files.get(value)
                    if file and file.filename != '' and _img_allowed_file(file):
                        f = _file_clear(secure_filename(f'{file.filename.encode("utf-8")}'))
                        #  TODO: Если нету папки media то ошибка появляется
                        if not os.path.exists(pathImage + '/' + f[0:2]):
                            os.mkdir(pathImage + '/' + f[0:2])
                        if not os.path.exists(pathImage + '/' + f[0:2] + '/' + f[2:4]):
                            os.mkdir(pathImage + '/' + f[0:2] + '/' + f[2:4])
                        if not os.path.exists(pathImage + '/' + f[0:2] + '/' + f[2:4] + '/' + f[4:6]):
                            os.mkdir(pathImage + '/' + f[0:2] + '/' + f[2:4] + '/' + f[4:6])

                        file.save(os.path.join(pathImage + '/' + f[0:2] + '/' + f[2:4] + '/' + f[4:6], f))
                        result[value] = f
                return result

        return False

# methods for add days to received date
def add_days(date, days: int):
    if type(date) is str:
        current_date = datetime.datetime.fromisoformat(date)
    elif type(date) is datetime:
        current_date = date
    else:
        return date
    while days > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5:
            # sunday = 6
            continue
        days -= 1
    return current_date

# classes for name service included with excel doc
class ExtractWithExcel():
    __filepath: str()
    __filename: str()

    def __init__(self, filename):
        self.__filepath = os.path.join(pathTemp, filename)
        self.__filename = filename[:filename.rfind('.')]
        self.data = self.toData(self.__filepath)

    def toData(self, filepath: str):
        return pd.read_excel(self.__filepath, sheet_name=0, header=0)

    def getNameWithCode(self, code: int):
        for i in range(self.data.shape[0]):
            if int(self.data.iloc[i, [self.data.shape[1] - 1]]) == code:
                return {
                    "en": self.data['en_name'][i],
                    "ru": self.data['ru_name'][i],
                    "kz": self.data['kk_name'][i]
                }
