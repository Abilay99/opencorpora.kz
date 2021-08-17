from flask import Blueprint, current_app, jsonify
from flask_restful import Api
from marshmallow import ValidationError

from auth_service_api.api.v1.resources import ResMyAction
from auth_service_api.api.v1.resources import ResMyNotification
from auth_service_api.api.v1.resources import ResMyAppeal
from auth_service_api.extensions import apispec
from auth_service_api.api.v1.resources import ResMyProfile
from auth_service_api.api.v1.resources import ChekOrganized
from auth_service_api.api.v1.resources import KidDirecton
from auth_service_api.api.v1.schemas import UserListSchema


blueprint = Blueprint("api", __name__, url_prefix="/api/v1")
api = Api(blueprint)

api.add_resource(ResMyProfile, "/my-profile", endpoint="my_profile")
# Darkhan API
# api.add_resource(UserRequestIin, "/user_iin", endpoint="user_by_iin")
# Dauren API
api.add_resource(ResMyAction, "/my-action", endpoint="my_action")
api.add_resource(ResMyAppeal, "/my-appeal", endpoint="my_appeal")
api.add_resource(ResMyNotification, "/my-notification", endpoint="my_notification")
# api.add_resource(ChekOrganized, "/chek_organized", endpoint="check_by_organized")
# api.add_resource(KidDirecton, "/kid_direction", endpoint="kid_by_direction")


@blueprint.before_app_first_request
def register_views():
    apispec.spec.components.schema("UserListSchema", schema=UserListSchema)
    apispec.spec.path(view=ResMyProfile, app=current_app)


@blueprint.errorhandler(ValidationError)
def handle_marshmallow_error(e):
    return jsonify(e.messages), 400
