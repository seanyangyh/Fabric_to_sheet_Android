from __future__ import print_function
import httplib2
import os
import datetime
import User_Input
import json
# from time import sleep

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'


def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def json_parser(raw_data):
    # json -> dict of python
    json_data = json.loads(raw_data)
    return json_data


def fabric_crash_rate_uploader(data, date, spreadsheet_id, sheet_range, service):
    # clear data of Summary!A2:E first
    request = service.spreadsheets().values().clear(spreadsheetId=spreadsheet_id, range=sheet_range, body={}).execute()
    print(request)
    for i in range(0, len(User_Input.Version), 1):
        crash_uv = data[User_Input.Version[i]]['CRASH-FREE USERS']
        crash_pv = data[User_Input.Version[i]]['CRASH-FREE SESSIONS']
        append_sheet = sheet_summary_append_handler(date, User_Input.Version[i], crash_uv, crash_pv, spreadsheet_id, sheet_range, service)
        print(append_sheet)


def sheet_summary_append_handler(date, ver, crash_uv, crash_pv, spreadsheet_id, sheet_range, service):
    value_range_body = {
        'values': [
            [date, ver, crash_uv, crash_pv],
        ]
    }
    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=sheet_range,
                                                     valueInputOption='USER_ENTERED', body=value_range_body).execute()
    return result


def fabric_crashlytics_modifier(column_a_data, data, spreadsheet_id, sheet_range, service):
    temp_list_duplicate = []  # Temporary List to record the issue has been modified do not need raise again
    for i in range(0, len(column_a_data['values']), 1):
        for j in range(0, len(data['data']), 1):
            if column_a_data['values'][i][0] == data['data'][j]['IssueNumber']:
                crash_count = data['data'][j]['Crash'] + " / " + data['data'][j]['User']
                modify_sheet = sheet_all_modify_handler(crash_count, spreadsheet_id, sheet_range + str(i+1), service)
                print(modify_sheet)
                temp_list_duplicate.append(j)

    print(temp_list_duplicate)
    return temp_list_duplicate


def sheet_all_modify_handler(data, spreadsheet_id, sheet_range, service):
    value_range_body = {
        'range': sheet_range,
        'values': [
            [data],
        ]
    }
    result = service.spreadsheets().values().update(spreadsheetId=spreadsheet_id, range=sheet_range,
                                                     valueInputOption='USER_ENTERED', body=value_range_body).execute()
    return result


def fabric_crashlytics_uploader(duplicate_list, data, spreadsheet_id, sheet_range, service):
    for i in range(0, len(data['data']), 1):
        ver = data['data'][i]['Version']
        if User_Input.PlatformName is 'Android':
            ver_begin = ver.index('(')
            ver_last = ver.index(')')
            ver = ver[ver_begin+1:ver_last]
        if ver == User_Input.Top_build[0] and i not in duplicate_list:
            num = data['data'][i]['IssueNumber']
            url = data['data'][i]['URL']
            crash_count = data['data'][i]['Crash'] + " / " + data['data'][i]['User']
            title = data['data'][i]['IssutTitle']
            sub_title = data['data'][i]['IssueSubtitle']
            append_sheet = sheet_all_append_handler(num, ver, url, crash_count, title, sub_title, spreadsheet_id, sheet_range, service)
            print(append_sheet)


def sheet_all_append_handler(num, ver, url, crash_count, title, sub_title, spreadsheet_id, sheet_range, service):
    value_range_body = {
        'values': [
            [num, ver, url, crash_count, User_Input.Default_owner, User_Input.Default_status, "", "", title, sub_title],
        ]
    }
    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=sheet_range,
                                                     valueInputOption='USER_ENTERED', body=value_range_body).execute()
    return result


def sheet_all_append_version(ver, spreadsheet_id, sheet_range, service):
    value_range_body = {
        'values': [
            [ver],
        ]
    }
    result = service.spreadsheets().values().append(spreadsheetId=spreadsheet_id, range=sheet_range,
                                                     valueInputOption='USER_ENTERED', body=value_range_body).execute()
    print(result)
    begin_split = result['updates']['updatedRange'].split('!')
    second_split = begin_split[1].lstrip('A')
    row = int(second_split)
    result2 = sheet_all_fill_color_and_merge(row, spreadsheet_id, service)
    return result2


def sheet_all_fill_color_and_merge(row, spreadsheet_id, service):
    batch_update_spreadsheet_request_color = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": User_Input.sheet_id_all,
                        "startRowIndex": row-1,
                        "endRowIndex": row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 10
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "backgroundColor": {
                                "red": 1,
                                "green": 1,
                                "blue": 0
                            }
                        }
                    },
                    "fields": "userEnteredFormat(backgroundColor)"
                }
            },
            {
                "mergeCells": {
                    "range": {
                        "sheetId": User_Input.sheet_id_all,
                        "startRowIndex": row-1,
                        "endRowIndex": row,
                        "startColumnIndex": 0,
                        "endColumnIndex": 10
                    },
                    "mergeType": "MERGE_ROWS"
                }
            }
        ]
    }
    result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                 body=batch_update_spreadsheet_request_color).execute()
    return result


def crash_rate_warning_handler(column_d_data, spreadsheet_id, service):
    for i in range(0, len(column_d_data), 1):
        crash_rate = column_d_data[i]
        print(crash_rate)
        if not crash_rate == []:
            temp = crash_rate[0]
            crash_rate_value = temp.rstrip('%')
            start_column = 3
            end_column = 4
            sheet_id = User_Input.sheet_id_summary
            if float(crash_rate_value) <= 99.7:
                update_text_color = sheet_update_text_color(i+2, start_column, end_column, 1, 0, 0, sheet_id, spreadsheet_id, service)
                print(update_text_color)
            else:
                update_text_color = sheet_update_text_color(i+2, start_column, end_column, 0, 0, 0, sheet_id, spreadsheet_id, service)
                print(update_text_color)


def fabric_warning_handler(column_d_data, spreadsheet_id, service):
    for i in range(0, len(column_d_data), 1):
        crash_user = column_d_data[i]
        if not crash_user == []:
            temp = crash_user[0]
            crash_count = temp.strip().split(" / ")
            if int(crash_count[0]) >= User_Input.Criteria_count:
                start_column = 0
                end_column = 10
                sheet_id = User_Input.sheet_id_all
                update_text_color = sheet_update_text_color(i+2, start_column, end_column, 1, 0, 0, sheet_id, spreadsheet_id, service)
                print(update_text_color)


def sheet_update_text_color(row, start_column, end_column, red, green, blue, sheet_id, spreadsheet_id, service):
    batch_update_spreadsheet_request_color = {
        "requests": [
            {
                "repeatCell": {
                    "range": {
                        "sheetId": sheet_id,
                        "startRowIndex": row - 1,
                        "endRowIndex": row,
                        "startColumnIndex": start_column,
                        "endColumnIndex": end_column
                    },
                    "cell": {
                        "userEnteredFormat": {
                            "textFormat": {
                                "foregroundColor": {
                                    "red": red,
                                    "green": green,
                                    "blue": blue
                                }
                            }
                        }
                    },
                    "fields": "userEnteredFormat(textFormat)"
                }
            },
        ]
    }
    result = service.spreadsheets().batchUpdate(spreadsheetId=spreadsheet_id,
                                                body=batch_update_spreadsheet_request_color).execute()
    return result


def main():
    today = datetime.datetime.now()
    print(today.strftime("%Y/%m/%d"))

    # Oauth Credential from client_secret.json
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    # Sheet_ID from the url
    spreadsheet_id = User_Input.spreadsheet_id

    # Define range
    range_all = 'All!A2:J'
    range_all_column_a = 'All!A:A'
    range_all_column_d = 'All!D'
    range_summary = 'Summary!A2:E'
    range_summary_column_d = 'Summary!D2:D'

    # read Fabric.json
    read_fabric = open(str(PATH('./Fabric.json')), "r")
    raw_data = read_fabric.read()
    read_fabric.close()
    # crash rate parser
    crash_rate_dict = json_parser(raw_data)
    print(crash_rate_dict)
    # upload crash rate data to sheet
    fabric_crash_rate_uploader(crash_rate_dict, today.strftime("%Y/%m/%d"), spreadsheet_id, range_summary, service)

    # read Top_build_Fabric.json
    read_crashlytics = open(str(PATH('./Top_build_Fabric.json')), "r")
    raw_data_crashlytics = read_crashlytics.read()
    read_crashlytics.close()
    # crashlytics parser
    crashlytics_dict = json_parser(raw_data_crashlytics)
    print(crashlytics_dict)

    # find fabric num in column A or not
    is_version_exist = False
    column_a_data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=range_all_column_a).execute()
    print(column_a_data)
    for i in range(0, len(column_a_data['values']), 1):
        # print(column_a_data['values'][i])
        if User_Input.Top_build == column_a_data['values'][i]:
            is_version_exist = True
            break

    # if version exist then update crash/user into sheet, otherwise upload crashlytics data to sheet
    if is_version_exist is True:
        duplicated_list = fabric_crashlytics_modifier(column_a_data, crashlytics_dict, spreadsheet_id, range_all_column_d, service)
        fabric_crashlytics_uploader(duplicated_list, crashlytics_dict, spreadsheet_id, range_all, service)
    else:
        sheet_all_append_version(User_Input.Top_build[0], spreadsheet_id, range_all, service)
        fabric_crashlytics_uploader([], crashlytics_dict, spreadsheet_id, range_all, service)

    # get Summary sheet column D data to find crash rate above 0.3% and mark as red
    summary_column_d_data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                            range=range_summary_column_d).execute()
    print(summary_column_d_data)
    crash_rate_warning_handler(summary_column_d_data['values'], spreadsheet_id, service)

    # get All sheet column D data to find crash count above 100 and mark as red
    column_d_data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id,
                                                            range=range_all_column_d + "2:D").execute()
    print(column_d_data)
    fabric_warning_handler(column_d_data['values'], spreadsheet_id, service)


if __name__ == '__main__':
    main()