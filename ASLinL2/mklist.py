#! /usr/bin/python3.9

import sys
# import exrex
import subprocess

services = {}

# longueur de 15 caractères
# lettres majuscules (au moins 3), 
# minuscules et chiffres (au moins 3). 
# pas de caractères spéciaux.
password_regex = r"^(?=[a-z0-9]{3})(?=[A-Z]{3})[a-zA-Z0-9]{9}$"

# hash_password_cmd = "slappasswd -s"

if len(sys.argv) < 2:
    print("Veuillez specifier le fichier csv")
    sys.exit()

def add_count(service):
    count = services.get(service, 0)
    if count == 0:
        services[service] = 1
    else:
        services[service] += 1
    return count + 1

def build_login(service):
    # build the prefix from service and count
    first_letter = service[0]
    last_letter = service[len(service) - 1]
    prefix = f"{first_letter}{last_letter}".lower()

    # add count to prefix
    count = services[service] 
    for i in range(4 - len(f"{count}")):
        prefix += "0"
    
    return f"{prefix}{count}"

# def generate_password(use_default):
#     password = "Passw0rd"
#     # generate plain text on regex
#     if not use_default : password = exrex.getone(password_regex)
#     # Hash the password
#     return hash_password(password)

# def hash_password(password):
#     hashed_password = subprocess.run(f"{hash_password_cmd} {password}", stdout=subprocess.PIPE, shell=True)
#     hashed_password = hashed_password.stdout.decode().rstrip()
#     return hashed_password

def generate_password_2(use_default):
    password = "Passw0rd"
    # generate plain text
    if not use_default : 
        password = subprocess.run(f"mkpasswd -l 20 -d 3 -c 3 -s 0 -C 3", stdout=subprocess.PIPE, shell=True)
        password = password.stdout.decode().rstrip()
    return password

# Read the line
with open(sys.argv[1]) as fichier:
    # for each line 
    for ligne in fichier:
        # Split the line
        entry = ligne.rstrip().split(";")
        # If all data are present 
        if len(entry) < 3: continue
        # increment the count of user in service and get the new count 
        new_count = add_count(entry[2])
    
        # build prefix 
        login = build_login(entry[2])
        # build password 
        password = generate_password_2(new_count == 1)

        # add to entry
        entry.append(login)
        entry.append(password)

        # join on ;
        new_line = ";".join(entry)
    
        print(new_line)