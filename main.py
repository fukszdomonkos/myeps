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
parser.add_argument("-J", "--json",
                    help="Export to JSON",
                    action="store_true")
parser.add_argument("-X", "--xlsx",
                    help="Export to Excel",
                    action="store_true")
parser.add_argument("-H", "--html",
                    help="Export to HTML",
                    action="store_true")
args = parser.parse_args()
username = args.username
password = args.password
export_to_json = args.json
export_to_xlsx = args.xlsx
export_to_html = args.html

all_data = get_myeps_data(username, password)

save(all_data, username, to_json=export_to_json, to_xlsx=export_to_xlsx, to_html=export_to_html)
