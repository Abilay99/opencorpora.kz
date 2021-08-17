from flask_restful import Resource
# from flask_jwt_extended import jwt_required, get_jwt_identity, get_current_user
from flask import request
import requests


class ChekOrganized(Resource):
    def get(self):
        kato_number = request.args.get('kato_number')
        # current_user = get_current_user()
        # token = get_jwt_identity()
        print("Kato number", kato_number)
        url = 'https://apitst.qaznaonline.kz/eddo/api/v1'\
            '/check_organization_capacity?kato_number=' + kato_number
        req = requests.request(method='get', url=url)
        print("REQ", req)
        return req.json()


# @blueprint.route("/organizations-staff", methods=["GET"])
# def get_organizations_staff():
#     organization_id = request.args.get("organizations_id")
#     header = str(request.headers["Authorization"])
#    token_split = header.split()
#    token = token_split[1]
#    if organization_id:
#        req = requests.get(
#            ROOT_URL+'/api/v1/organizations-staff?organization_id='+ organization_id,
#            headers={"Authorization": "Bearer %s" % token}
#            )
#        query = req.json()
#        return query
#             else:
#         return {"msg": "organization_id required"}