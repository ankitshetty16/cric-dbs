from flask import Flask, render_template
from flask import request
from flask_restful import Resource, Api, reqparse
import requests
from urllib.parse import quote
import psycopg2
import json
import datetime

app = Flask(__name__)
api = Api(app)

conn = psycopg2.connect(
    host = "localhost",
    database = "players-point",
    user = "postgres",
    password = "admin123"
)

@app.route("/")
def home():
    return render_template("index.html")

def get_roleId(role):
    if role == "Batsman":
        return 1
    elif role == "Bowler":
        return 2
    elif role == "WK-Batsman":
        return 3
    elif role == "Batting Allrounder":
        return 4
    else:
        return 5
class register(Resource):
    def post(self):
        try:
            data = request.get_json()
            player_name = data['name']
            player_dob = datetime.datetime.strptime(data['dob'] , '%Y/%m/%d').date()
            role = data['role']
            team = data['team']
            bat_type = data['batType']
            bowl_type = None
            if 'bowlType' in data:
                bowl_type = data['bowlType']
            role_id = get_roleId(role)
            cur = conn.cursor()
            play_id_query = "select max(id) from player_info"
            cur.execute(play_id_query)
            player_id = int(cur.fetchone()[0]) + 1
            teamIdQuery = "select id from teams where name = %s"
            cur.execute(teamIdQuery,(team,))
            teamId = cur.fetchone()[0]
            insertQuery = "Insert into player_info values(%s,%s,%s,%s,%s,%s,%s); "
            cur.execute(insertQuery,(player_id,player_name,player_dob,role_id,teamId,bat_type,bowl_type))
            conn.commit()
            cur.close()
            resp = {"success":True}
            return resp, 200
        except:
            print("An exception has occured")
            return 404

class filterInfo(Resource):
    def get(self):
        cur = conn.cursor()
        role_query = "select name from player_roles"
        cur.execute(role_query)
        roles = cur.fetchall()
        res = {}
        role_list = []
        for role in roles:
            role_list.append(role[0])
        res['roles'] = role_list
        team_query = "select name from teams"
        cur.execute(team_query)
        teams = cur.fetchall()
        team_list = []
        for team in teams:
            team_list.append(team[0])
        res['teams'] = team_list
        return res,200

def start_endpoint():
    api.add_resource(register,'/register')
    api.add_resource(filterInfo,'/filterInfo')
    app.run(host="0.0.0.0", port="80",debug=True)

def test_db():
    cur = conn.cursor()
    test_query = "select * from player_info"
    cur.execute(test_query)
    rec = cur.fetchall()
    print(rec)
    cur.close()

# @app.after_request
# def after_request():
#     if conn is not None:
#         print("closing connection")
#         conn.close()

if __name__ == '__main__':
    start_endpoint()
    #test_db()
    #conn.close()
