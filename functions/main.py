import requests
import mysql.connector
from mysql.connector import errorcode
import datetime

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY5MGFhOTczLTBkZGItNDhiZC1hMDZmLTkwNTMwOTM4NzZiZSIsImlhdCI6MTcwNzE3NTY2NCwic3ViIjoiZGV2ZWxvcGVyLzc1MDJkNGRlLTI2YWEtZjhjMS0wMDRmLWVmZWJjYWFmODVlNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiXSwidHlwZSI6ImNsaWVudCJ9XX0.HNmCO6end3HxRkhkssTqK2-ZSVXEXQhUcfEuO2vH70vAWPvokFfulZK4WdjHtNbnf72J4ZSmOZb9Av3pV62VSw",
}

db_connection = mysql.connector.connect(user="remote", database="clashroyale", port=3306)
cursor = db_connection.cursor()

def main():
    #tags_id = verify_tags()
    #or i in range(len(tags_id)):
        get_json("#9G28ULYR")

def verify_tags():
    sql = "select (select group_concat(distinct tag_team) from battlelog) as tag_team, (select group_concat(distinct tag_opp) from battlelog) as tag_opp;"
    cursor.execute(sql)
                    
    tags = []
    for (tag) in cursor:
        for i in range(2):
            if "," not in tag[i]:
                tags_to_split = tag[i]
                tags.append(tags_to_split)
            else:
                tags_to_split = tag[i].split(",")
                for p in range(len(tags_to_split)):
                    tags.append(tags_to_split[p])

    return tags

def get_json(tag):
    tag = tag.replace("#", "%23")
    if len(tag) > 5:
        response = requests.get(url=f"https://proxy.royaleapi.dev/v1/players/{tag}/battlelog", headers=headers)
        response.raise_for_status()  # raises exception when not a 2xx response
        if response.status_code != 204:
            bt = response.json()
            for game in bt:
                battle_time = game["battleTime"]
                game_mode = game["gameMode"]["name"]
                for team in game["team"]:
                    name_team = team["name"]
                    tag_id_team = team["tag"]
                    id_battle = battle_time + tag_id_team
                    crowns_team = team["crowns"]
                    try:
                        name_clan_team = team["clan"]["name"]
                    except KeyError:
                        name_clan_team = ""
                        pass
                    i = 1
                    cartas_team = []
                    for card in team["cards"]:
                        if i < 9:
                            cartas_team.append(card["name"])
                    cartas_team = sorted(cartas_team)
                for opponent in game["opponent"]:
                    name_opp = opponent["name"]
                    tag_id_opp = opponent["tag"]
                    crowns_opp = opponent["crowns"]
                    try:
                        name_clan_opp = opponent["clan"]["name"]
                    except KeyError:
                        name_clan_opp = ""
                        pass
                    i = 1
                    cartas_opp = []
                    for card_opp in opponent["cards"]:
                        if i < 9:
                            cartas_opp.append(card_opp["name"])
                    cartas_opp = sorted(cartas_opp)
                date = datetime.datetime(int(battle_time[:4]), int(battle_time[4:6]), int(battle_time[6:8]), int(battle_time[9:11]), int(battle_time[11:13]), int(battle_time[13:15]))
                sql = "INSERT IGNORE INTO battlelog (id, time_stamp, game_date, game_mode, name_team, tag_team, name_clan_team, card1_team, card2_team, card3_team, card4_team, card5_team, card6_team, card7_team, card8_team, crowns_team, crowns_opp, name_opp, tag_opp, name_clan_opp, card1_opp, card2_opp, card3_opp, card4_opp, card5_opp, card6_opp, card7_opp, card8_opp) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                values = (id_battle, battle_time, date, game_mode, name_team, tag_id_team, name_clan_team, cartas_team[0], cartas_team[1], cartas_team[2], cartas_team[3], cartas_team[4], cartas_team[5], cartas_team[6], cartas_team[7], crowns_team, crowns_opp, name_opp, tag_id_opp, name_clan_opp, cartas_opp[0], cartas_opp[1], cartas_opp[2], cartas_opp[3], cartas_opp[4], cartas_opp[5], cartas_opp[6], cartas_opp[7])
                cursor.execute(sql, values)
                db_connection.commit()


main()