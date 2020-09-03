import pandas as pd
from sqlalchemy import create_engine
from datetime import timedelta
from dateutil.relativedelta import relativedelta
#from datetime import datetime
from openpyxl.workbook import Workbook
import numpy as np

import requests
url ="assets/Attributes/d_kpi.csv"
r = requests.get(url).content
print(r)

#engine = create_engine('mysql+pymysql://root:Handschoen92@localhost:3306/kpiframework')
#dbConnection    = engine.connect()

#SQL Retrieve data
keys            = ['d_kpi_id','d_date_id']##,'d_level0_id','d_level1_id','d_level2_id'
Facts           = ['f_kpi_daopi','f_kpi_CoinGecko']


#Dataframes Fact
#f_kpi_test       = pd.read_sql("select Numerator,Denominator,d_kpi_id,d_level0_id,d_level1_id,d_level2_id,d_date_id from kpiframework.f_kpi", dbConnection);
f_kpi_daopi         = pd.csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\f_kpi_daopi.csv');
f_kpi_CoinGecko    = pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/f_kpi_CoinGecko.xlsx');
print(f_kpi_daopi)
print(f_kpi_CoinGecko)
f_kpi = pd.concat(Facts)
print(f_kpi_CoinGecko)

#Dataframes Dimensions/attributes
tmp_d_kpi       = pd.DataFrame(pd.read_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\d_kpi.csv')); #, columns=['d_kpi_id', 'KPIName'], index_col=0)
d_kpi           = tmp_d_kpi[['d_kpi_id']]#,'Calculation'
d_date          = pd.read_sql("select d_date_id,full_date,d_date_id as int_day,date_name_eu as DayName,replace(calendar_year_month,'-','') as int_month,LAST_DAY(date_name) as LD_Month,concat(calendar_year,' ',month_name) as MonthName,concat(calendar_year,calendar_quarter) 	as int_quarter,MAKEDATE(YEAR(date_name),1)+ INTERVAL QUARTER(date_name) QUARTER - INTERVAL 1 DAY as LD_Quarter,concat('Q',calendar_quarter,' ',calendar_year) as QuarterName,calendar_year as int_year,calendar_year as YearName,LAST_DAY(DATE_ADD(date_name, INTERVAL 12-MONTH(date_name) MONTH)) as LD_Year from dimensionalmodel.d_date", dbConnection);
##d_level0        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL0_Blockchain_Library.xlsx',sheet_name='1'));
##d_level1        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL1_ICON_Library.xlsx',sheet_name='1'));
##d_level2        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL2_ICON_Library.xlsx',sheet_name='1'));
df_list         = [f_kpi,d_kpi,d_date]#,d_level0,d_level1,d_level2
Grain           = ['full_date','LD_Month','LD_Quarter','LD_Year']
GrainName       = ['DayName','MonthName','QuarterName','YearName']

"""
-Join all reference tables to the dataframe with a loop
-Group by all relevant columns to calculate the numerator and denominator
-Loop through to repeat this for all the grains provided (time-grains)
-Create file for evert grain calculated
"""

for z,o in zip(Grain,GrainName):
    df = df_list[0]
    for i,x in zip(df_list[1:],range(len(keys))):
        df = df.merge(i, on=keys[x])
    #del df['d_date_id']
    dfgrouped = df.groupby(['d_kpi_id','d_level0_id','d_level1_id','d_level2_id',z,o]).agg({'Numerator': ['sum'],'Denominator': ['sum']})  #'Calculation','d_level0_id','d_level1_id','d_level2_id',
    grouped_multiple = dfgrouped.reset_index()
    grouped_multiple.columns = grouped_multiple.columns.droplevel(1)
    grouped_multiple['Grain'] = o
    grouped_multiple.rename(columns={z: 'Period_int'}, inplace=True)
    grouped_multiple.rename(columns={o: 'PeriodName'}, inplace=True)
    #print(dfgrouped)
    #print(df.columns)
    grouped_multiple.to_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_' + str(o) + '.xlsx')

KPIFrameworkDay     = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_DayName.xlsx'));
KPIFrameworkMonth   = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_MonthName.xlsx'));
KPIFrameworkQuarter = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_QuarterName.xlsx'));
KPIFrameworkYear    = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_YearName.xlsx'));

"""
-Concatenate the files created in previous step and create a new file with all grains concatenated. Distinguish by filtering on column 'grain'
-Convert period integer to datetime (needed later for visualisation and calculations)
-Calculate an extra column named 'Period in lp' meaning: the data of the previous period. This will be used later to join the numerator and denominator of the previous period
"""

KPIFramework    = pd.concat([KPIFrameworkDay, KPIFrameworkMonth,KPIFrameworkQuarter,KPIFrameworkYear])
KPIFramework["Period_int"] = pd.to_datetime(KPIFramework["Period_int"])
KPIFramework['Period_int_lp'] = KPIFramework[['Grain','Period_int']].apply(lambda x: x['Period_int'] + timedelta(days=+7) if x['Grain']=='DayName' else x['Period_int'] + timedelta(days=+365) if x['Grain']=='YearName' else x['Period_int'] + relativedelta(months=+1) if x['Grain']=='MonthName' else x['Period_int'] + relativedelta(months=+3) if x['Grain']=='QuarterName' else x['Period_int'], axis=1)
#['Period_int_lp']

#print(KPIFramework.columns)
"""
-Create two row-id's. One is for the dataframe itself and one is manipulated to be used to join
-Create second KPIFramework and only select numerator and denominator with the row_id_lp
-Merge the two ID's to add last period numerator and denominator to existing framework
-Drop unnesseccary columns
-Save file
"""

KPIFramework['Row_id'] = KPIFramework.apply(lambda x: x['Period_int'].strftime('%Y%m%d') + str(x['d_kpi_id']) + str(x['d_level0_id']) + str(x['d_level1_id']) + str(x['d_level2_id']) + str(x['Grain']), axis=1)
KPIFramework['Row_id_lp'] = KPIFramework.apply(lambda x: x['Period_int_lp'].strftime('%Y%m%d') + str(x['d_kpi_id']) + str(x['d_level0_id']) + str(x['d_level1_id']) + str(x['d_level2_id']) + str(x['Grain']), axis=1)

KPIFramework_LP = KPIFramework[['Row_id_lp','Numerator','Denominator']]
KPIFramework = KPIFramework.merge(KPIFramework_LP, how='left',left_on=['Row_id'], right_on=['Row_id_lp'],suffixes = ("","_LP"))

KPIFramework = KPIFramework.drop(columns=['Row_id_lp','Row_id_lp_LP','Row_id','Unnamed: 0'],axis=1)
#print(KPIFramework.columns)

KPIFramework.to_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python.xlsx', index=False)
