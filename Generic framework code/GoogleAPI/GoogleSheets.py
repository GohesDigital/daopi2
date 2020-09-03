import gspread
import json
import pandas as pd
from pprint import pprint

from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credsgoogle = ServiceAccountCredentials.from_json_keyfile_name("credsgoogle.json", scope)

client = gspread.authorize(credsgoogle)

sheet = client.open("KPI Library").sheet1 # Open the spreadhseet


data = sheet.get_all_records()

pprint(data)

with open("KPIAttributes_daopi.json", "w") as outfile:
    json.dump(data, outfile)

df = pd.read_json (r'/Blockchain industry code/GoogleAPI/KPIAttributes_daopi.json')
df.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\d_kpi_daopi.csv', index = False)
