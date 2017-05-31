'''
請在環境變數新增 Fabirc帳號密碼
FABIRCUSER = 你的帳號
FABIRCPASSWORD = 你的密碼

下面三行也丟掉環境變數中
# Firefox
PATH="/Users/mark/Downloads/geckodriver:$PATH"
export PATH

安裝火狐
'''

import sys
import os


def PATH(p):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), p))


iOS = {"default_status": "Open", "default_owner": "Keith", "spreadsheet_id": "1ex2ovtXCVkZWuyqZi7awUYYxpK-uxioS-rOdyI6N_8E", "sheet_id_all": "1927443904", "sheet_id_summary": "670362750"}
Android = {"default_status": "Open", "default_owner": "Fate", "spreadsheet_id": "1aEMm04KCgHUaNDmP3IsEI-Tuz2FBfcMJmYhIBTbgsD8", "sheet_id_all": "227423795", "sheet_id_summary": "1295400851"}
Test = {"spreadsheet_id": "1Gx_2izYogh-0PgEej-EtGJrYzUaL_Ci5N4OH0bQLblc", "sheet_id_all": "845833450", "sheet_id_summary": "362639746"}


def get_parameter(para):
    PlatformName = 'iOS'
    Top_build = []
    Version = []
    Criteria_count = 0
    test_flag = 0
    Default_status = 'Open'
    Default_owner = 'Keith'
    spreadsheet_id = '1Gx_2izYogh-0PgEej-EtGJrYzUaL_Ci5N4OH0bQLblc'
    sheet_id_all = '845833450'
    sheet_id_summary = '362639746'

    for i in range(0, len(para), 1):
        if para[i] == '-platform':
            PlatformName = para[i+1]
        elif para[i] == '--top-build':
            Top_build.append(para[i+1])
        elif para[i] == '-version':
            Version.extend(para[i+1].split(','))
            Version.append('All Version')
        elif para[i] == '-criteria':
            Criteria_count += int(para[i+1])
        elif para[i] == '-test':
            test_flag += int(para[i+1])

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


user_input_data(sys.argv)
