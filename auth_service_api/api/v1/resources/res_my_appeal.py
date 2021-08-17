from flask_restful import Resource
from flask import request
import requests
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth_service_api.models import Users
from auth_service_api.extensions import pagination
from auth_service_api.extensions import db
from auth_service_api.models import ElectronicAppeals
from auth_service_api.api.v1.schemas import ElectronicAppealsSchema

class ResMyAppeal(Resource):
    @jwt_required
    def get(self):
        userID = get_jwt_identity()
        if userID:
            externalRequestId = request.json.get('RequestId', None)
            if externalRequestId is None:
                return {'Warring': 'pls enter statement ID'}, 401
            get_obj = ElectronicAppeals.query.filter((ElectronicAppeals.id_user == userID)
                                                     & (ElectronicAppeals.externalRequestId == externalRequestId)
                                                     ).order_by(ElectronicAppeals.updated_date.desc()).first()
            if get_obj is not None:
                schema = ElectronicAppealsSchema(many=False)
                return schema.dump(get_obj), 200
            return {"Error": "not found applea"}, 401
        return {"Error": "not found token"}, 403

    @jwt_required
    def post(self):
        userID = get_jwt_identity()
        if userID:
            user = Users.query.get_or_404(userID)
            externalRequestId = request.json.get('RequestId', None)
            if externalRequestId is None:
                return {'Warring': 'pls enter statement ID'}, 401
            descreption = request.json.get('descreption', None)
            if descreption is None:
                return {'Warring': 'pls enter descreption'}, 401
            application_id = None
            url = 'https://apitst.qaznaonline.kz/adn/api/v1/applications-for-parents?requesterIin=' + user.bin
            data = requests.request(method='get', url=url)
            if data.status_code == 200:
                res = data.json()['results']
                if res is not None:
                    for item in res:
                        if item['externalRequestId'] == externalRequestId:
                            application_id = item['application_id']
            else:
                return {"Error": "not found pupil on IIN: %s" % user.bin}, 401
            obj = ElectronicAppeals(
                externalRequestId=externalRequestId,
                id_user=userID,
                application_id=application_id,
                descreption=descreption
            )
            db.session.add(obj)
            db.session.commit()
            return {"succes": "created appeal"}, 200
        return {"Error": "user unauthorization"}, 403
