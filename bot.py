from mastodon import Mastodon
from dotenv import load_dotenv
from pathlib import Path
import os
import time

load_dotenv()

INSTANCE_BASE = os.getenv('INSTANCE_BASE')
CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
ACCESS_TOKEN = os.getenv('ACCESS_TOKEN')
WELCOME_MESSAGE = os.getenv('WELCOME_MESSAGE', 'Welcome to the instance, @{username}!')
MESSAGE_VISIBILITY = os.getenv('MESSAGE_VISIBILITY', 'unlisted')
WAIT_TIME = int(os.getenv('WAIT_TIME', 300))
IS_DOCKER = os.getenv('IS_DOCKER', False)


def contains_local_account(accounts):
    for account in accounts:
        if account.username == account.acct:
            return True
    return False

def is_local_account(account):
    return account.username == account.acct

def send_welcome_message(mastodon, account):
    formatted_message = WELCOME_MESSAGE.format(username=account.username, useracct=account.acct)
    mastodon.status_post(formatted_message)

last_id_file = Path('.') / 'last_id.txt'
last_id = 0

if IS_DOCKER:
    last_id_file = Path('/data') / 'last_id'
if last_id_file.is_file():
    with open(last_id_file) as f:
        print(int(f.read()))

print('Botvenon is starting...')
print('Welcoming any users after id %d' % last_id)

mastodon = Mastodon(
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN,
    api_base_url=INSTANCE_BASE)

user = mastodon.account_verify_credentials()  # Get the current user

followers = mastodon.account_followers(user)  # Get the latest followers


# print(
#     f'''Followed by: {account.username}
# (Acct value: {account.acct}, id: {account.id})''')

while True:
    for account in mastodon.account_followers(user):
        if is_local_account(account) and account.id > last_id and not account.bot:
            last_id = account.id
            with open(last_id_file, 'w+') as f:
                f.write(str(last_id))
            print('Welcoming %s...' % account.username)
            send_welcome_message(mastodon, account)
    time.sleep(WAIT_TIME)
