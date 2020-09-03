import gspread
from pprint import pprint

from oauth2client.service_account import ServiceAccountCredentials
scope = ["https://spreadsheets.google.com/feeds",'https://www.googleapis.com/auth/spreadsheets',"https://www.googleapis.com/auth/drive.file","https://www.googleapis.com/auth/drive"]

credsgoogle = ServiceAccountCredentials.from_json_keyfile_name("credsgoogle.json", scope)

client = gspread.authorize(credsgoogle)

sheet = client.open("KPI Library").sheet1 # Open the spreadhseet

data = sheet.get_all_records()  # Get a list of all records

pprint(data)