from flask_restful import Resource
from flask import request
import requests
from .utils.service import ExtractWithExcel, add_days
from flask import jsonify
from datetime import datetime
from flask_jwt_extended import get_jwt_identity, jwt_required
from auth_service_api.models import Users
from auth_service_api.extensions import pagination
from auth_service_api.api.v1.schemas import ResMyActionSchema
dxl = ExtractWithExcel('gu_type_add_school.xlsx')


class ResMyNotification(Resource):
    @jwt_required
    def get(self):
        userID = get_jwt_identity()
        if userID:
            user = Users.query.get_or_404(userID)
            url = 'https://apitst.qaznaonline.kz/adn/api/v1/applications-for-parents?requesterIin=' + user.bin
            data = requests.request(method='get', url=url)
            if data.status_code == 200:
                res = data.json()['results']
                result = []
                d = dict()
                if res is not None:
                    for item in res:
                        d['ServiceName'] = dxl.getNameWithCode(int(item['Type_applic']))
                        d['RequestId'] = item['externalRequestId']
                        d['DateTimeStatement'] = item['create_time']
                        if item['received_time'] is not None:
                            d['StatusRecived'] = "received"
                            d['ReceivedTime'] = item['received_time']
                        else:
                            d['StatusRecived'] = "not received"
                        d['ResultTiming'] = 5
                        d['DatatimeOfTheResult'] = datetime.isoformat(add_days(item['create_time'], d['ResultTiming']))
                        d['StatusApplication'] = item['status_application']
                        result.append(d)
                if result:
                    return pagination.paginate(result, ResMyActionSchema(many=True), marshmallow=True)
        else:
            return {"error": "Data not found by IIN %s" % user.bin}
