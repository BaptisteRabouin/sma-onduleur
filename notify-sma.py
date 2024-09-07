#!/usr/bin/env python
# -*- coding: utf-8 -*-
import smtplib
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate
import requests
import urllib3

# Permet de passer les problèmes liés au certificat https non valide
urllib3.disable_warnings()

# Récupère le code JSON de la page web de l'onduleur.
# Code dynamique qui affiche toutes les 5 secondes l'état de l'appareil.
url = "<IP-inverter>/dyn/getDashValues.json"
r = requests.get(url, verify=False)  # Le "verify=false" vient compléter la ligne 12
# en passant l'étape de danger lié à https

# Ouverture (ou création) d'un fichier en écriture
fichier = open("controleSMA.txt", "w")
# écris le code récupéré dans ce fichier
fichier.write(r.text)
# ferme le fichier
fichier.close()

# Rouvre le fichier en lecture cettte fois.
with open("controleSMA.txt", "r") as f:
    b = f.readline()  # Lis le fichier ligne par ligne
    c = b[273:276]  # récupère l'info précise localisée entre les index 273 et 274
    print(c)
    d = str(c)  # la converti en chaine de caractere pour l'analyser
    if c != '307':  # si l'info récupérée n'est pas égale à 307 alors l'onduleur est en erreur

        server = smtplib.SMTP()
        # server.set_debuglevel(1) # Décommenter pour activer le debug
        server.connect('<your smtp address mail', 25)

        server.helo()

        fromaddr = 'Onduleur <address mail>'
        toaddrs = ['<your address mail>']  # On peut mettre autant d'adresses que l'on souhaite
        sujet = "L'onduleur est en erreur."
        html = u"""\
            <html>
            <head>
            <meta charset="utf-8" />
            </head>
            <body>
            <div>
            Bonjour Baptiste

            L'onduleur présente une erreur, veuillez vérifier que tout aille bien et si possible,
            réenclenchez les panneaux solaires.

            Merci et bonne journée.

            Cordialement,

            Votre SMA
            </div>
            </body
            </html>
            """

        msg = MIMEMultipart('alternative')
        msg['Subject'] = sujet
        msg['From'] = fromaddr
        msg['To'] = ','.join(toaddrs)
        msg["Date"] = formatdate(localtime=True)

        part = MIMEText(html, 'html')
        msg.attach(part)

        try:
            server.sendmail(fromaddr, toaddrs, msg.as_string())
        except smtplib.SMTPException as e:
            print(e)

        server.quit()
        #time.sleep(7200)  # Met en pause le programme pendant 2h le temps que l'onduleur soit remis en état ok.
    else:
        pass
