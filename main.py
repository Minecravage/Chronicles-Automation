import requests
from dotenv import load_dotenv
import sys
import os
import asyncio

from Core.Observation.notif import notifications_attaques
from Core.Action_OG.send_attack_notification import send_notification_attack
from Core.Observation.notif import notifications_attaques

from Utils.logger import create_logger

# Chargement du .env
load_dotenv()

# Création du Logger
print("Starting logger...")
logger = create_logger()
logger.debug("Logger created")

try :

    # On essaie de créer la session
    logger.debug("Creating Session...")
    s = requests.Session()

    # Et de lui ajouter le cookie défini en .env
    logger.debug("Settings cookies...")
    s.cookies.set("PHPSESSID", str(os.getenv("PHPSESSID")))

    # Boucle de fonctionnement
    def logic():
        while True:
            for attack in notifications_attaques(s=s):
                send_notification_attack(s=s, attack=attack)

        
                

            

except KeyboardInterrupt: # Si l'utilisateur fait CTRL+C
    logger.info("Interrupted Program. See you next time !")
    sys.exit(0)

except Exception as e: # Si une autre erreur survient
    logger.critical(f"Erreur : {e}")
    sys.exit(1)
