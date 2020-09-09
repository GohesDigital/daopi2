import gspread
import json
import pandas as pd
from pprint import pprint

from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credsgoogle = ServiceAccountCredentials.from_json_keyfile_name("credsgoogle.json", scope)

client = gspread.authorize(credsgoogle)

Sheetlist=['KPI Library','Level 1 Library']
FileList=['KPIAttributes_daopi.json','Level1Attributes_daopi.json']
DimensionList=['d_kpi_daopi.csv','Level1Attributes_daopi.csv']

for i,p,d in zip(Sheetlist,FileList,DimensionList):
    sheet = client.open(i).sheet1    # Open the spreadhseet

    data = sheet.get_all_records()

    pprint(data)

    with open(p, "w") as outfile:
        json.dump(data, outfile)

    df = pd.read_json(r'C:\Users\nickh\PycharmProjects\daopi2\Generic framework code\GoogleAPI/' + p  )
    df.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes/' + d, index = False)
