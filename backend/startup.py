from flask import Flask
from flask import request
from flask_restful import Resource, Api, reqparse
import requests
from urllib.parse import quote

app = Flask(__name__)
api = Api(app)

class register(Resource):
    def post(self):
        print(request.get_json())
        resp = {"register" : "success"}
        return resp, 200

def start_endpoint():
    api.add_resource(register,'/register')
    app.run(host="0.0.0.0", port="5000")

if __name__ == '__main__':
    start_endpoint()
