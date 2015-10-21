__author__ = 'fukszdomonkos'

import argparse
from myeps import get_myeps_data, save

parser = argparse.ArgumentParser()
parser.add_argument("-u", "--username",
                    help="Specifies the username",
                    type=str,
                    required=True)
parser.add_argument("-p", "--password",
                    help="Specifies the password",
                    type=str,
                    required=True)
args = parser.parse_args()
username = args.username
password = args.password

all_data = get_myeps_data(username, password)

save(all_data, username, to_json=True)
