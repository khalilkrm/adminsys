#! /usr/bin/python3.9

import sys
import subprocess

# Constants
create_ldap_user_cmd = "ldapadd -D 'cn=Directory Manager,dc=localdomain' -f {0} -x -w rootroot"
set_permissions_on_user_directory_cmd = "install -o {0} -g {1} -m 0700 -d /home/{0}"
search_ldap_user_cmd = "ldapsearch -LLL -x -b 'dc=localdomain' '(|(uid={0})(cn=Directory Manager))'"
options = ["--password", "--givenname", "--sn", "--uid", "--uidnumber"]

if len(sys.argv) < 11 :
    print("mkglobal_user.py : Missed option or argument for option")
    sys.exit()

for index in range(1,len(sys.argv)-1, 2):
    if not sys.argv[index] in options:
        print(f"invalid option -- '{sys.argv[index]}'")
        sys.exit()

def get_argv(option):
    if not option in options:
        print(f"Unknown option '{option}'")
    index = sys.argv.index(option)
    return sys.argv[index+1]

def hash_passwd(plain):
    hashed = subprocess.run(f"slappasswd -s {plain.rstrip()}", stdout=subprocess.PIPE, shell=True)
    return hashed.stdout.decode().rstrip()

def is_user_directory_exist(uid):
    count = subprocess.run(f"ls /home | grep '{uid}' | wc -l", stdout=subprocess.PIPE, shell=True)
    return int(count.stdout.decode().strip()) > 0

with open("user.ldip", "w") as file:
    file.write(f"dn: uid={get_argv('--uid')},ou=People,dc=localdomain\n")
    file.write("objectClass: top\n")
    file.write("objectClass: inetorgperson\n")
    file.write("objectClass: posixAccount\n")
    file.write(f"cn: {get_argv('--givenname')} {get_argv('--sn')}\n")
    file.write(f"sn: {get_argv('--sn')}\n")
    file.write(f"givenname: {get_argv('--givenname')}\n")
    file.write(f"userPassword: {hash_passwd(get_argv('--password'))}\n")
    file.write(f"gidNumber: {100}\n")
    file.write(f"uidNumber: {get_argv('--uidnumber')}\n")
    file.write(f"homeDirectory: /home/{get_argv('--uid')}\n")
    file.write("loginShell: /bin/bash\n")


# Create LADP user
subprocess.run(create_ldap_user_cmd.format("user.ldip"), shell=True)

# Check user directory existance
if is_user_directory_exist(get_argv('--uid')) : 
    print('User directory already exist')
else: 
    # Create user directory
    subprocess.run(f"mkdir /home/{get_argv('--uid')}", shell=True)
    # Set owner and permissions
    subprocess.run(set_permissions_on_user_directory_cmd.format(get_argv('--uid'), 'users'), shell=True)
    if is_user_directory_exist(get_argv('--uid')) : 
        print('User directory created')
    else: print('User directory could not be created')
