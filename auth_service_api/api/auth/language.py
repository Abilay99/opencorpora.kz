# -*- coding: utf-8 -*-
# @Time    : 23/01/2021 23:46
# @Author  : Aydar
# @FileName: language.py
# @Software: PyCharm
# @Telegram   ：aydardev


MOBILE_OPERATOR_CALL_CENTER = {
    "Altel": {
        "code": ["700", "708"],
        "call_center": ["611", "+7 (700) 800-08-80"]
    },
    "Tele2": {
        "code": ["707", "747"],
        "call_center": ["116", "+7 (707) 000-07-07"]
    },
    "Kcell Activ": {
        "code": ["701", "702", "775", "778"],
        "call_center": ["116", "3030", "9090", "+7 (727) 258-83-00"]
    },
    "Beeline": {
        "code": ["705", "771", "776", "777"],
        "call_center": ["116", "+7 (727) 350-05-00"]
    }
}

NEMESE = {
    "en": " or ",
    "ru": " или ",
    "kk": " немесе "
}

def except_mobile(code):
    for on, od in MOBILE_OPERATOR_CALL_CENTER.items():
        if code in od['code']:
            return {
                "msg_kk": "Бұл нөмер бұғатталған! Қолданыстағы нөмеріңізді еңгізіңіз немесе"
                + " мобильді операторыңызға(Call-Center: {0}) хабарласыңыз: {1}"
                .format(on, NEMESE['kk'].join(od['call_center'])),
                "msg_ru": "Этот номер заблокирован! Введите свой текущий номер или обратитесь"
                + " к своему оператору(Call-Center: {0}) мобильной связи: {1}"
                .format(on, NEMESE['kk'].join(od['call_center'])),
                "msg_en": "This number is blocked! Enter your current number or"
                + " contact your mobile operator(Call-Center: {0}): {1}"
                .format(on, NEMESE['kk'].join(od['call_center']))
            }

SEND_TYPE_ERR = {"msg_kk": "Сұраныс түрі қате send_type1 тіркелу үшін таңдаңыз send_type2 құпия" +
                 "сөзді қалпына келтіру үшін таңдаңыз",
                 "msg_ru": "demo1",
                 "msg_en": "send type error select send_type1 for register or send_type2 for forgot password"
                 }

UESR_NOT_FIND1 = {
    "msg_kk": "Бұл нөмер тіркелген",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}

UESR_NOT_FIND = {
    "msg_kk": "Бұл нөмер тіркелмеген",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}

REQUIRED_MOBILE_AND_SEND_TYPE = {
    "msg_kk": "send_type мен mobile жазу міндетті",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}

NOT_JSON = {
    "msg_kk": "cіз жіберген type json емес",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}

BLOCK_PHONE_NUMBER = {
    "msg_kk": "hello1",
    "msg_ru": "hello2",
    "msg_en": "your mobile block, try it in three days"
}

SUCCESSFUL_SMS = {
    "msg_kk": "hello1",
    "msg_ru": "hello2",
    "msg_en": "successful send sms"
}

FAILED_SEND_SMS = {
    "msg_kk": "SMS жіберіу сәтсіз болды",
    "msg_ru": "demo1",
    "msg_en": "demo2"
}

REQUIRED_MOBILE_AND_PASSWORD = {
    "msg_kk": "password мен mobile жазу міндетті",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}
REQUIRED_BIN_AND_PASSWORD = {
    "msg_kk": "password пен bin жазу міндетті",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}
LOGIN_FAILED = {
    "msg_kk": "Логин немесе пароль дұрыс емес",
    "msg_ru": "demo1",
    "msg_en": "demo2",
}

VERIFICATION_CODE_ERROR = {
    "msg_kk": "ddd",
    "msg_ru": "ddd",
    "msg_en": "Verification code error",
}

VERIFICATION_CODE_EXPIRED = {
    "msg_kk": "ddd",
    "msg_ru": "ddd",
    "msg_en": "Verification code expired",
}

REQUIRED_VERIFICATION_CODE = {
    "msg_kk": "verification code толтыру міндетті",
    "msg_ru": "please input verification code",
    "msg_en": "please input verification code"
}

REQUIRED_FORM_DATA = {
    "msg_kk": "Missing [first_name, last_name, mobile, username, email, password]",
    "msg_ru": "Missing [first_name, last_name, mobile, username, email, password]",
    "msg_en": "Missing [first_name, last_name, mobile, username, email, password]",
}

USER_IS_REGISTRED = {
    "msg_kk": "Бұндай қолданушы тіркеліп қойылған",
    "msg_ru": "Bad credentials",
    "msg_en": "Bad credentials"
}

CREATE_NEW_USER = {
    "msg_kk": "Қолданушы сәтті құрылды",
    "msg_ru": "Қолданушы сәтті құрылды",
    "msg_en": "successful create new user"
}

PASSWORD_NOT_SAME = {
    "msg_kk": "екі пароль бірдей емес",
    "msg_ru": "екі пароль бірдей емес",
    "msg_en": "The two passwords are not the same",
}

PASSWORD_UPDATE = {
    "msg_kk": "Пароль жаңарту сәтті болды",
    "msg_ru": "successful update user password",
    "msg_en": "successful update user password",
}
