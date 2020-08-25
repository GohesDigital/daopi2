from pycoingecko import CoinGeckoAPI
import json
import pandas as pd
cg = CoinGeckoAPI()
cs_list = ['icon','ethereum']

start_dti = '1, 1, 2019'
end_dti = '13, 01, 2019'
index = pd.date_range(start_dti, end_dti)

#data = cg.get_coin_history_by_id(cs, str('01-01-2019'))

appended_data = []
for d in index.strftime('%d-%m-%Y'):
    for a in cs_list:
        data = cg.get_coin_history_by_id(a, str(d))
        history = pd.DataFrame(data=[{'d_date_id' : str(d),
                                        a: data['market_data']['current_price']['eur']}]).set_index('d_date_id')
        appended_data.append(history)


appended_data = pd.concat(appended_data)
appended_data['Denominator'] = 0
appended_data['kpi_id'] = 17
appended_data['d_level0_id'] = 1
appended_data['d_level1_id'] = 0
appended_data['d_level2_id'] = 0

#df['DOB']=pd.to_datetime(df['DOB'].dt.strftime('%m/%d/%Y'))

f_kpi_CoinGecko = appended_data.rename(columns={"icon": "Numerator"})
print(f_kpi_CoinGecko)
f_kpi_CoinGecko.to_excel(r'C:/Users/nick/Documents/ICON KPI analytics/f_kpi_CoinGecko.xlsx', index=False)

#Numerator,Denominator,d_kpi_id,d_level0_id,d_level1_id,d_level2_id,d_date_id