import requests
from flask import jsonify, request, make_response
from flask_restful import Resource
import json


class KidDirecton(Resource):
    # def post(self):
    #     url = 'http://apitst.qaznaonline.kz/eddo/api/v1/kid_direction'
    #
    #     data = request.json
    #     print(data)
    #     response = requests.post(url=url, data=data)
    #     print("success", response.text)
    #     return {'test': response.text}

    def post(self):
        url = 'https://apitst.qaznaonline.kz/eddo/api/v1/kid_direction'
        data = request.json
        serialized = {
            "kid_name": data['kid_name'],
            "kid_surname": data['kid_surname'],
            "kid_father_name": data['kid_father_name'],
            "kid_direction_data": data['kid_direction_data'],
            "organizations_id": data['organizations_id'],
            "kid_direction_number": data['kid_direction_number'],
            "base_organization_name": data['base_organization_name'],
            "kato_number": data['kato_number'],
            "kid_iin": data['kid_iin']
        }
        headers = {
            "X-Requested-With": "XMLHttpRequest",
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.52 Safari/536.5",
            "Content-Type": "application/json",
            "Accept": "*/*"
        }
        print(serialized)
        payload = json.dumps(serialized)
        response = requests.request("POST", url, headers=headers, data=payload)
        response = make_response(response.content)
        response.headers['Content-Type'] = "application/json"
        return response
        # response = requests.post(url=url, data=json.dumps(serialized), headers=headers, verify=False)
        # return response.text



# resp = requests.get("https://status.github.com/api/status.json")
# x = resp.json()

# import requests
# url = 'https://status.github.com/api/status.json'
# resp = requests.get(url)
# print(resp.status_code)
# # => 200
# print(resp.json())
# print(resp.json()['status'])
# => {'status': 'good', 'last_updated': '2015-04-20T13:08:28Z'}

# import json
# mydata = {"name": "Apple", "quantity": 42, "date": "2014-02-27" }
# serializeddata = json.dumps(mydata)

# def post(self):
#     schema = UserFullSchema()
#     user = schema.load(request.json)
#
#     db.session.add(user)
#     db.session.commit()
#
#     return {"msg": "user created", "user": schema.dump(user)}, 201