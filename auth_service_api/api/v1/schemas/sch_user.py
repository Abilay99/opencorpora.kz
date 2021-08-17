from auth_service_api.models import Users
from auth_service_api.extensions import ma, db


class UserFullSchema(ma.SQLAlchemyAutoSchema):
    password = ma.String(load_only=True, required=True)

    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("_password",)


class UserPutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("_password", "active", "id", "create_time", "full_name", "bin")


class UserListSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Users
        sqla_session = db.session
        load_instance = True
        exclude = ("_password", "active", "update_time", "create_time", "id")
