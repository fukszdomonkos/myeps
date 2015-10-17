__author__ = 'fuksz'

import argparse
import requests
from bs4 import BeautifulSoup
import datetime
import json

#Parsing arguments
parser = argparse.ArgumentParser()
parser.add_argument("-u","--username",
                    help="Specifies the username",
                    type=str,
                    required=True)
parser.add_argument("-p","--password",
                    help="Specifies the password",
                    type=str,
                    required=True)
args = parser.parse_args()
username = args.username
password = args.password

base_url = "http://www.myepisodes.com"

login_data = {'username': username, 'password': password, 'action': 'Login', 'u': ''}
with requests.Session() as s:
    r_login = s.post(base_url + "/login.php", data=login_data)
    r_wasted = s.get(base_url + "/timewasted/")
    wasted_html = r_wasted.text

    soup = BeautifulSoup(wasted_html, 'html.parser')
    wasted_table = soup.select("table.mylist tr")

    wasted_headers = wasted_table[0].select("th")
    wasted_header_names = []
    for idx, header in enumerate(wasted_headers):
            wasted_header_names.append(header.get_text())

    wasted_total = wasted_table[len(wasted_table)-1].select("th")[6].get_text()


    wasted_data = [];
    for idx, wasted_row in enumerate(wasted_table):
        if (idx > 0) and (idx < len(wasted_table) - 1):
            wasted_row_columns = wasted_row.select("td");
            row_data = {}
            for idx_col, wasted_row_column in enumerate(wasted_row_columns):
                if (idx_col > 0):
                    if (idx_col == 1):
                        url = wasted_row_column.a.get('href')
                        row_data["url"] = url
                    header_name = wasted_header_names[idx_col]
                    row_data[header_name] = wasted_row_column.get_text()
            wasted_data.append(row_data)

    wasted_all = {"shows": wasted_data, "total": wasted_total}

    all_show_data = [];
    for idx, wasted_data_row in enumerate(wasted_data):
        if(idx < 2):
            show_url = base_url + wasted_data_row['url']
            r_show = s.get(show_url);
            show_html = r_show.text
            soup = BeautifulSoup(show_html, 'html.parser')
            show_table = soup.select("table.mylist tr")

            show_headers = show_table[0].select("th")
            show_header_names = []
            for header in show_headers:
                show_header_names.append(header.get_text())

            show_data = [];
            for idx, show_row in enumerate(show_table):
                if (idx > 0):
                    show_row_columns = show_row.select("td");
                    if (len(show_row_columns) > 1):
                        row_data = {}
                        for idx_col, show_row_column in enumerate(show_row_columns):
                            header_name = show_header_names[idx_col]
                            if (idx_col == 4) or (idx_col == 5):
                                if (show_row_column.input.get("checked") == ""):
                                    row_data[header_name] = True
                                else:
                                    row_data[header_name] = False
                            else:
                                row_data[header_name] = show_row_column.get_text()
                        show_data.append(row_data)

            all_show_data.append(show_data);

    all_data = {"wasted": wasted_all, "shows": all_show_data};

    # print(all_data)

filename = "myeps_" + username + "_" + datetime.datetime.now().strftime("%Y.%m.%d_%H.%M.%S") + ".json"

with open("output/" + filename, 'w') as output:
    output.write(json.dumps(all_data,indent=4, separators=(',', ': ')))