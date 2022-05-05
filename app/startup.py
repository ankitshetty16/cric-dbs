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

def get_roleId(role_id):
    cur = conn.cursor()
    roleIdQuery = "select name from player_roles where id = %s"
    cur.execute(roleIdQuery,(role_id,))
    role = str(cur.fetchone()[0])
    cur.close()
    return role

def getTeam(team_id):
    cur = conn.cursor()
    roleIdQuery = "select name from teams where id = %s"
    cur.execute(roleIdQuery,(team_id,))
    team = str(cur.fetchone()[0])
    cur.close()
    return team

def getFormat(format_id):
    cur = conn.cursor()
    roleIdQuery = "select name from formats where id = %s"
    cur.execute(roleIdQuery,(format_id,))
    formt = str(cur.fetchone()[0])
    cur.close()
    return formt

class register(Resource):
    def post(self):
        try:
            cur = conn.cursor()
            data = json.loads(request.get_data())
            player_name = data['name']
            player_dob = datetime.datetime.strptime(data['dob'] , '%Y/%m/%d').date()
            role = data['role']
            team = data['team']
            bat_type = data['batType']
            bowl_type = None
            if 'bowlType' in data:
                bowl_type = data['bowlType']
            # role_id = get_roleId(role)
            roleIdQuery = "select id from player_roles where name = %s"
            cur.execute(roleIdQuery,(role,))
            role_id = int(cur.fetchone()[0])
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
        cur.close()
        team_list = []
        for team in teams:
            team_list.append(team[0])
        res['teams'] = team_list
        return res,200

class getFormats(Resource):
    def get(self):
        cur = conn.cursor()
        format_query = "select name from formats"
        cur.execute(format_query)
        roles = cur.fetchall()
        cur.close()
        res = {}
        format_list = []
        for format in roles:
            format_list.append(format[0])
        res['roles'] = format_list
        return res,200

def getPlayerInfo(id):
    cur = conn.cursor()
    player_query = "select * from player_info where id = %s"
    cur.execute(player_query,(id),)
    player = cur.fetchone()
    cur.close()
    if player is None:
        return {}
    res = {}
    res['name'] = str(player[1])
    res['dob'] = str(player[2])
    res['role'] = get_roleId(int(player[3]))
    res['team'] = getTeam(int(player[4]))
    res['batting_type'] = str(player[5])
    res['bowling_type'] = str(player[6])
    return res

def getBattingStats(id):
    cur = conn.cursor()
    player_query = "select * from batting_statistics where player_id = %s"
    cur.execute(player_query,(id),)
    players = cur.fetchall()
    cur.close()
    if players is None:
        return {}
    result = {}
    #data = []
    for player in players:
        res = {}
        res['id'] = int(player[1])
        res['format'] = getFormat(int(player[2]))
        res['matches'] = int(player[3])
        res['innings'] = int(player[4])
        res['runs'] = int(player[5])
        res['balls_faced'] = int(player[6])
        res['strike_rate'] = float(player[7])
        res['average'] = float(player[8])
        res['ducks'] = int(player[9])
        res['50s'] = int(player[10])
        res['100s'] = int(player[11])
        res['200s'] = int(player[12])
        res['highest_score'] = int(player[13])
        res['not_outs'] = int(player[14])
        result[res['format']] = res
    return result


def getBowlingStats(id):
    cur = conn.cursor()
    player_query = "select * from bowling_statistics where player_id = %s"
    cur.execute(player_query,(id),)
    players = cur.fetchall()
    cur.close()
    if players is None:
        return {}
    result = {}
    #data = []
    for player in players:
        res = {}
        res['id'] = int(player[1])
        res['format'] = getFormat(int(player[2]))
        res['matches'] = int(player[3])
        res['innings'] = int(player[4])
        res['balls'] = int(player[5])
        res['economy'] = float(player[6])
        res['average'] = float(player[7])
        res['maidens'] = int(player[8])
        res['wickets'] = int(player[9])
        res['4_wicket'] = int(player[10])
        res['5_wicket'] = int(player[11])
        result[res['format']] = res
    return result

class getPlayer(Resource):
    def get(self):
        player_id = request.args.get('id')
        player_info = getPlayerInfo(player_id)
        if player_info == {}:
            return {"msg":"record not found", "status_code": 400},400
        res = {}
        res['player_info'] = player_info
        batting_stats = getBattingStats(player_id)
        res['batting_stats'] = batting_stats
        bowling_stats = getBowlingStats(player_id)
        res['bowling_stats'] = bowling_stats
        return res,200

def start_endpoint():
    api.add_resource(register,'/register')
    api.add_resource(filterInfo,'/filterInfo')
    api.add_resource(getFormats,'/getFormats')
    api.add_resource(getPlayer,'/getPlayer')
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
