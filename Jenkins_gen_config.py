'''
請在環境變數新增 Fabirc帳號密碼
FABRICUSER = 你的帳號
FABRICPASSWORD = 你的密碼

下面三行也丟掉環境變數中
# Firefox
PATH="/Users/mark/Downloads/geckodriver:$PATH"
export PATH

安裝火狐
'''
from __future__ import print_function
import httplib2
import os
import datetime
import json
import sys

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(prog=['Jenkins_gen_config'], parents=[tools.argparser])
    flags.add_argument('-p', '--platform', nargs=1, action='store', choices=['iOS', 'Android'], default='iOS',
                        help='Platform selection: iOS or AND, default=iOS')
    flags.add_argument('-c', '--criteria', nargs=1, action='store', default=100,
                        help='Warning color, if above this num, text will be filled in red color, default=100',
                        type=int)
    flags.add_argument('-t', '--test', nargs=1, action='store', choices=[0, 1], default=0,
                        help='0 for official spreadsheet, 1 for test spreadsheet, default=0', type=int)
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
# SCOPES = 'https://www.googleapis.com/auth/drive'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

iOS = {"default_status": "Open", "default_owner": "Keith", "spreadsheet_id": "1ex2ovtXCVkZWuyqZi7awUYYxpK-uxioS-rOdyI6N_8E", "sheet_id_all": "1927443904", "sheet_id_summary": "670362750"}
Android = {"default_status": "Open", "default_owner": "Fate", "spreadsheet_id": "1aEMm04KCgHUaNDmP3IsEI-Tuz2FBfcMJmYhIBTbgsD8", "sheet_id_all": "227423795", "sheet_id_summary": "1295400851"}
Test = {"spreadsheet_id": "1Gx_2izYogh-0PgEej-EtGJrYzUaL_Ci5N4OH0bQLblc", "sheet_id_all": "845833450", "sheet_id_summary": "362639746"}


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


def get_actual_version_on_Fabric(raw_data):
    temp = raw_data[:3]
    temp_1 = temp[:1]
    temp_2 = temp[-2:]
    data = temp_1 + '.' + temp_2 + ' (' + raw_data + ')'
    print(data)
    return data


def get_Android_sheet_version(spreadsheet_id, sheet_range, service):
    data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
    Version = []
    count = 0
    Version.append(get_actual_version_on_Fabric(data['values'][len(data['values']) - 1][2]))
    for i in range(len(data['values'])-2, 0, -1):
        try:
            if data['values'][i][5] == '100%':
                Version.append(get_actual_version_on_Fabric(data['values'][i][2]))
                count += 1
            if count == 4:
                break
        except:
            continue

    Version.append('All Version')
    print(Version)
    return Version


def get_iOS_sheet_version(spreadsheet_id, sheet_range, service):
    data = service.spreadsheets().values().get(spreadsheetId=spreadsheet_id, range=sheet_range).execute()
    Version = []
    count = 0
    for i in range(len(data['values']) - 1, 0, -1):
        try:
            if '審核通過' in data['values'][i][5]:
                Version.append(data['values'][i][2])
                count += 1
            if count == 5:
                break
        except:
            continue

    Version.append('All Version')
    print(Version)
    return Version


def get_parameter(para):
    PlatformName = ['iOS']
    Top_build = []
    Version = []
    Criteria_count = [100]
    test_flag = [0]
    Default_status = 'Open'
    Default_owner = 'Keith'
    spreadsheet_id = '1Gx_2izYogh-0PgEej-EtGJrYzUaL_Ci5N4OH0bQLblc'
    sheet_id_all = '845833450'
    sheet_id_summary = '362639746'

    # Oauth Credential from client_secret.json
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http, discoveryServiceUrl=discoveryUrl)

    # PG_發版紀錄 Sheet_ID from the url
    release_spreadsheet_id = '19INfvzcS0ThpHeaoqeOOrBazrZBvJ38_umOSxUnGyt4'

    # Define range
    range_Android = 'PG_Android!A:F'
    range_iOS = 'PG_iOS!A:F'

    # parameter deploy
    PlatformName = para.platform[0]
    Criteria_count = para.criteria[0]
    test_flag = para.test[0]

    # auto get latest 5 versions from PG_發版紀錄 spreadsheet
    if Top_build == [] or Version == []:
        if PlatformName == 'iOS':
            Version = get_iOS_sheet_version(release_spreadsheet_id, range_iOS, service)
            Top_build.append(Version[0])
        if PlatformName == 'Android':
            Version = get_Android_sheet_version(release_spreadsheet_id, range_Android, service)
            Top_build.append(Version[0])

    if PlatformName == 'iOS':
        Default_status = iOS['default_status']
        Default_owner = iOS['default_owner']
        spreadsheet_id = iOS['spreadsheet_id']
        sheet_id_all = iOS['sheet_id_all']
        sheet_id_summary = iOS['sheet_id_summary']
    elif PlatformName == 'Android':
        Default_status = Android['default_status']
        Default_owner = Android['default_owner']
        spreadsheet_id = Android['spreadsheet_id']
        sheet_id_all = Android['sheet_id_all']
        sheet_id_summary = Android['sheet_id_summary']

    if test_flag == 1:
        spreadsheet_id = Test['spreadsheet_id']
        sheet_id_all = Test['sheet_id_all']
        sheet_id_summary = Test['sheet_id_summary']

    result = dict(plat=PlatformName, top=Top_build, ver=Version, cri=Criteria_count, test=test_flag, status=Default_status, owner=Default_owner, ssid=spreadsheet_id, sidall=sheet_id_all, sidsum=sheet_id_summary)
    return result


def user_input_data(u_input):
    print(u_input)
    config = get_parameter(u_input)
    print(config)
    file = open('./User_Input.py', "w")
    file.close()
    file = open('./User_Input.py', "a")
    file.write('PlatformName = ' + '\'' + config['plat'] + '\'' + '\n')
    file.write('Top_build = ' + str(config['top']) + '\n')
    file.write('Version = ' + str(config['ver']) + '\n')
    file.write('Criteria_count = ' + str(config['cri']) + '\n')
    file.write('Default_status = ' + '\'' + config['status'] + '\'' + '\n')
    file.write('Default_owner = ' + '\'' + config['owner'] + '\'' + '\n')
    file.write('spreadsheet_id = ' + '\'' + config['ssid'] + '\'' + '\n')
    file.write('sheet_id_all = ' + '\'' + config['sidall'] + '\'' + '\n')
    file.write('sheet_id_summary = ' + '\'' + config['sidsum'] + '\'' + '\n')
    file.close()


user_input_data(flags.parse_args())
