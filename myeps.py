__author__ = 'fukszdomonkos'

import requests
from bs4 import BeautifulSoup

import datetime
import json


class LoginError(Exception):
    def __init__(self, value=None):
        self.value = value
    def __str__(self):
        return repr(self.value)


class ParseError(Exception):
    def __init__(self, value=None):
        self.value = value

    def __str__(self):
        return repr(self.value)

def get_myeps_data(username, password):
    base_url = "http://www.myepisodes.com"

    if (username == "") or (password == ""):
        raise LoginError()
    login_data = {'username': username, 'password': password, 'action': 'Login', 'u': ''}
    with requests.Session() as s:
        r_login = s.post(base_url + "/login.php?action=login", data=login_data)

        login_error_strings = ["Username not entered", "Password not entered", "Username not found", "Invalid password"]
        if any(login_error_string in r_login.text for login_error_string in login_error_strings):
            raise LoginError()

        r_wasted = s.get(base_url + "/timewasted/")
        wasted_html = r_wasted.text

        soup = BeautifulSoup(wasted_html, 'html.parser')
        wasted_table = soup.select("table.mylist tr")

        wasted_total = wasted_table[len(wasted_table) - 1].select("th")[6].get_text()

        wasted_data = []
        for idx, wasted_row in enumerate(wasted_table):
            if (idx > 0) and (idx < len(wasted_table) - 1):  # Excluding headers
                wasted_row_columns = wasted_row.select("td")
                row_data = {}
                row_data["name"] = wasted_row_columns[1].get_text()
                row_data["url"] = wasted_row_columns[1].a.get('href')
                row_data["status"] = wasted_row_columns[2].get_text()
                row_data["runtime"] = wasted_row_columns[3].get_text()
                row_data["eps"] = wasted_row_columns[4].get_text()
                row_data["mins"] = wasted_row_columns[5].get_text()
                row_data["time_wasted"] = wasted_row_columns[6].get_text()
                wasted_data.append(row_data)

        wasted_all = {"shows": wasted_data, "total": wasted_total}

        all_show_data = []
        for idx, wasted_data_row in enumerate(wasted_data):
            if (idx < 2) or False:  # Limit the number of shows, only for development. Set False to limit.
                show_url = base_url + wasted_data_row['url']
                r_show = s.get(show_url)
                show_html = r_show.text
                soup = BeautifulSoup(show_html, 'html.parser')
                show_table = soup.select("table.mylist tr")

                show_data = []
                for idx, show_row in enumerate(show_table):
                    if idx > 0:  # Exclude main header
                        show_row_columns = show_row.select("td")
                        if len(show_row_columns) > 1:  # Check if it is a real show detail row
                            row_data = {}
                            try:
                                air_date_string = show_row_columns[0].get_text()
                                air_date_date = datetime.datetime.strptime(air_date_string, '%Y-%b-%d')
                                row_data["air_date"] = air_date_date.isoformat()
                                row_data["show_name"] = show_row_columns[1].get_text()
                                epis = show_row_columns[2].get_text()
                                epis_split = epis.split('x')
                                row_data["season"] = int(epis_split[0])
                                row_data["episode"] = int(epis_split[1])
                                row_data["episode_title"] = show_row_columns[3].get_text()
                                row_data["acquired"] = True if (
                                show_row_columns[4].input.get("checked") == "") else False
                                row_data["watched"] = True if (
                                show_row_columns[4].input.get("checked") == "") else False
                            except ValueError:
                                raise ParseError()

                            show_data.append(row_data)

                show_data_with_name = {"show": wasted_data_row['name'], "episodes": show_data}

                all_show_data.append(show_data_with_name)

        all_data = {"wasted": wasted_all, "shows": all_show_data}

    return all_data


def save(all_data, username, to_json, to_xlsx, to_html):
    filename = "myeps_" + username + "_" + datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    if to_json:
        save_to_json(all_data, filename + ".json")
    if to_xlsx:
        save_to_xlsx(all_data, filename + ".xlsx")
    if to_html:
        save_to_html(all_data, filename + ".html")

def save_to_json(all_data, filename):
    with open(filename, 'w') as output:
        output.write(json.dumps(all_data, indent=4, separators=(',', ': ')))


def save_to_xlsx(all_data, filename):
    import xlsxwriter

    workbook = xlsxwriter.Workbook(filename)
    wasted_sheet = workbook.add_worksheet(name="Time Wasted")

    bold = workbook.add_format({'bold': True})

    wasted_sheet.merge_range(0, 0, 0, 5, 'Time Wasted', bold)

    wasted_headers = ("Name", "Status", "Runtime", "Mins", "Eps", "Time Wasted")
    for wasted_header_col, wasted_header in enumerate(wasted_headers):
        wasted_sheet.write(1, wasted_header_col, wasted_header)

    row = 2
    col = 0

    for wasted_row in (all_data["wasted"]["shows"]):
        wasted_sheet.write(row, col, wasted_row["name"])
        wasted_sheet.write(row, col + 1, wasted_row["status"])
        wasted_sheet.write(row, col + 2, wasted_row["runtime"])
        wasted_sheet.write(row, col + 3, wasted_row["mins"])
        wasted_sheet.write(row, col + 4, wasted_row["eps"])
        wasted_sheet.write(row, col + 5, wasted_row["time_wasted"])
        row += 1

    # Write a total using a formula.
    wasted_sheet.write(row, 0, 'Total', bold)
    wasted_sheet.write(row, 1, all_data["wasted"]["total"])

    workbook.close()


def save_to_html(all_data, filename):
    with open(filename, 'w') as output:
        raise Exception()
