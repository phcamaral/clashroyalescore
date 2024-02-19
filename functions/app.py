from flet import *
from firebase_admin import credentials
from firebase_admin import firestore
import firebase_admin

# Use the application default credentials.
cred = credentials.Certificate("clash-royale-score-firebase-adminsdk-vf7x5-60c466301c.json")

firebase_admin.initialize_app(cred)
db = firestore.client()


def main(page: Page):
    page.title = "Pedro Amaral Analysis"
    page.scroll = "auto"

    def search(e):
        tag_required = tag.value

        if not tag.value:
            tag.error_text = "Please, insert a tag"
            page.update()
        else:
            page.clean()
            docs = db.collection('Battles').where('tag_player', '==', tag_required).get()
            for doc in docs:
                result = doc.to_dict()
                player = result['name_player']
                page.add(
                    Row(
                        controls=[Text(value=player)], alignment="center"
                    )
                )
                #page.add(Image(src=f"icons/{result['card1_team']}.png", width=100, height=100, fit=ImageFit.CONTAIN))
    
    tag = TextField(label="Insert tag")

    page.add(
        tag,
        ElevatedButton("Search", on_click=search)
    )

app(target=main, assets_dir="icons")