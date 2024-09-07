# Script qui envoi un email lorsqu'il y a une erreur sur l'onduleur

import smtplib
import emails_config
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import requests
import urllib3

# Envoyer des emails lorsque l'onduleur est en erreur

def recuperer_donnees(url):
    # Fonction qui recupere les donnees de la page web, ici les données Json
    datas = requests.get(url, verify=False)
    return datas


def enregistrer_et_extraction_donnees(datas):
    # Fonction qui ecrit les donnees dans un fichier et extrait la donnee qui nous interesse
    with open("controleSMA.txt", "w") as fichier: # Ouvre le fichier en écriture ou le créer s'il n'existe pas (le "r+" ne fonctionne pas pour créer le fichier, seule le "w" marche)
        fichier.write(datas.text) # Ecris les données dans le fichier
    with open("controleSMA.txt", "r") as fichier: # Ouvre le fichier en lecture
        ligne = fichier.read() # Lis le fichier
        donnee_a_extraire = ligne[273:276]  # récupère l'info précise localisée entre les index 273 et 274
    
    return str(donnee_a_extraire) # Retourne la donnée voulue


def envoyer_email(email_destinataire, sujet, message):
    # Fonction qui envoi un email
    multipart_message = MIMEMultipart()
    multipart_message["Subject"] = sujet
    multipart_message["From"] = emails_config.config_email
    multipart_message["To"] = email_destinataire

    multipart_message.attach(MIMEText(message, "plain"))

    serveur_mail = smtplib.SMTP(emails_config.config_server, emails_config.config_server_port)
    serveur_mail.starttls()
    serveur_mail.login(emails_config.config_email, emails_config.config_password)
    serveur_mail.sendmail(emails_config.config_email, email_destinataire, multipart_message.as_string())
    serveur_mail.quit()



message_email = """Bonjour,

L'onduleur est en erreur !

Merci de consulter les évènements relatifs à l'incident 
directement depuis la page d'accès de l'onduleur.

Cordialement,

Onduleur SMA
"""


urllib3.disable_warnings()  # désactive les alertes liées au https


url = "<IP_INVERTER>/dyn/getDashValues.json"

datas_recuperees = recuperer_donnees(url)
data_extraite = enregistrer_et_extraction_donnees(datas_recuperees)

if data_extraite != "307":
    envoyer_email("<YOUR_EMAIL>", "Erreur sur onduleur", message_email)
else:
    pass
    #envoyer_email("<YOUR_EMAIL>", "TEST pour onduleur", "TEST")

