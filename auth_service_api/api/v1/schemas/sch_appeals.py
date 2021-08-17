from auth_service_api.models import ElectronicAppeals
from auth_service_api.extensions import ma, db

class ElectronicAppealsSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ElectronicAppeals
        sqla_session = db.session
        load_instance = True
        exclude = ("id", "id_user", "application_id", )
