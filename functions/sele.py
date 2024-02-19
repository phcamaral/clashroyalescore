from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import datetime
import sys
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# Use the application default credentials.
cred = credentials.Certificate("clash-royale-score-firebase-adminsdk-vf7x5-60c466301c.json")

firebase_admin.initialize_app(cred)
db = firestore.client()

def main():
    tag = ["RJ88Y8U08", "8LJ92G8UG", "9CPCC890", "9G28ULYR"]
    acess_link(tag)

def acess_link(tag):
    for t in tag:
        tag_team = t
        op = webdriver.ChromeOptions()
        op.add_argument("headless")
        op.add_argument('--disable-gpu')
        op.add_argument('--no-sandbox')
        op.add_argument('--disable-setuid-sandbox')
        op.add_argument('--disable-dev-shm-usage')
        driver = webdriver.Chrome(options=op)
        #acessando o link da página
        link = f"https://royaleapi.com/player/{t}/battles/history?"
        driver.get(link)

        while True:
            for i in range(1, 11):
                dict = {}
                try:
                    #tentando pegar o modo de jogo
                    game_mode = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[1]/div[2]/h4").text
                except:
                    try:
                        i += 1
                        #caso haja uma div em oculto
                        game_mode = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[1]/div[2]/h4").text
                    except:
                        i = i - 2
                        break
                # verificando o modo de jogo
                if game_mode in ["1v1", "Ranked1v1", "Gold Rush", "Ladder", "1v1 Battle", "Grand Challenge", "Classic Challenge", "Global Tournament", "Normal Battle"]:
                    #coletando informações
                    link_cards_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[1]/div[3]")
                    name_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[1]/div[1]/div/div/a").text
                    name_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[2]/div[1]/div/div/a").text
                    link_cards_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[2]/div[3]")
                    tag_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[2]/div[1]/div/div/a").get_attribute("href").split("/")
                    crown_team, crown_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[1]/div[2]/div[1]").text.split(" - ")
                    time_ago = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[1]").text
                    timestamp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[1]")
                    match_id = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]")
                    match_id = match_id.get_attribute("id")
                    id_battle = match_id + tag_team
                    date = timestamp.get_attribute("data-content")
                    date = date[:-4]
                    try:
                        tower_team = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[1]/a/div/div").text
                    except:
                        tower_team = ""
                    try:
                        tower_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div[2]/a/div/div").text
                    except:
                        tower_opp = ""
                    try:
                        name_clan_team = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[1]/div[{i}]/div[1]/div[1]/div/div/div[1]/a").text
                        tag_clan_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[1]/div[{i}]/div[1]/div[1]/div/div/div[1]/a" ).get_attribute("href").split("/")
                        tag_clan_team = tag_clan_team[4]
                    except:
                        name_clan_team = ""
                        tag_clan_team = ""
                    try:
                        name_clan_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[4]/div[4]/div/div[1]/div[{i}]/div[2]/div[1]/div/div/div[1]/a").text
                        tag_clan_opp= driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[4]/div[4]/div/div[1]/div[{i}]/div[2]/div[1]/div/div/div[1]/a" ).get_attribute("href").split("/")
                        tag_clan_opp = tag_clan_opp[4]
                    except:
                        tag_clan_opp = ""
                        name_clan_opp = ""
                    
                    cards_team = link_cards_team.get_attribute("id")
                    cards_opp = link_cards_opp.get_attribute("id")
                    #colocando as cartas em ordem alfabética
                    cards_team = cards_team[5:]
                    cards_opp = cards_opp[5:]
                    tag_opp = tag_opp[4]
                    cards_team = cards_team.split(",")
                    cards_opp = cards_opp.split(",")
                    #verificando se foi vitória, derrota ou empate
                    if int(crown_team) > int(crown_opp):
                        result = "W"
                    elif int(crown_team) < int(crown_opp):
                        result = "L"
                    else:
                        result = "D"
                    match_duels = "0"
                    dict = {
                    'id_battle' : id_battle,
                    'name_player' : name_team,
                    'date' : date,
                    'tag_player' : tag_team,
                    'name_clan_team' : name_clan_team,
                    'tag_clan_team' : tag_clan_team,
                    'game_mode' : game_mode,
                    'match_duels' : match_duels,
                    'tower' : tower_team,
                    'card1_team' : cards_team[0],
                    'card2_team' : cards_team[1],
                    'card3_team' : cards_team[2],
                    'card4_team' : cards_team[3],
                    'card5_team' : cards_team[4],
                    'card6_team' : cards_team[5],
                    'card7_team' : cards_team[6],
                    'card8_team' : cards_team[7],
                    'crown_team' : crown_team,
                    'crown_opp' : crown_opp,
                    'name_opp' : name_opp,
                    'tag_opp' : tag_opp,
                    'name_clan_opp' : name_clan_opp,
                    'tag_clan_opp' : tag_clan_opp,
                    'tower_opp' : tower_opp,
                    'card1_opp' : cards_opp[0],
                    'card2_opp' : cards_opp[1],
                    'card3_opp' : cards_opp[2],
                    'card4_opp' : cards_opp[3],
                    'card5_opp' : cards_opp[4],
                    'card6_opp' : cards_opp[5],
                    'card7_opp' : cards_opp[6],
                    'card8_opp' : cards_opp[7],
                    }

                    doc_ref = db.collection('Battles').document(id_battle)
                    doc_ref.set(dict)    
                
                #verificação duel
                elif game_mode == "Duel":
                    #verificando a primeira partida do modo duel
                    link_cards_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[1]/div[3]")
                    name_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[1]/div[1]/div/div/a").text
                    name_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[2]/div[1]/div/div/a").text
                    link_cards_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[2]/div[3]")
                    tag_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[2]/div[1]/div/div/a").get_attribute("href").split("/")
                    crown_team, crown_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[2]/div/div[2]").text.split(" - ")
                    match_id = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]")
                    match_id = match_id.get_attribute("id")
                    match_duels = "1"
                    id_battle = match_id + tag_team + match_duels
                    time_ago = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[3]/div[1]").text
                    crown_general_team, crown_general_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[1]/div[2]/div[1]").text.split(" - ")
                    if (int(crown_general_team) - int(crown_general_opp)) == 2 or (int(crown_general_team) - int(crown_general_opp)) == -2:
                        timestamp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[10]/div[1]")
                        date = timestamp.get_attribute("data-content")
                    else:
                        timestamp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[14]/div[1]")
                        date = timestamp.get_attribute("data-content")
                    date = date[:-4]
                    cards_team = link_cards_team.get_attribute("id")
                    cards_team = cards_team[5:]
                    cards_team = cards_team.split(",")
                    cards_opp = link_cards_opp.get_attribute("id")
                    tag_opp = tag_opp[4]
                    #colocando as cartas em ordem alfabética
                    cards_opp = cards_opp[5:]
                    cards_opp = cards_opp.split(",")
                    dict = {
                    'id_battle' : id_battle,
                    'name_player' : name_team,
                    'date' : date,
                    'tag_player' : tag_team,
                    'name_clan_team' : name_clan_team,
                    'tag_clan_team' : tag_clan_team,
                    'game_mode' : game_mode,
                    'match_duels' : match_duels,
                    'tower' : tower_team,
                    'card1_team' : cards_team[0],
                    'card2_team' : cards_team[1],
                    'card3_team' : cards_team[2],
                    'card4_team' : cards_team[3],
                    'card5_team' : cards_team[4],
                    'card6_team' : cards_team[5],
                    'card7_team' : cards_team[6],
                    'card8_team' : cards_team[7],
                    'crown_team' : crown_team,
                    'crown_opp' : crown_opp,
                    'name_opp' : name_opp,
                    'tag_opp' : tag_opp,
                    'name_clan_opp' : name_clan_opp,
                    'tag_clan_opp' : tag_clan_opp,
                    'tower_opp' : tower_opp,
                    'card1_opp' : cards_opp[0],
                    'card2_opp' : cards_opp[1],
                    'card3_opp' : cards_opp[2],
                    'card4_opp' : cards_opp[3],
                    'card5_opp' : cards_opp[4],
                    'card6_opp' : cards_opp[5],
                    'card7_opp' : cards_opp[6],
                    'card8_opp' : cards_opp[7],
                    }

                    doc_ref = db.collection('Battles').document(id_battle)
                    doc_ref.set(dict)
                    #verificando a segunda partida do modo duel
                    link_cards_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[7]/div[1]/div[3]")
                    link_cards_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[7]/div[2]/div[3]")
                    crown_team, crown_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[6]/div/div[2]").text.split(" - ")
                    cards_opp = link_cards_opp.get_attribute("id")
                    cards_team = link_cards_team.get_attribute("id")
                    cards_team = cards_team[5:]
                    cards_team = cards_team.split(",")
                    cards_opp = cards_opp[5:]
                    cards_opp = cards_opp.split(",")
                    match_duels = "2"
                    id_battle = match_id + tag_team + match_duels
                    dict = {
                        'id_battle' : id_battle,
                        'name_player' : name_team,
                        'date' : date,
                        'tag_player' : tag_team,
                        'name_clan_team' : name_clan_team,
                        'tag_clan_team' : tag_clan_team,
                        'game_mode' : game_mode,
                        'match_duels' : match_duels,
                        'tower' : tower_team,
                        'card1_team' : cards_team[0],
                        'card2_team' : cards_team[1],
                        'card3_team' : cards_team[2],
                        'card4_team' : cards_team[3],
                        'card5_team' : cards_team[4],
                        'card6_team' : cards_team[5],
                        'card7_team' : cards_team[6],
                        'card8_team' : cards_team[7],
                        'crown_team' : crown_team,
                        'crown_opp' : crown_opp,
                        'name_opp' : name_opp,
                        'tag_opp' : tag_opp,
                        'name_clan_opp' : name_clan_opp,
                        'tag_clan_opp' : tag_clan_opp,
                        'tower_opp' : tower_opp,
                        'card1_opp' : cards_opp[0],
                        'card2_opp' : cards_opp[1],
                        'card3_opp' : cards_opp[2],
                        'card4_opp' : cards_opp[3],
                        'card5_opp' : cards_opp[4],
                        'card6_opp' : cards_opp[5],
                        'card7_opp' : cards_opp[6],
                        'card8_opp' : cards_opp[7],
                        }
                    doc_ref = db.collection('Battles').document(id_battle)
                    doc_ref.set(dict)
                    
                    try:
                        #verificando se há uma terceira partida do modo duel
                        link_cards_team = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[11]/div[1]/div[3]")
                        link_cards_opp = driver.find_element("xpath",f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[11]/div[2]/div[3]")
                        crown_team, crown_opp = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]/div[10]/div/div[2]").text.split(" - ")
                        cards_opp = link_cards_opp.get_attribute("id")
                        cards_team = link_cards_team.get_attribute("id")
                        cards_team = cards_team[5:]
                        cards_team = cards_team.split(",")
                        cards_opp = cards_opp[5:]
                        cards_opp = cards_opp.split(",")
                        match_duels = "3"
                        id_battle = match_id + tag_team + match_duels
                        dict = {
                        'id_battle' : id_battle,
                        'name_player' : name_team,
                        'date' : date,
                        'tag_player' : tag_team,
                        'name_clan_team' : name_clan_team,
                        'tag_clan_team' : tag_clan_team,
                        'game_mode' : game_mode,
                        'match_duels' : match_duels,
                        'tower' : tower_team,
                        'card1_team' : cards_team[0],
                        'card2_team' : cards_team[1],
                        'card3_team' : cards_team[2],
                        'card4_team' : cards_team[3],
                        'card5_team' : cards_team[4],
                        'card6_team' : cards_team[5],
                        'card7_team' : cards_team[6],
                        'card8_team' : cards_team[7],
                        'crown_team' : crown_team,
                        'crown_opp' : crown_opp,
                        'name_opp' : name_opp,
                        'tag_opp' : tag_opp,
                        'name_clan_opp' : name_clan_opp,
                        'tag_clan_opp' : tag_clan_opp,
                        'tower_opp' : tower_opp,
                        'card1_opp' : cards_opp[0],
                        'card2_opp' : cards_opp[1],
                        'card3_opp' : cards_opp[2],
                        'card4_opp' : cards_opp[3],
                        'card5_opp' : cards_opp[4],
                        'card6_opp' : cards_opp[5],
                        'card7_opp' : cards_opp[6],
                        'card8_opp' : cards_opp[7],
                        }
                        doc_ref = db.collection('Battles').document(id_battle)
                        doc_ref.set(dict)
                    except:
                        pass

                else:
                    match_id = driver.find_element("xpath", f"/html/body/div[3]/div[4]/div[2]/div[6]/div[{i}]")
                    match_id = match_id.get_attribute("id")
                    
            driver.get(link + "before=" + match_id[7:-2] + "000&&")

#def insert_sql():

main()