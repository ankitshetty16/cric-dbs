import psycopg2
import pandas as pd
import csv

conn = psycopg2.connect(
    host = "localhost",
    database = "Players Point",
    user = "postgres",
    password = "Chauvinist@5"
)

def formats():
    formats={1:"test",2:"odi",3:"t20"}
    cur=conn.cursor()
    for k,v in formats.items():
        id=k
        format=v
        insertQuery = "Insert into formats values(%s,%s); "
        cur.execute(insertQuery,(id,format))
    conn.commit()
    cur.close()


def player_roles(df):
    roles={}
    count=1
    for i in df.player_role:
        if i not in roles.values():
            roles[count]=i
            count+=1
    cur=conn.cursor()
    for k,v in roles.items():
        id=k
        role=v
        insertQuery = "Insert into player_roles values(%s,%s); "
        cur.execute(insertQuery,(id,role))
    conn.commit()
    cur.close()
    return roles

def fill_player_ranking(player_id,format_id,role_id,rank):
    cur=conn.cursor()
    insertQuery = "Insert into player_rankings values(%s,%s,%s,%s); "
    cur.execute(insertQuery,(player_id,format_id,role_id,rank))
    conn.commit()
    cur.close()


def player_rankings(df,roles):
    # count=1
    x=0
    for j in df.player_id:   
        player_id=j
        # for r in ["bat","bowl"]:
            
        for m in [1,2,3]:
            format_id=m
            for k, v in roles.items():
                if df.player_role[x]==v:
                    role_id=k
            # id=count
            # if r=="bat":
            if role_id==2 or role_id==1 or role_id==4:
                if m==1:
                    rank=df.player_bat_testrank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
                elif m==2:
                    rank=df.player_bat_Odirank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
                elif m==3:
                    rank=df.player_bat_t20rank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
            # elif r=="bowl":
            elif role_id==3 or role_id==5:
                if m==1:
                    rank=df.player_bowl_testrank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
                elif m==2:
                    rank=df.player_bowl_Odirank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
                elif m==3:
                    rank=df.player_bowl_t20rank[x]
                    if rank:
                        fill_player_ranking(int(player_id),int(format_id),int(role_id),int(rank))
                        # count+=1
            # print(count)
        x+=1
        print(x)

def teams(df):
    teams={}
    count=1
    for i in df.player_intlTeam:
      if i not in teams.values():
        teams[count]=i
        count+=1
    test_rank=[36,77,19,100,66,85,18,76,74,78,94,28,96,51,89,53,21,15,62,60,17,99,32,65,56,67,64,98,40,1,120,90,4,25,92,80,69,55,8,3,82,42,83,20,2]
    Odi_rank=[21,46,4,17,14,55,84,97,80,59,22,20,1,49,44,6,63,69,62,76,13,35,66,73,47,52,102,39,81,33,31,56,53,30,28,91,98,3,70,8,67,100,61,48,24]   
    t20_rank=[78,19,110,50,15,85,90,95,25,83,73,66,54,81,36,24,11,53,21,100,60,70,35,14,16,2,5,10,97,61,9,30,37,88,13,86,76,65,64,57,23,79,22,99,63]
    cur=conn.cursor()
    x=0
    for k,v in teams.items():
        id=k
        team=v
        insertQuery = "Insert into teams values(%s,%s,%s,%s,%s); "
        cur.execute(insertQuery,(id,team,test_rank[x],Odi_rank[x],t20_rank[x]))
        x+=1
    conn.commit()
    cur.close()
    return teams

def fill_in_player_info(id,name,dob,role_id,team_id,batting_type,bowling_type):
    cur=conn.cursor()
    insertQuery = "Insert into player_info values(%s,%s,%s,%s,%s,%s,%s); "
    cur.execute(insertQuery,(id,name,dob,role_id,team_id,batting_type,bowling_type))
    conn.commit()
    cur.close()
    

def player_info(df,roles,team):
    for x in range(len(df.player_id)):
        id=df.player_id[x]
        name=df.player_name[x]
        print(id)
        dob=pd.to_datetime(df.player_DOB[x], format='%d-%m-%Y')
        for k,v in roles.items():
            if df.player_role[x]==v:
                role_id=k
        for k,v in team.items():
            if df.player_intlTeam[x]==v:
                team_id=k
        batting_type=df.player_battingtype[x]
        bowling_type=df.Player_bowlingtype[x]
        fill_in_player_info(int(id),name,dob,int(role_id),int(team_id),batting_type,bowling_type) 

def fill_in_bowling_stats(player_id,format_id,matches,innings,balls,economy,average,maidens,wickets,wicket_4,wicket_5):
    cur=conn.cursor()
    insertQuery = "Insert into bowling_statistics values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
    cur.execute(insertQuery,(player_id,format_id,matches,innings,balls,economy,average,maidens,wickets,wicket_4,wicket_5))
    conn.commit()
    cur.close()                                
    
def bowling_statistics(df):
    x=0
    # count=1
    
    for j in df.player_id:   
        player_id=j
        for m in [1,2,3]:
            format_id=m
            
            # id =count
            if m==1:
                matches= df.player_Bowling_Matches_Test[x]
                innings=df.player_Bowling_Innings_Test[x]
                balls=df.player_Bowling_Balls_Test[x]
                economy=df.player_Bowling_ECO_Test[x]
                average=df.player_Bowling_Avg_Test[x]
                maidens=df.player_Bowling_Maidens_Test[x]
                wickets=df.player_Bowling_Wickets_Test[x]
                wicket_4=df.player_Bowling_4W_Test[x]
                wicket_5=df.player_Bowling_5W_Test[x]
                fill_in_bowling_stats(int(player_id),int(format_id),int(matches),int(innings),int(balls),float(economy),float(average),int(maidens),int(wickets),int(wicket_4),int(wicket_5))
                                        

            elif m==2:
                matches= df.player_Bowling_Matches_ODI[x]
                innings=df.player_Bowling_Innings_ODI[x]
                balls=df.player_Bowling_Balls_ODI[x]
                economy=df.player_Bowling_ECO_ODI[x]
                average=df.player_Bowling_Avg_ODI[x]
                maidens=df.player_Bowling_Maidens_ODI[x]
                wickets=df.player_Bowling_Wickets_ODI[x]
                wicket_4=df.player_Bowling_4W_ODI[x]
                wicket_5=df.player_Bowling_5W_ODI[x]
                fill_in_bowling_stats(int(player_id),int(format_id),int(matches),int(innings),int(balls),float(economy),float(average),int(maidens),int(wickets),int(wicket_4),int(wicket_5))

            elif m==3:
                matches= df.player_Bowling_Matches_T20[x]
                innings=df.player_Bowling_Innings_T20[x]
                balls=df.player_Bowling_Balls_T20[x]
                economy=df.player_Bowling_ECO_T20[x]
                average=df.player_Bowling_Avg_T20[x]
                maidens=df.player_Bowling_Maidens_T20[x]
                wickets=df.player_Bowling_Wickets_T20[x]
                wicket_4=df.player_Bowling_4W_T20[x]
                wicket_5=df.player_Bowling_5W_T20[x]
                fill_in_bowling_stats(int(player_id),int(format_id),int(matches),int(innings),int(balls),float(economy),float(average),int(maidens),int(wickets),int(wicket_4),int(wicket_5))
            # count+=1                            
        x+=1

def fill_in_batting_stats(player_id,format_id,matches,innings,runs,balls_faced,strike_rate,average,ducks,no_50s,no_100s,no_200s,highest_score,not_outs):
    cur=conn.cursor()
    insertQuery = "Insert into batting_statistics values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s); "
    cur.execute(insertQuery,(player_id,format_id,matches,innings,runs,balls_faced,strike_rate,average,ducks,no_50s,no_100s,no_200s,highest_score,not_outs))
    conn.commit()
    cur.close()   

def batting_statistics(df):
    x=0
    # count=1

    for j in df.player_id:   
        player_id=j    
        
    
        for m in [1,2,3]:
            format_id=m
            # id =count
            if m==1:
                matches= df.player_batting_Matches_Test[x]
                innings=df.player_batting_Inning_Test[x]
                runs=df.player_batting_runs_Test[x]
                balls_faced=df.player_batting_Balls_Test[x]
                strike_rate= df.player_batting_SR_Test[x]
                average=df.player_batting_Average_Test[x]
                ducks=df.player_batting_Ducks_Test[x]
                no_50s=df.player_batting_50s_Test[x]
                no_100s=df.player_batting_100s_Test[x]
                no_200s=df.player_batting_200s_Test[x]
                highest_score=df.player_batting_Highest_Test[x]
                not_outs=df.player_batting_NotOut_Test[x]
                fill_in_batting_stats(int(player_id),int(format_id),int(matches),int(innings),int(runs),int(balls_faced),float(strike_rate),float(average),int(ducks),int(no_50s),int(no_100s),int(no_200s),int(highest_score),int(not_outs))

            elif m==2:
                matches= df.player_batting_Matches_ODI[x]
                innings=df.player_batting_Inning_ODI[x]
                runs=df.player_batting_runs_ODI[x]
                balls_faced=df.player_batting_Balls_ODI[x]
                strike_rate= df.player_batting_SR_ODI[x]
                average=df.player_batting_Average_ODI[x]
                ducks=df.player_batting_Ducks_ODI[x]
                no_50s=df.player_batting_50s_ODI[x]
                no_100s=df.player_batting_100s_ODI[x]
                no_200s=df.player_batting_200s_ODI[x]
                highest_score=df.player_batting_Highest_ODI[x]
                not_outs=df.player_batting_NotOut_ODI[x]
                fill_in_batting_stats(int(player_id),int(format_id),int(matches),int(innings),int(runs),int(balls_faced),float(strike_rate),float(average),int(ducks),int(no_50s),int(no_100s),int(no_200s),int(highest_score),int(not_outs))
                                        
    
            elif m==3:
                matches= df.player_batting_Matches_T20[x]
                innings=df.player_batting_Inning_T20[x]
                runs=df.player_batting_runs_T20[x]
                balls_faced=df.player_batting_Balls_T20[x]
                strike_rate= df.player_batting_SR_T20[x]
                average=df.player_batting_Average_T20[x]
                ducks=df.player_batting_Ducks_T20[x]
                no_50s=df.player_batting_50s_T20[x]
                no_100s=df.player_batting_100s_T20[x]
                no_200s=df.player_batting_200s_T20[x]
                highest_score=df.player_batting_Highest_T20[x]
                not_outs=df.player_batting_NotOut_T20[x]
                fill_in_batting_stats(int(player_id),int(format_id),int(matches),int(innings),int(runs),int(balls_faced),float(strike_rate),float(average),int(ducks),int(no_50s),int(no_100s),int(no_200s),int(highest_score),int(not_outs))
            # count+=1
        x+=1
    
if __name__ == '__main__':
    print("Welcome!")
    print("loading the datatables....")
    with open("players_point.csv", "r") as f:
        reader= csv.reader(f)
        head= next(reader)
    df=pd.read_csv("players_point.csv",usecols=head)
    

    formats()
    print("formats table laoded")
    roles=player_roles(df)
    print("player_roles table laoded")
    team =teams(df)
    print("teams table laoded")
    player_info(df,roles,team)
    print("player_info table laoded")
    player_rankings(df,roles)
    print("player_ranking table loaded")
    bowling_statistics(df)
    print("bowling_statistics table laoded")
    batting_statistics(df)
    print("batting_statistics table laoded")


    print("---------------------------------------")

    print("The PLAYERS POINT DATATABLE is loaded ")
    print("<<<<<<<<<<<<<<<<Have fun in PLAYERS POINT !>>>>>>>>>>>>>>>>>>>>>>>>")
