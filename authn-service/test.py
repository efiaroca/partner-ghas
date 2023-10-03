import json
import requests
import csv
import pandas as pd
import logging
import getpass
import datetime
import re

today = datetime.date.today()

CGRE = "\33[92m"
CEND = "\33[0m"
CRED = "\33[91m"
CBLU = "\33[34m"
CBLU2 = "\33[94m"
CYELL = "\33[93m"
CBOLD = "\33[1m"

# Prompt the user whether they want to tail the log
tail_log = input(f"Do you want to tail debug log? ({CYELL}\"y\"{CEND}/{CYELL}\"n\"{CEND}):")
# Set up logging
if tail_log in {"y","Y"}:
    print(f"Log will be tailed.... but also saved to{CYELL}{CBOLD}'{today}_groups_bulk_remove_users.log'{CEND}")
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    logging.basicConfig(handlers=[logging.FileHandler(f"logs/{today}_groups_bulk_remove_users.log"), console_handler],format="[ %(asctime)s ]-[ %(process)d ]-[ %(levelname)s ]-[ %(message)s ]", level=logging.DEBUG)

else:
    print(f"OK, will only be logging to {CYELL}{CBOLD}'{today}_projects_bulk_delete.log'{CEND} then...")
    file_log = logging.basicConfig(filename=f"logs/{today}_groups_bulk_remove_users.log",format="[ %(asctime)s ]-[ %(process)d ]-[ %(levelname)s ]-[ %(message)s ]",level=logging.DEBUG)

user_email = input(f"Enter your {CBOLD}{CBLU2}email{CEND}{CEND}:\n")
api_token = getpass.getpass(f"Enter your {CBOLD}{CBLU2}API-Token{CEND}{CEND}:\n", stream=None)
site_url = input(f"Enter {CBOLD}{CBLU2}Site URl{CEND}{CEND}  e.g {CBOLD}{CBLU2}https://jira.example.com{CEND}{CEND}:\n")
group_name = input(f"Enter {CBOLD}{CBLU2}group name{CEND}{CEND} to remove users from:\n")
site = re.search(r'//(.*?)\.', site_url).group(1)


group_name = "IDP-Developers"

user_email = "snoop.snaap@clap.com"
api_token ="AIUqeXTZfssfi1rg5eudt4B77"
site_url = "https://site.atlassian.net"

# Create a new session
s = requests.Session()
s.auth = (user_email,api_token)
s.get(f"{site_url}/rest/api/3/myself")

# Getting displayname

s_r = s.get(f"{site_url}/rest/api/3/myself")
user_details = s_r.json()
a_display_name = user_details["displayName"]
print(f"Greetings {CBOLD}{CBLU2}{a_display_name}{CEND}! Have fun removing all users from {group_name}!")
f_n = a_display_name.split()
a_display_name = f_n[0]

all_members=[]
members_to_remove = []
def get_all_members():
    start_at = 0
    max_result = 50
    while True:
        url = f"{site_url}/rest/api/3/group/member?groupname={group_name}&includeInactiveUsers=true&startAt={start_at}&maxResult{max_result}"

        response = s.get(url)

        response = response.json()

        print(f"{CBLU}{len(all_members)}{CEND} users added to {CYELL}{CBOLD}'CSV-file'{CEND}!")

        all_members.extend(response["values"])
        if response["isLast"] == True:
            break
        start_at = start_at + max_result

        print(response)

    for user in all_members:

        account_id = user["accountId"]
        display_name = user["displayName"]
        active = user["active"]
        #email = user["emailAddress"]
        members_to_remove.append([account_id, display_name, active])
    filname = f"exports/{today}__{a_display_name}_{group_name}_{len(members_to_remove)}.csv"
    df = pd.DataFrame(members_to_remove, columns=["Account ID", "Display Name", "Active"]).to_csv(filname, index= False)



get_all_members()



