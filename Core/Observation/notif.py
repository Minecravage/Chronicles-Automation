from bs4 import BeautifulSoup
import asyncio
import time
import os
import logging

attaques_deja_envoyees = {}

def notifications_attaques(s):
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

            attack = []
            attack.append(identifiant)

        logger.debug("End of notif func")
        return attack
        
            
        
    except Exception as e:
        logger.warning(f"Error in notif func: {e}")