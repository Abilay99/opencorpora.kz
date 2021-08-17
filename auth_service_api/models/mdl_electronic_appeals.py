from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.dialects.postgresql import UUID
from auth_service_api.extensions import db, pwd_context
from auth_service_api.models.helpers import DateTime
from auth_service_api.models import Users
import uuid

class TblElectronicAppeals(db.Model):
    __tablename__       = 'tbl_electronic_appeals'

    id                  = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    externalRequestId   = db.Column(db.String(14), nullable=False)
    id_user             = db.Column(UUID(as_uuid=True), db.ForeignKey(Users.id), nullable=False)
    application_id      = db.Column(UUID(as_uuid=True), unique=True, nullable=False)
    descreption         = db.Column(db.Text(), nullable=False)
    created_date        = db.Column(db.DateTime(timezone=True), default=DateTime.now())
    updated_date        = db.Column(db.DateTime(timezone=True), default=DateTime.now())
    response_appeal     = db.Column(db.String(255), default=None)

    def __repr__(self):
        return '<TblElectronicAppeals %r>' % self.id_user
