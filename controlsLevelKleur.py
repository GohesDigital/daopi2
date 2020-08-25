##SQL Retrieve data
from sqlalchemy import create_engine
import pandas as pd
import os

path = 'C:/Users/nick/Documents/ICON KPI analytics/Attributes'
os.chdir(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes')
#engine = create_engine('mysql+pymysql://root:Handschoen92@localhost:3306/kpiframework')
#dbConnection    = engine.connect()

#d_kpi = pd.DataFrame(pd.read_sql("select distinct KPIName from kpiframework.d_kpi", dbConnection));
#d_level0 = pd.DataFrame(pd.read_sql("select distinct LevelName from kpiframework.d_level0", dbConnection));
#d_level1 = pd.DataFrame(pd.read_sql("select distinct LevelName from kpiframework.d_level1", dbConnection));
#d_level2 = pd.DataFrame(pd.read_sql("select distinct LevelName from kpiframework.d_level2", dbConnection));
#d_level3 = pd.DataFrame(pd.read_sql("select distinct LevelName from kpiframework.d_level3", dbConnection));
#d_level4 = pd.DataFrame(pd.read_sql("select distinct LevelName from kpiframework.d_level4", dbConnection));
#d_target = pd.DataFrame(pd.read_sql("select distinct Target    from kpiframework.d_target", dbConnection));

#datatypes
DTd_kpi           = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/d_kpi.xlsx',sheet_name='2'));
DTd_level0        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL0_Blockchain_Library.xlsx',sheet_name='2'));
DTd_level1        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL1_ICON_Library.xlsx',sheet_name='2'));
DTd_level2        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL2_ICON_Library.xlsx',sheet_name='2'));
DTd_level3        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL3_ICON_Library.xlsx',sheet_name='2'));


#datatypes
#DTd_kpi.set_index('column')['datatype']
DTKPINameList    = dict(DTd_kpi.set_index('column')['datatype'])
DTLevel0NameList = dict(DTd_level0.set_index('column')['datatype'])
DTLevel1NameList = dict(DTd_level1.set_index('column')['datatype'])
DTLevel2NameList = dict(DTd_level2.set_index('column')['datatype'])
DTLevel3NameList = dict(DTd_level3.set_index('column')['datatype'])
#Level4NameList = d_level4.set_index('d_kpi_id')['KPIName'].to_dict()
#TargetList     = d_target.set_index('d_kpi_id')['KPIName'].to_dict()

#Dataframes
#f_kpi           = pd.read_sql("select * from kpiframework.f_kpi", dbConnection);
d_kpi           = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/d_kpi.xlsx',sheet_name='1')); #,
d_level0        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL0_Blockchain_Library.xlsx',sheet_name='1'));
d_level1        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL1_ICON_Library.xlsx',sheet_name='1'));
d_level2        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL2_ICON_Library.xlsx',sheet_name='1'));
d_level3        = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/Attributes/LEVEL3_ICON_Library.xlsx',sheet_name='1'));

pd.set_option('display.expand_frame_repr', False)

#dbConnection.close()

#attributelists
KPINameList    = dict(d_kpi.set_index('d_kpi_id')['KPIName'].to_dict())
Level0NameList = dict(d_level0.set_index('d_level0_id')['LevelName'].to_dict())
Level1NameList = dict(d_level1.set_index('d_level1_id')['Level1Name'].to_dict())
Level2NameList = dict(d_level2.set_index('d_level2_id')['Level2Color'].to_dict())
Level3NameList = dict(d_level3.set_index('d_level3_id')['Level3Name'].to_dict())
#Level4NameList = d_level4.set_index('d_kpi_id')['KPIName'].to_dict()
#TargetList     = d_target.set_index('d_kpi_id')['KPIName'].to_dict()

print(Level2NameList)

# In[]:
# Controls for webapp

KPINameColor = dict(
    Alles="#FA9FB5",
)


LEVEL0_COLORS = dict(
    Alles="#FA9FB5"
)

LEVEL1_COLORS = dict(
    GD="#FFEDA0"
)

LEVEL2_COLORS = dict(
    GD="#FFEDA0",
    GE="#FA9FB5",
    GW="#A1D99B",
    IG="#67BD65",
    OD="#BFD3E6",
    OE="#B3DE69",
    OW="#FDBF6F",
    ST="#FC9272",
    BR="#D0D1E6",
    MB="#ABD9E9",
    IW="#3690C0",
    LP="#F87A72",
    MS="#CA6BCC",
    Confidential="#DD3497",
    DH="#4EB3D3",
    DS="#FFFF33",
    DW="#FB9A99",
    MM="#A6D853",
    NL="#D4B9DA",
    OB="#AEB0B8",
    SG="#CCCCCC",
    TH="#EAE5D9",
    UN="#C29A84",
)

LEVEL3_COLORS = dict(
    GD="#FFEDA0",
    GE="#FA9FB5",
    GW="#A1D99B",
    IG="#67BD65",
    OD="#BFD3E6",
    OE="#B3DE69",
    OW="#FDBF6F",
    ST="#FC9272",
    BR="#D0D1E6",
    MB="#ABD9E9",
    IW="#3690C0",
    LP="#F87A72",
    MS="#CA6BCC",
    Confidential="#DD3497",
    DH="#4EB3D3",
    DS="#FFFF33",
    DW="#FB9A99",
    MM="#A6D853",
    NL="#D4B9DA",
    OB="#AEB0B8",
    SG="#CCCCCC",
    TH="#EAE5D9",
    UN="#C29A84",
)
