# Créer le script mkquota.py qui, en se basant sur le fichier des utilisateurs (voir leçons
# précédentes), ajoutera les quotas suivants :
# a. Les membres du service Compta auront un quota de 130 Mo
# b. Les membres du service Soins auront un quota de 140 Mo
# c. Les membres des autres services auront un quota fixé à 200 Mo
# Vérifier, avec l’option report, que ces quotas sont effectivement bien configurés.

import subprocess

CMD_ADD_USER_QUOTA = "xfs_quota -x -c 'limit bhard=<limit>m <uid>' /home"

with open("liste-login-pass.csv", "r") as file:
    for line in file:
        array = line.split(";")
        uid = array[3]
        service = array[2]
        limit = 200

        if service == "Compta":
            limit = 130
        elif service == "Soins":
            limit = 140
        
        subprocess.run(CMD_ADD_USER_QUOTA.replace('<limit>', str(limit)).replace('<uid>', uid), shell=True)