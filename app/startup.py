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

def getFormatId(format):
    cur = conn.cursor()
    roleIdQuery = "select id from formats where name = %s"
    cur.execute(roleIdQuery,(format,))
    formt = int(cur.fetchone()[0])
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
        #cur.close()
        team_list = []
        for team in teams:
            team_list.append(team[0])
        res['teams'] = team_list
        format_query = "select name from formats"
        cur.execute(format_query)
        formats = cur.fetchall()
        cur.close()
        format_list = []
        for format in formats:
            format_list.append(format[0])
        res['formats'] = format_list
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
        res['formats'] = format_list
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
    res['id'] = int(player[0])
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
    update_format = {'test' : 0, 'odi': 0, 't20' :0}
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
        update_format[res['format']] = 1
    emptyRes = {}
    emptyRes['id'] = None
    emptyRes['format'] = None
    emptyRes['matches'] = None
    emptyRes['innings'] = None
    emptyRes['runs'] = None
    emptyRes['balls_faced'] = None
    emptyRes['strike_rate'] = None
    emptyRes['average'] = None
    emptyRes['ducks'] = None
    emptyRes['50s'] = None
    emptyRes['100s'] = None
    emptyRes['200s'] = None
    emptyRes['highest_score'] = None
    emptyRes['not_outs'] = None
    if update_format['test'] == 0:
        result['test'] = emptyRes
    if update_format['odi'] == 0:
        result['odi'] = emptyRes
    if update_format['t20'] == 0:
        result['t20'] = emptyRes

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

def updatePlayerInfo(player_data):
    cur = conn.cursor()
    data = player_data['player_info']
    player_id = data['id']
    player_name = data['name']
    player_dob = datetime.datetime.strptime(data['dob'] , '%Y-%m-%d').date()
    role = data['role']
    team = data['team']
    bat_type = data['batting_type']
    bowl_type = None
    if 'bowling_type' in data:
        bowl_type = data['bowling_type']
    # role_id = get_roleId(role)
    roleIdQuery = "select id from player_roles where name = %s"
    cur.execute(roleIdQuery,(role,))
    role_id = int(cur.fetchone()[0])
    teamIdQuery = "select id from teams where name = %s"
    cur.execute(teamIdQuery,(team,))
    teamId = cur.fetchone()[0]
    insertQuery = "Update player_info set name = %s, dob = %s, role_id = %s, team_id = %s, batting_type = %s, bowling_type = %s where id = %s;"
    cur.execute(insertQuery,(player_name,player_dob,role_id,teamId,bat_type,bowl_type,player_id))
    conn.commit()
    cur.close()

def updateBattingStats(bat_data):
    cur = conn.cursor()
    req = bat_data['batting_stats']
    formats = ['test','odi','t20']
    for f in formats:
        if req[f] != {}:
            res= req[f]
            player_id = res['id']
            if player_id is None:
                continue
            format_id = getFormatId(res['format'])
            matches = res['matches']
            innings = res['innings']
            runs = res['runs']
            balls_faced = res['balls_faced']
            strike_rate = res['strike_rate']
            average = res['average']
            ducks = res['ducks']
            s50s = res['50s']
            s100s = res['100s']
            s200s = res['200s']
            highest_score = res['highest_score']
            notouts= res['not_outs']
            # insertQuery = "Update batting_statistics set matches = %s, innings = %s, runs = %s, balls_faced = %s, strike_rate = %s, average = %s, ducks = %s, 50s = %s,100s = %s,200s = %s,highest_score = %s,notouts = %s where id = %s and format_id = %s;"
            # cur.execute(insertQuery,(matches,innings,runs,balls_faced,strike_rate,average,ducks,s50s, s100s, s200s, highest_score,notouts, player_id,format_id))
            insertQuery = "Update batting_statistics set matches = %s, innings = %s, runs = %s, balls_faced = %s, strike_rate = %s, average = %s, ducks = %s, highest_score = %s,not_outs = %s where player_id = %s and format_id = %s;"
            cur.execute(insertQuery,(matches,innings,runs,balls_faced,strike_rate,average,ducks, highest_score,notouts, player_id,format_id))
            conn.commit()
    conn.close()
    

class updatePlayer(Resource):
    def post(self):
        # try:
            cur = conn.cursor()
            data = json.loads(request.get_data())
            if 'player_info' in data:
                updatePlayerInfo(data)
            if 'batting_stats' in data:
                updateBattingStats(data)
            return {"status_code": 200, "msg" : "successfully updated"}, 200
        # except:
        #     return {"status_code": 404, "msg" : "exception has occurred"}, 404

class getAllPlayers(Resource):
    def get(self):
        team = request.args.get('team')
        role = request.args.get('role')
        battingType = request.args.get('batting_type')
        bowlingType = request.args.get('bowling_type')
        print(team)
        cur = conn.cursor()
        getPlayerQuery = "select p.id, p.name,p.dob,t.name as team,r.name as role,p.batting_type,p.bowling_type from player_info p, teams t, player_roles r where r.id = p.role_id and p.team_id = t.id"
        if team is not None:
            getPlayerQuery = getPlayerQuery + ' and t.name = ' + '\''+team +'\''
        if role is not None:
            getPlayerQuery = getPlayerQuery + ' and r.name = ' + '\''+role+'\''
        if battingType is not None:
            getPlayerQuery = getPlayerQuery + ' and p.batting_type = ' + '\''+battingType+'\''
        if bowlingType is not None:
            getPlayerQuery = getPlayerQuery + ' and p.bowling_type = ' + '\''+bowlingType+'\''
        getPlayerQuery = getPlayerQuery + ';'
        cur.execute(getPlayerQuery)
        result = cur.fetchmany(50)
        res = []
        for rec in result:
            record = {}
            record['player_id'] = int(rec[0])
            record['name'] = str(rec[1])
            record['dob'] = str(rec[2])
            record['team'] = str(rec[3])
            record['role'] = str(rec[4])
            record['batting_type'] = str(rec[5])
            record['bowling_type'] = str(rec[6])
            res.append(record)
        return {'data': res},200

def start_endpoint():
    api.add_resource(register,'/register')
    api.add_resource(filterInfo,'/filterInfo')
    api.add_resource(getFormats,'/getFormats')
    api.add_resource(getPlayer,'/getPlayer')
    api.add_resource(updatePlayer,'/updatePlayer')
    api.add_resource(getAllPlayers,'/getAllPlayers')
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
    test_db()
    #test_db()
    #conn.close()
