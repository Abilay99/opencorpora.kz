from flask import request
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity
from auth_service_api.models import Users
from auth_service_api.api.v1.resources.utils import UploadFile
from auth_service_api.extensions import db
from auth_service_api.commons.pagination import paginate
from auth_service_api.api.v1.schemas import (
    UserListSchema,
    UserFullSchema,
    UserPutSchema
)


class ResMyProfile(Resource):
    @jwt_required
    def get(self):
        user_id = get_jwt_identity()
        # request.args.get('user_id')
        if user_id:
            schema = UserListSchema()
            user = Users.query.get_or_404(user_id)
            user_json = schema.dump(user)
            return {"User": user_json}
        return {"error": "not found user"}, 403

    @jwt_required
    def put(self):
        user_id = get_jwt_identity()
        req = dict(request.form)
        user = Users.query.get_or_404(user_id)
        if req.get('mobile', None) is not None:
            user.mobile = req['mobile']
        if req.get('email', None) is not None:
            user.email = req['email']
        if req.get('password', None) is not None:
            user.password = req['password']
        if 'photo' in request.files:
            if request.files['photo']:
                if user.photo is not None:
                    UploadFile.rs_file([user.photo], True)
                    req = UploadFile.rs_file(['photo'])
                else:
                    req = UploadFile.rs_file(['photo'])
        
        schema = UserPutSchema(partial=True)
        user = schema.load(req, instance=user)
        db.session.commit()

        return {"msg": "user updated", "user": schema.dump(user)}

    def delete(self, user_id):
        user = Users.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()

        return {"msg": "user deleted"}
