import logging
import random

from Utils.send_notif import send_notif

def send_notification_attack(s, attack: tuple):
    logger = logging.getLogger("app")
    
    cible = attack[0]
    attaquant = attack[1]
    timestamp = attack[2]

    joueurs_discord = {
        "Arracheuse2GrandMere": "1324501678698922077",
        "Tete": "1443599635682689204",
        "Dreams": "1281515951799537737",
        "404": "1007946209408843787",
        "Aniel": "646019813650726923",
        "Peregrin": "422382190161166337",
        "YoyanVLR": "1312081273069502476",
        "Bobino": "1546565554930843668",
        "DB2": "1426603030433759465",
        "Hugo H": "1387097300538490911",
        "Isken Yami No Rei": "1188595252500643860",
        "Nana": "725073001707732999",
        "Raph la Casse": "1544390579448848426",
        "Thefarmeur": "1321973124870307901"
    }

    discord_id = joueurs_discord.get(cible)
    cible_mention = f"<@{discord_id}>" if discord_id else cible

    data = {
        "username": "Nan mais c'est okay",
        "avatar_url": "https://i.etsystatic.com/47531348/r/il/e93c9c/5929905166/il_fullxfull.5929905166_s0kn.jpg",
        "embeds": [{
            "title": "On se fait attaquer !",
            "color": 5254336,
            "fields": [
                {
                    "name": "Victime",
                    "value": cible_mention,
                    "inline": False
                },
                {
                    "name": "Attaquant",
                    "value": attaquant,
                    "inline": False
                },
                {
                    "name": "Arrivée des troupes à",
                    "value": f"<t:{timestamp}:T>",
                    "inline": False
                }
            ],
            "image": {
                            "url": random.choice(["https://c.tenor.com/WcSr_LjrLfoAAAAd/tenor.gif", "https://c.tenor.com/TMhnW8cH10gAAAAC/tenor.gif", "https://images3.memedroid.com/images/UPLOADED810/660ab27b128e6.jpeg", "https://images7.memedroid.com/images/UPLOADED222/603948c0d345b.jpeg", "https://images3.memedroid.com/images/UPLOADED684/625dc26add1fd.jpeg", "https://images7.memedroid.com/images/UPLOADED767/66cc892f48fc3.jpeg", "https://c.tenor.com/DXUlofTJe9oAAAAC/tenor.gif"])
                        }
        }]
    }

    
    logger.debug("Sent with status code " + str(send_notif(data=data)))