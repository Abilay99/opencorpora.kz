# -*- coding: utf-8 -*-
# @Time    : 23/01/2021 22:59
# @Author  : Aydar
# @FileName: mdl_verify_code.py
# @Software: PyCharm
# @Telegram   ：aydardev
from sqlalchemy.dialects.postgresql import UUID, ENUM
from auth_service_api.extensions import db
from auth_service_api.models.helpers import DateTime
import enum
import uuid

class SendTypeEnum(enum.Enum):
    send_type1 = "register"
    send_type2 = "forget"
    send_type3 = "other"


send_type_enum = ENUM(SendTypeEnum, name="send_type_enum")


class TblVerifyCode(db.Model):
    __tablename__ = 'tbl_verify_code'
    id = db.Column(UUID(as_uuid=True), primary_key=True, unique=True, default=uuid.uuid4)
    mobile = db.Column(db.String(10), nullable=False)
    code = db.Column(db.String(4), nullable=False)
    send_type = db.Column(send_type_enum)
    create_time = db.Column(db.DateTime(timezone=True), nullable=False, default=DateTime.now())
    repeat_expire_time = db.Column(db.DateTime(timezone=True), nullable=True, default=None)
    repeat_count = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return "<verify_code %s -> %s>"% self.code % self.mobile 