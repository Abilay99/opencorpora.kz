from flask import request, jsonify, Blueprint, current_app as app
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt,
)
from auth_service_api.api.auth.utils import send_mobile
from auth_service_api.models import Users, VerifyCode
from auth_service_api.models.helpers import DateTime
from auth_service_api.extensions import pwd_context, jwt, apispec
from auth_service_api.api.auth.helpers import revoke_token, is_token_revoked,\
    add_token_to_database
from auth_service_api.extensions import db
from auth_service_api.api.auth.language import (
    UESR_NOT_FIND1,
    SEND_TYPE_ERR,
    UESR_NOT_FIND,
    REQUIRED_MOBILE_AND_SEND_TYPE,
    NOT_JSON,
    except_mobile,
    SUCCESSFUL_SMS,
    FAILED_SEND_SMS,
    REQUIRED_MOBILE_AND_PASSWORD,
    REQUIRED_BIN_AND_PASSWORD,
    LOGIN_FAILED,
    VERIFICATION_CODE_ERROR,
    VERIFICATION_CODE_EXPIRED,
    REQUIRED_VERIFICATION_CODE,
    REQUIRED_FORM_DATA,
    USER_IS_REGISTRED,
    CREATE_NEW_USER,
    PASSWORD_NOT_SAME,
    PASSWORD_UPDATE
)


blueprint = Blueprint("auth", __name__, url_prefix="/api/auth")

@blueprint.route("/test", methods=["POST"])
def test():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

@blueprint.route("/sms", methods=["POST"])
def send_sms():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    mobile = request.json.get("mobile", None)
    send_type = request.json.get("send_type", None)

    if not mobile or not send_type:
        return jsonify(REQUIRED_MOBILE_AND_SEND_TYPE), 400

    user = Users.query.filter_by(mobile=mobile).first()
    mobile = str(mobile)[::-1][0:10][::-1]
    if send_type == 'send_type1':
        if user is not None:
            return jsonify(UESR_NOT_FIND1), 400
    elif send_type == 'send_type2':
        if user is None:
            return jsonify(UESR_NOT_FIND), 400
    else:
        return jsonify(SEND_TYPE_ERR), 400

    verify_code = VerifyCode.query.filter_by(mobile=mobile, send_type=send_type)\
        .order_by(VerifyCode.id.desc()).first()

    if verify_code:
        exp_time = verify_code.repeat_expire_time
        print(exp_time)
        if exp_time is not None and exp_time > DateTime.now():
            return jsonify(error="Kute turynyz bloktalu uaqyty %s dein" % exp_time), 400
        if verify_code.repeat_expire_time is not None and exp_time <= DateTime.now():
            verify_code.repeat_expire_time = None
            verify_code.repeat_count = 0
            db.session.flush()
        if verify_code.repeat_count >= 3:
            verify_code.repeat_expire_time = DateTime.now() + DateTime.timedelta(m=30)
            db.session.commit()
            return jsonify(except_mobile(mobile[:3])), 400
    send_status = send_mobile(mobile=mobile, send_type=send_type)
    if send_status:
        ret = {
            "mobile": mobile,
            "send_type": send_type,
            "msg": SUCCESSFUL_SMS
        }
        return jsonify(ret), 200
    else:
        return jsonify(FAILED_SEND_SMS), 400


@blueprint.route("/login", methods=["POST"])
def login():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    bin = request.json.get("bin", None)
    password = request.json.get("password", None)
    if not bin or not password:
        return jsonify(REQUIRED_BIN_AND_PASSWORD), 400

    user = Users.query.filter_by(bin=bin).first()
    if user is None or not pwd_context.verify(password, user.password):
        return jsonify(LOGIN_FAILED), 400

    access_token = create_access_token(identity=user.id)
    refresh_token = create_refresh_token(identity=user.id)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    add_token_to_database(refresh_token, app.config["JWT_IDENTITY_CLAIM"])

    ret = {"access_token": access_token, "refresh_token": refresh_token}
    return jsonify(ret), 200


@blueprint.route("/register", methods=["POST"])
def register():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    bin = request.json.get("bin", None)
    full_name = request.json.get("full_name", None)
    mobile = request.json.get("mobile", None)
    code = request.json.get("code", None)
    email = request.json.get("email", None)
    password = request.json.get("password", None)
    if full_name and mobile and bin and password:
        if code:
            verify_records = VerifyCode.query.filter((VerifyCode.mobile == mobile)
                                                     & (VerifyCode.code == code)
                                                     & (VerifyCode.send_type == "send_type1")
                                                     ).order_by(VerifyCode.create_time.desc()).first()
            if verify_records is None:
                return jsonify(VERIFICATION_CODE_ERROR), 400
            else:
                five_minutes_ago = verify_records.create_time + DateTime.timedelta(m=5)
                if five_minutes_ago > DateTime.now():
                    return jsonify(VERIFICATION_CODE_EXPIRED), 400

                user = Users.query.filter((Users.bin == bin) | (Users.email == email)
                                          | (Users.mobile == mobile)).first()
                if user:
                    return jsonify(USER_IS_REGISTRED), 400

                obj_user = Users(
                    bin=bin,
                    full_name=full_name,
                    mobile=mobile,
                    email=email,
                    password=password
                )
                verify_records.sum_ = 0
                verify_records.is_valid = False
                db.session.add(obj_user)
                db.session.commit()
                ret = {
                    "status": "success",
                    "mobile": mobile,
                    "msg": CREATE_NEW_USER,
                }
                return jsonify(ret), 201
        else:
            return jsonify(REQUIRED_VERIFICATION_CODE), 400
    else:
        return jsonify(REQUIRED_FORM_DATA), 400

@blueprint.route("/reset-password", methods=["POST"])
def reset_password():
    if not request.is_json:
        return jsonify(NOT_JSON), 400

    mobile = request.json.get("mobile", None)
    code = request.json.get("code", None)
    password1 = request.json.get("password1", None)
    password2 = request.json.get("password2", None)

    if not mobile or not password1 or not password2 or not code:
        return jsonify(REQUIRED_MOBILE_AND_PASSWORD), 400

    user = Users.query.filter_by(mobile=mobile).first()
    if user is None:
        return jsonify(UESR_NOT_FIND), 400

    if password1 != password2:
        return jsonify(PASSWORD_NOT_SAME), 400

    if code is not None:
        verify_records = VerifyCode.query.filter((VerifyCode.mobile == mobile)
                                                 & (VerifyCode.code == code)
                                                 & (VerifyCode.send_type == "send_type2")
                                                 ).order_by(VerifyCode.create_time.desc()).first()
        if verify_records is None:
            return jsonify(VERIFICATION_CODE_ERROR), 400
        else:
            five_minutes_ago = verify_records.create_time + DateTime.timedelta(m=5)
            if five_minutes_ago > DateTime.now():
                return jsonify(VERIFICATION_CODE_EXPIRED), 400
            user.password = password1
            verify_records.sum_ = 0
            verify_records.is_valid = False
            db.session.commit()
            ret = {
                "status": "success",
                "mobile": mobile,
                "msg": PASSWORD_UPDATE
            }
            return jsonify(ret), 200
    else:
        return jsonify(REQUIRED_VERIFICATION_CODE), 400

@blueprint.route("/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)
    add_token_to_database(access_token, app.config["JWT_IDENTITY_CLAIM"])
    ret = {"access_token": access_token}
    return jsonify(ret), 200


@blueprint.route("/revoke_access", methods=["DELETE"])
@jwt_required
def revoke_access_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@blueprint.route("/revoke_refresh", methods=["DELETE"])
@jwt_refresh_token_required
def revoke_refresh_token():
    jti = get_raw_jwt()["jti"]
    user_identity = get_jwt_identity()
    revoke_token(jti, user_identity)
    return jsonify({"message": "token revoked"}), 200


@jwt.user_loader_callback_loader
def user_loader_callback(identity):
    return Users.query.get(identity)


@jwt.token_in_blacklist_loader
def check_if_token_revoked(decoded_token):
    return is_token_revoked(decoded_token)


@blueprint.before_app_first_request
def register_views():
    apispec.spec.path(view=send_sms, app=app)
    apispec.spec.path(view=login, app=app)
    apispec.spec.path(view=reset_password, app=app)
    apispec.spec.path(view=refresh, app=app)
    apispec.spec.path(view=revoke_access_token, app=app)
    apispec.spec.path(view=revoke_refresh_token, app=app)
