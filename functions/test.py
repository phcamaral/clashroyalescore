import requests
import mysql.connector
from mysql.connector import errorcode
import datetime
import schedule
import time

headers = {
    "Content-type": "application/json",
    "Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjY5MGFhOTczLTBkZGItNDhiZC1hMDZmLTkwNTMwOTM4NzZiZSIsImlhdCI6MTcwNzE3NTY2NCwic3ViIjoiZGV2ZWxvcGVyLzc1MDJkNGRlLTI2YWEtZjhjMS0wMDRmLWVmZWJjYWFmODVlNSIsInNjb3BlcyI6WyJyb3lhbGUiXSwibGltaXRzIjpbeyJ0aWVyIjoiZGV2ZWxvcGVyL3NpbHZlciIsInR5cGUiOiJ0aHJvdHRsaW5nIn0seyJjaWRycyI6WyI0NS43OS4yMTguNzkiXSwidHlwZSI6ImNsaWVudCJ9XX0.HNmCO6end3HxRkhkssTqK2-ZSVXEXQhUcfEuO2vH70vAWPvokFfulZK4WdjHtNbnf72J4ZSmOZb9Av3pV62VSw",
}

db_connection = mysql.connector.connect(user="remote", database="clashroyale", port=3306)
cursor = db_connection.cursor()

def main():
    tags_id = verify_tags()
    print(tags_id)

def verify_tags():
    sql = "select distinct tag_team, tag_opp from battlelog;"
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

main()