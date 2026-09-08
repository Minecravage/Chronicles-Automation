from bs4 import BeautifulSoup
import asyncio
import time
import os
import logging

attaques_deja_envoyees = {}


async def notifications_attaques(s):
    while True:
        logger = logging.getLogger("app")

        try:
            logger.debug("Starting notif func...")

            r = s.get("https://chronicles20.be/alliance.php")

            logger.debug("Parsing of response")

            soup = BeautifulSoup(r.text, "html.parser")

            attaques = soup.find_all(
                "div",
                id=lambda x: x and x.startswith(
                    "afficher_decompte_attaque_subie_encours_"
                )
            )

            for compte in attaques:
                logger.debug("Attack found. Preparing infos...")

                attaque_id = compte["id"].split("_")[-1]

                bloc_attaque = compte.find_previous("div")
                noms = bloc_attaque.find_all("b")

                if len(noms) < 2:
                    continue

                cible = noms[0].get_text(strip=True)

                joueurs_discord = {
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

                attaquant = noms[1].get_text(strip=True)

                input_timestamp = soup.find(
                    "input",
                    id=f"heure_arrivee_attaque_subie_encours_{attaque_id}"
                )

                if not input_timestamp:
                    continue

                timestamp = int(input_timestamp["value"])

                identifiant = (cible, attaquant, timestamp)

                if identifiant in attaques_deja_envoyees:
                    continue

                # On mémorise l'attaque avec son timestamp
                attaques_deja_envoyees[identifiant] = timestamp

                data = {
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
                        ]
                    }]
                }

                logger.debug("Sending...")

                s.post(
                    str(os.getenv("WEBHOOK_DISCORD")),
                    json=data
                )

                logger.debug("Sent !")

            logger.debug("End of notif func")

            await asyncio.sleep(10)

        except Exception as e:
            logger.warning(f"Error in notif func: {e}")
            await asyncio.sleep(10)


async def clear_cache():
    global attaques_deja_envoyees

    while True:
        logger = logging.getLogger("app")

        try:
            logger.debug("Starting wiping cache func...")

            maintenant = int(time.time())

            attaques_deja_envoyees = {
                identifiant: timestamp
                for identifiant, timestamp in attaques_deja_envoyees.items()
                if timestamp > maintenant
            }

            logger.debug("End of wiping cache func")

        except Exception as e:
            logger.warning(f"Error in wiping cache func: {e}")

        await asyncio.sleep(3600)