from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from auth_service_api.extensions import db, pwd_context
# from sqlalchemy import func
from auth_service_api.models.helpers import DateTime
import uuid
class TblUsers(db.Model):
    __tablename__ = 'tbl_users'
    id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    full_name = db.Column(db.String(255), nullable=False)
    bin = db.Column(db.String(20), unique=True, nullable=False)
    mobile = db.Column(db.String(10), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    _password = db.Column("password", db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True)
    photo = db.Column(db.String, nullable=True)
    update_time = db.Column(db.DateTime(timezone=True), default=DateTime.now(), onupdate=DateTime.now())
    create_time = db.Column(db.DateTime(timezone=True), default=DateTime.now())

    def __init__(self, full_name, bin, mobile, email, password):
        self.full_name = full_name
        self.bin = bin
        self.mobile = mobile
        self.email = email
        self.password = password

    @hybrid_property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = pwd_context.hash(value)

    def __repr__(self):
        return "<Users %s>" % self.full_name
