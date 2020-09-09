from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
from datetime import datetime
import numpy as np

cg = CoinGeckoAPI()
cs_list = ['icon','ethereum']#,'chainlink'
cs_list_id = ['1','2']
kpi_id = ['17','18','19']
kpi_request = ['current_price','total_volume','market_cap']
#cs_list_id = ['1','2','3']

start_dti = '01, 01, 2019'
end_dti = '01, 30, 2019'
index = pd.date_range(start_dti, end_dti)

#data = cg.get_coin_history_by_id(cs, str('01-01-2019'))

appended_data = []
for d in index.strftime('%d-%m-%Y'):
    for s, o in zip(kpi_id, kpi_request):
        for a,g in zip(cs_list,cs_list_id):
            data = cg.get_coin_history_by_id(a, str(d))
            history = pd.DataFrame(data=[{'d_date_id' : str(d),
                                             a: data['market_data'][o]['eur']}]).set_index('d_date_id')
            history['d_level0_id'] = str(g)
            history['Denominator'] = 0
            history['d_kpi_id'] = s
            history['d_level1_id'] = 0
            history['d_level2_id'] = 0
            history['d_level3_id'] = 0
            history['d_level4_id'] = 0
            history['Numerator'] = ''
            appended_data.append(history)


appended_data = pd.concat(appended_data)

#df['DOB']=pd.to_datetime(df['DOB'].dt.strftime('%m/%d/%Y'))

f_kpi_CoinGecko = appended_data.reset_index('d_date_id') #rename(columns={"icon": "Numerator"}).
#f_kpi_CoinGecko['Numerator'] = f_kpi_CoinGecko['icon'] + f_kpi_CoinGecko['ethereum']
f_kpi_CoinGecko= f_kpi_CoinGecko.fillna(0)
f_kpi_CoinGecko["Numerator"] = (f_kpi_CoinGecko["icon"] + f_kpi_CoinGecko["ethereum"]).astype("float")
#f_kpi_CoinGecko['Numerator'] = f_kpi_CoinGecko.loc[f_kpi_CoinGecko['Numerator'].isna() , 'Numerator'] = f_kpi_CoinGecko['ethereum'])

#f_kpi_CoinGecko['Numerator'] = f_kpi_CoinGecko.loc[f_kpi_CoinGecko['Numerator'].isna() , 'Numerator'] = f_kpi_CoinGecko['icon']
#f_kpi_CoinGecko.loc[f_kpi_CoinGecko['Numerator'].notna() , 'Numerator'] = f_kpi_CoinGecko['Numerator']

#f_kpi_CoinGecko.loc[f_kpi_CoinGecko['icon'].isna() , 'Numerator'] = f_kpi_CoinGecko['ethereum']
#f_kpi_CoinGecko.loc[f_kpi_CoinGecko['icon'].notna() , 'Numerator'] = f_kpi_CoinGecko['icon']
f_kpi_CoinGecko['d_date_id'] = pd.to_datetime(f_kpi_CoinGecko['d_date_id'])
f_kpi_CoinGecko['d_date_id'] =  f_kpi_CoinGecko.d_date_id.apply(lambda x: x.strftime('%Y%m%d')).astype(int)

f_kpi_CoinGecko = f_kpi_CoinGecko.drop(columns=cs_list,axis=1)

print(f_kpi_CoinGecko)

#tmp_d_level0_id           = pd.DataFrame(pd.read_excel("C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/LEVEL0_Blockchain_Library.xlsx");

#d_level0_id           = tmp_d_level0_id[['d_level0_id','Calculation']];

f_kpi_CoinGecko.to_csv(r'C:\Users\nickh\PycharmProjects\daopi2\assets\Attributes\Blockchain industry\CoinGeckoData\f_kpi_CoinGecko.csv', index=False)
#Numerator,Denominator,d_kpi_id,d_level0_id,d_level1_id,d_level2_id,d_date_id


