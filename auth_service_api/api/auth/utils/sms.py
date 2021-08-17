# -*- coding: utf-8 -*-
# @Time    : 2021/1/8 下午1:22
# @Author  : Aydar
# @FileName: sms.py
# @Software: PyCharm
# @Telegram   ：aydardev

from random import choice

from flask_sqlalchemy import model

from auth_service_api.api.auth.utils.smsc_api import SMSC
from auth_service_api.config import SEND_SMS_KZ
from auth_service_api.models import VerifyCode
from auth_service_api.extensions import db

smsc = SMSC()


def generate_code():
    seeds = "1234567890"
    random_str = []
    for i in range(4):
        random_str.append(choice(seeds))
    return "".join(random_str)


def send_mobile(mobile, send_type):
    code = generate_code()
    sms_content = SEND_SMS_KZ + str(code)
    mobile_content = "7" + mobile
    sms_status = smsc.send_sms(mobile_content, sms_content, sender="sms")
    verify_code = VerifyCode.query.filter_by(mobile=mobile, send_type=send_type)\
        .order_by(VerifyCode.id.desc()).first()
    if verify_code is not None:
        verify_code.repeat_count += 1
        db.session.flush()
    elif sms_status[1] == '1':
        code_record = VerifyCode(
            mobile=mobile,
            code=code,
            send_type=send_type
        )
        db.session.add(code_record)
    else:
        return False

    db.session.commit()
    return True
