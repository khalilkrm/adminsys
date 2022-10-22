#! /usr/bin/python3.9

# constants
import subprocess

uidnumber=30000

created_groups = []

cmd_create_local_user = "useradd -m -g {0} {2}"
cmd_add_passwd = "echo {0} | passwd --stdin {1}"
cmd_hash_string = "slappasswd -s {0}"
cmd_create_local_group = "groupadd {0}"
cmd_add_user_to_group = "/usr/sbin/usermod -a -G {0} {1}"
cmd_add_user_info = "chfn -f '{0}' {1}"
cmd_add_global_user = "/usr/bin/python3.9 mkglobal_user.py --password '{0}' --givenname '{1}' --sn '{2}' --uid '{3}' --uidnumber {4}"

def is_nod(login):
    sliced = login[2:]
    if sliced.isdigit():
        return int(sliced) % 2 == 0

def hash(subject):
    result = subprocess.run(cmd_hash_string.format(subject), stdout=subprocess.PIPE, shell=True)
    result = result.stdout.decode().strip()
    return result

def create_local_group(group):
    if not group in created_groups: 
        subprocess.run(cmd_create_local_group.format(group), shell=True)
        created_groups.append(group)

def create_global_user(
    password,
    givenname,
    sn,
    uid,
    uidnumber):
    subprocess.run(cmd_add_global_user.format(password.rstrip(), givenname, sn, uid, uidnumber), shell=True)

def add_user_info(fullname, username):
    subprocess.run(cmd_add_user_info.format(fullname, username), shell=True)

def create_local_user(username, principalgroup, secondarygroup, password):
    subprocess.run(cmd_create_local_user.format(principalgroup, password, username), shell=True)
    attach_to_group(username, secondarygroup)

def attach_to_group(username, secondarygroup):
    subprocess.run(cmd_add_user_to_group.format(secondarygroup, username), shell=True)

# with open("liste-login-pass.csv", "r") as file:
#     for line in file:
#         entry = line.split(";")
#         if not len(entry) > 4: continue
#         isnod = is_nod(entry[3])
#         if isnod == None: continue
#         if isnod == False:
#             subprocess.run(f"userdel -r {entry[3]}", stdout=subprocess.PIPE, shell=True)
#             if not entry[2].lower() in created_groups:
#                 subprocess.run(f"groupdel {entry[2].lower()}", shell=True)
#                 created_groups.append(entry[2].lower())

with open("liste-login-pass.csv", "r") as file:
    for line in file:
        entry = line.split(";")
        if not len(entry) > 4: continue
        isnod = is_nod(entry[3])
        if isnod == None: continue
        create_local_group(entry[2].lower())
        if isnod == False:
            create_local_user(
                principalgroup="users", 
                secondarygroup=entry[2].lower(), 
                username=entry[3], 
                password=hash(entry[4]))
            subprocess.run(cmd_add_passwd.format(entry[4].strip(), entry[3]), shell=True)
            add_user_info(f"{entry[0]} {entry[1]}", entry[3])
        else:
            create_global_user(
                password=entry[4],
                givenname=entry[1],
                sn="_".join(entry[0].split(" ")),
                uid=entry[3],
                uidnumber=uidnumber
            )
            uidnumber += 1
            attach_to_group(entry[3], entry[2].lower())