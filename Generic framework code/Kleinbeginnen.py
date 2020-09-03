import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import datetime
#import mysql.connector
from sqlalchemy import create_engine

import pandas as pd
import flask
import glob
import os
import dash_bootstrap_components as dbc


image_directory = '/Users/chriddyp/Desktop/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

#engine = create_engine('mysql+pymysql://root:Handschoen92@localhost:3306/kpiframework')
#dbConnection    = engine.connect()

#SQL Retrieve data
keys            = ['d_kpi_id','d_level0_id','d_level1_id','d_level2_id'] #'d_date_id',
keysl1          = ['d_kpi_id','d_level0_id','d_level1_id']
ListGrain       = ['int_day','int_month','int_quarter','int_year']
#Dataframes
#f_kpi           = pd.read_sql("select * from kpiframework.f_kpi", dbConnection);

#KPIFrameworkDay     = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_DayName.xlsx'));
#KPIFrameworkMonth   = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_MonthName.xlsx'));
#KPIFrameworkQuarter = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_QuarterName.xlsx'));
#KPIFrameworkYear    = pd.DataFrame(pd.read_excel(r'C:/Users/nick/Documents/ICON KPI analytics/KPIFramework_Python_YearName.xlsx'));
KPIFramework         = pd.DataFrame(pd.read_csv(r'/assets/Attributes/KPIFramework_Python.csv'));

#print(KPIFramework.columns)

columnsdf1 = KPIFramework.columns.tolist()
columnsdf1.remove('d_level2_id')
columnsdf1.remove('Numerator')
columnsdf1.remove('Denominator')
columnsdf1.remove('Numerator_LP')
columnsdf1.remove('Denominator_LP')

#print(columnsd

KPIFrameworkl1 = KPIFramework.groupby(columnsdf1,as_index=False).agg({'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})

#KPIFramework    = pd.concat([KPIFrameworkDay, KPIFrameworkMonth,KPIFrameworkQuarter,KPIFrameworkYear])
d_kpi           = pd.DataFrame(pd.read_excel(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/d_kpi.xlsx',sheet_name='1'));  #, columns=['d_kpi_id', 'KPIName'], index_col=0)
d_level0        = pd.DataFrame(pd.read_excel(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/LEVEL0_Blockchain_Library.xlsx',sheet_name='1'));
d_level1        = pd.DataFrame(pd.read_excel(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/LEVEL1_ICON_Library.xlsx',sheet_name='1'));
d_level2        = pd.DataFrame(pd.read_excel(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/LEVEL2_ICON_Library.xlsx',sheet_name='1'));
df_list         = [KPIFramework,d_kpi,d_level0,d_level1,d_level2] #d_date
df_list_l1      = [KPIFrameworkl1,d_kpi,d_level0,d_level1]

KPIFrameworkl1.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/KPIFrameworkL1.csv', index=False)

# dff.drop(dff.filter(regex='Level2').columns, axis=1, inplace=Truf1)e)
# dff.drop(dff.filter(regex='level2').columns, axis=1, inplace=True)

# dfflevel1 = dff.groupby('d_kpi_id').agg({'Denominator': 'sum', 'Numerator': 'sum'})
dfl1 = df_list_l1[0]
for i, x in zip(df_list_l1[1:], range(len(keysl1))):
    dfl1 = dfl1.merge(i, on=keysl1[x])

dfl1["Period_int"] = pd.to_datetime(dfl1["Period_int"])

dfl1.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/dfl1.csv', index=False)

df = df_list[0]
for i,x in zip(df_list[1:],range(len(keys))):
    df = df.merge(i, on=keys[x])

#minx = pd.datetime(df['Period_int'].min())#)df.eval(
#print(minx)

df["Period_int"] = pd.to_datetime(df["Period_int"])

KPINameList = df['KPIName'].unique()
GrainNameList = df['Grain'].unique()
Level1NameList =  df['Level1Name'].unique()
Level2NameList = df['Level2Name'].unique().tolist()
#Level3NameList = df['Level3Name'].unique()

#print(df.columns)

KPINameColor    = dict(d_kpi.set_index('d_kpi_id')['KPIName'].to_dict())
Level0NameColor = dict(d_level0.set_index('LevelName')['Color'].to_dict())
Level1NameColor = dict(d_level1.set_index('Level1Name')['Level1Color'].to_dict())
Level2NameColor = dict(d_level2.set_index('Level2Name')['Level2Color'].to_dict())
#Level3NameColor = dict(d_level3.set_index('d_level3_id')['Level3Name'].to_dict())

#df['Level1Color'] = df['Level1Color'].apply(lambda x: "'" + str(x) + "'")

items = [
    dbc.DropdownMenuItem("First"),
    dbc.DropdownMenuItem(divider=True),
    dbc.DropdownMenuItem("Second"),
]


pd.set_option('display.expand_frame_repr', False)
#dbConnection.close()
# external CSS stylesheets

external_stylesheets = ['https://codepen.io/hessing/pen/oNjJbxR.css']
#
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
mapbox_access_token = "pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w"

layout = {'autosize': True,
          'automargin': True,
          'margin': dict(l=30, r=30, b=20, t=40),
          'hovermode': "closest",
          'plot_bgcolor': "LightSteelBlue",#2a3642
          'paper_bgcolor': "LightSteelBlue",
          'text_color' : "#36383b",
          'font' : dict(
              family="Montserrat",
              size=12,
              color="#36383b"
           ),
          'legend': dict(font=dict(size=10), orientation="h", color='#c6ccd3'), 'title': "Satellite Overview",
          'mapbox': dict(
              accesstoken=mapbox_access_token,
              style="light",
              center=dict(lon=-78.05, lat=42.54),
              zoom=7,
          )
          }


#app.layout = html.Div(
#    [dcc.Dropdown(
#             id="Grain",
#             options=[
#             {'label': i, 'value': i} for i in KPIFramework.Grain.unique()
#            ],
#             multi=False,
#             value='MonthName',
#             className="dcc_control",
#             ),
#        html.Div(
#            [dcc.Graph(id='graph-with-slider')
#            ])
#    ])

app = dash.Dash(__name__)
app.layout = html.Div(
        [html.Div([html.Div([html.H3(dcc.Dropdown(
                                    id="Level1NameSelect",
                                    options=[{'label': i, 'value': i} for i in Level1NameList],
                                    multi=False,
                                    value="ICON Blockchain",
                                    style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
                                    ),
                                    html.H5(dcc.Dropdown(
                                    id="Level2NameSelect",
                                    options=[{'label': str(i), 'value': str(i)} for i in Level2NameList],
                                    multi=True,
                                    value=["Blockmove","ICON Foundation","ReliantNode"],
                                    style={'width': '60%', 'float': 'right', 'display': 'inline-block','marginBottom': 0, 'marginTop': 0}
                                    ),
                                    ),
                            ],
                            id="TimeContainer",
                            className="dcc_control",

                            ),
                        html.Div(
                            [
                            html.Img(
                                    src=app.get_asset_url("daopi.png"),
                                    id="plotly-image",
                                    style={
                                          "height": "140px",
                                          "width": "auto",
                                          "margin-bottom": "60px",
                                    },
                                    ),
                            html.Img(
                                    src=app.get_asset_url("animeanimation.svg"),
                                    id="plotly-image2",
                                    style={
                                        "height": "140px",
                                        "width": "auto",
                                        "margin-bottom": "60px",
                                    },
                                    )
                            ],
                            className="BlockchainImage",
                        ),
                    ],
                    ),
                    html.Div([html.Div([dcc.RadioItems(
                                    id="GrainSelect",
                                    options=[{'label': i, 'value': i} for i in GrainNameList],
                                    className="dcc_control",
                                    value="MonthName",
                                    style = dict(
                                        family="Montserrat",
                                        size=10,
                                        color="#d4d4d4"
                                        ),
                                    ),
                                    dcc.RadioItems(
                                    id="DBColorVar",
                                    options=[{'label': 'Light', 'value': 'Light'},
                                            {'label': 'Dark', 'value': 'Dark'}],
                                    className="dcc_control",
                                    value="Dark",
                                    style = dict(
                                        family="Montserrat",
                                        size=10,
                                        color="#d4d4d4"
                                        ),
                                    ),
                                    ],
                                    id='radioitem1',
                                    className="dcc_control",
                                    #style={'width': '48%', 'float': 'left', 'display': 'inline-block'}
                                ),
                                dbc.Row(
                                [
                                 dbc.Col(
                                     dbc.DropdownMenu(
                                         label="Dropdown (default)", children=items, direction="down"
                                     ),
                                     width="auto",),
                                ],),
                                html.H5(dcc.Dropdown(
                                    id="KPISelect",
                                    options=[{'label': i, 'value': i} for i in KPINameList],
                                    multi=False,
                                    value="# SelfStaked",
                                    style={'width': '30%', 'float': 'middle', 'display': 'inline-block','marginBottom': 0, 'marginTop': 0}
                                    ),
                                    ),
                    ],
                    id='radioitems1',
                    className="dcc_control",
                   # style={'width': '48%', 'float': 'left', 'display': 'inline-block'}
                    ),
                    html.Div(
                    [dcc.Graph(
                            id='graph-overall-time',
                            className="control_label"
                            ),
                    ],
                    id="Graphoveralltime",
                    className="dcc_control",
                    ),
                    html.Div(
                    [dcc.Graph(
                            id='graph-with-slider',
                            className="control_label"
                            ),
                    ],
                    id="GraphContainer",
                    className="dcc_control",
                    ),
                    html.Div(
                    [dcc.Graph(
                            id='graph-level2compare',
                            className="control_label"
                            ),
                    ],
                    id="GraphLevel2",
                    className="dcc_control",
                    ),
#                    html.Div(
#                    [dcc.Graph(
#                            id='KPIBox',
#                            className="control_label"
#                            ),
#                    ],
#                    id="KPIBox",
#                    className="dcc_control",
#                    ),
        ],
id='Filters',
className="dcc_control",
style=
#{'width': '48%', 'float': 'left', 'display': 'inline-block'}
{'background-color': '#2a3642'
}
)

def CalculationLogic(Calculation):
    if Calculation==2:
        CalculationString= "df_by_Level2Name['Numerator'] / df_by_Level2Name['Denominator']"
        return CalculationString
    elif Calculation==1:
        CalculationString= "df_by_Level2Name['Numerator']"
        return CalculationString

def CalculationLogic2(Calculation):
    if Calculation==2:
        CalculationString= "df_by_Level1Name['Numerator'] / df_by_Level1Name['Denominator']"
        return CalculationString
    elif Calculation==1:
        CalculationString= "df_by_Level1Name['Numerator']"
        return CalculationString

def DBColorDEF(DBColor):
    if DBColor=='Light':
        ColorHex= ['"#d8d6c8"','"#191970"']
        return ColorHex
    elif DBColor=='Dark':
        ColorHex= ['"#252f3b"','"#c1c1c1"']
        return ColorHex


def NotationDEF(Notation):
    if Notation=='%':
        Notation= ['".1%"']
        return Notation
    elif Notation=='#':
        Notation= ['""']
        return Notation

#Calculation = KPIFramework.Calculation.unique()[0]
#y = CalculationLogic(Calculation)
#ydf = pd.DataFrame(data=y)
#print(eval(y))
#print(y)
#print(KPIFramework['Numerator'])

def update_filter(df,GrainSelect,KPISelect,Level1NameSelect,Level2NameSelect):
    dff= df[
      (df["Grain"] == GrainSelect)
    & (df["KPIName"] == KPISelect)
    & (df["Level1Name"] == Level1NameSelect)
    & df["Level2Name"].isin(Level2NameSelect)
    ]
    return dff

def update_filter_l1(dfl1,GrainSelect,KPISelect,Level1NameSelect):  #,Level2NameSelect
    dff= dfl1[
      (dfl1["Grain"] == GrainSelect)
    & (dfl1["KPIName"] == KPISelect)
    & (dfl1["Level1Name"] == Level1NameSelect)
  #  & df["Level2Name"].isin(Level2NameSelect)
    ]
    return dff

@app.callback(
    Output('graph-overall-time', 'figure'),
        [Input('GrainSelect', 'value'),
        Input("KPISelect", "value"),
        Input("Level1NameSelect", "value"),
       # Input("Level2NameSelect", "value"),
        Input("DBColorVar", "value"),
        ]
)

def update_mainfigure(GrainSelect,KPISelect,Level1NameSelect,DBColorVar):   #,Level2NameSelect
    dff = update_filter_l1(dfl1, GrainSelect,KPISelect,Level1NameSelect)       #,Level2NameSelect
    traces3 = []
    DBColor = DBColorDEF(DBColorVar)
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    Calculation = dff.Calculation.unique()[0]
    for i in df.Level1Name.unique():
        df_by_Level1Name = dff[dff['Level1Name'] == i]
        y = eval(CalculationLogic2(Calculation))
        traces3.append(dict(
            x=df_by_Level1Name['Period_int'],
            y=y,
            text=df_by_Level1Name['Level1Name'],
            color=df_by_Level1Name['Level1Name'],
            color_discrete_map=Level1NameColor,
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            type= 'Scatter',
            name=i,
            transforms = [dict(
                type='aggregate',
                groups=df_by_Level1Name['Period_int'],
                aggregations=[
                dict(target='Numerator', func='sum'),#, enabled=True
                dict(target='Denominator', func='sum')#, enabled=True
                ]
                ),
            ]
            )
        )
    return {
        'data': traces3,
        'layout': dict(
            xaxis=dict(type= 'string',
                        title= '',
                        gridcolor=eval(DBColor[0]),#'#c4c4c4',
                        range= [df_by_Level1Name['Period_int'].min()+ datetime.timedelta(days=-10), df_by_Level1Name['Period_int'].max()+ datetime.timedelta(days=10)],
                        showgrid=False,
                        gridwidth=0.1,
                        showline=True,
                        linewidth=2,
                        linecolor=df_by_Level1Name['Level1Color'].unique().astype(str),
                        font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1]),#'#c1c1c1'
                         )
            ),
            yaxis=dict(title= '',
                       range=[df_by_Level1Name['Numerator'].min()*0.9, df_by_Level1Name['Numerator'].max()*1.1],
                       gridcolor=eval(DBColor[0]),#'#252f3b',
                       showline=True,
                       linecolor=df_by_Level1Name['Level1Color'].unique().astype(str),
                       linewidth=2,
                      # tickformatstops=[
                      #     dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                      #     dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                      #     dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                      #     dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                      #     dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                      #     dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                      #     dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                      #     dict(dtickrange=["M12", None], value="%Y Y")
                      # ]
                       tickformat=eval(Notation[0]),
                       showgrid=True,
                       gridwidth=0.5,
            ),
            margin={'l': 80, 'b': 52, 't': 57, 'r': 63},
            legend=dict(
                    font=dict(
                        size=16,
                        family="Montserrat",
                        color=eval(DBColor[1])
                    ),
                    orientation="h",
                    ),

            plot_bgcolor = eval(DBColor[0]),
            paper_bgcolor= eval(DBColor[0]),#"#252f3b",
            font= dict(
                    family="Montserrat",
                    size=15,
                    color=eval(DBColor[1])
            ),
            images=dict(
                source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
                xref="paper", yref="paper",
                x=1, y=1.05,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
                ),
            title=dict(text =str(KPISelect)+' over time', #+' -     selected: '+str(Level2NameSelect),
                              font =dict(family='Montserrat',
                              size=22,
                              color = eval(DBColor[1])),
            ),
            hovermode='closest',
            transition = {'duration': 500},
        )
    }

@app.callback(
    Output('graph-with-slider', 'figure'),
        [Input('GrainSelect', 'value'),
        Input("KPISelect", "value"),
        Input("Level1NameSelect", "value"),
        Input("Level2NameSelect", "value"),
        Input("DBColorVar", "value"),
        ]

)

def update_figure(GrainSelect,KPISelect,Level1NameSelect,Level2NameSelect,DBColorVar):
    dff = update_filter(df, GrainSelect,KPISelect,Level1NameSelect,Level2NameSelect)
    traces = []
    DBColor = DBColorDEF(DBColorVar)
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    #KPIName = str(eval(KPISelect))
    Level2Entitytype = str(dff.Level2Entitytype.unique()[0])
    Calculation = dff.Calculation.unique()[0]
    for i in df.Level2Name.unique():
        df_by_Level2Name = dff[dff['Level2Name'] == i]
        #Calculation = df_by_Level2Name.Calculation.unique()[0]
        y = eval(CalculationLogic(Calculation))
        traces.append(dict(
            x=df_by_Level2Name['Period_int'], ##df_by_Level2Name['d_date_id'],
            y=y, #"df_by_Level2Name['Numerator']", # y(), #df_by_Level2Name['Numerator'],
            text=df_by_Level2Name['Level2Name'],
            color=df_by_Level2Name['Level2Name'],
            color_discrete_map= Level2NameColor,
            mode='lines+markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            type= 'Scatter',
            name=i,
            transforms = [dict(
                type='aggregate',
                groups=df_by_Level2Name['Period_int'],
                aggregations=[
                dict(target='Numerator', func='sum', enabled=True),
                dict(target='Denominator', func='sum', enabled=True)
                ]
            ),
            ]
        ))
    return {
        'data': traces,
        'layout': dict(
            xaxis=dict(type= 'string',
                        title= '',
                        gridcolor=eval(DBColor[0]),#'#c4c4c4',
                        range= [df_by_Level2Name['Period_int'].min() + datetime.timedelta(days=-10), df_by_Level2Name['Period_int'].max() + datetime.timedelta(days=10)],
                        showgrid=False,
                        gridwidth=0.1,
                        showline=True,
                        linewidth=2,
                        linecolor=df_by_Level2Name['Level1Color'].unique().astype(str),
                        font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1]),#'#c1c1c1'
                         )
            ),
            yaxis=dict(title= '',
                       range=[df_by_Level2Name['Numerator'].min()*0.9, df_by_Level2Name['Numerator'].max()*1.1],
                       gridcolor=eval(DBColor[0]),#'#252f3b',
                       showline=True,
                       linecolor=df_by_Level2Name['Level1Color'].unique().astype(str),
                       linewidth=2,
                      # tickformatstops=[
                      #     dict(dtickrange=[None, 1000], value="%H:%M:%S.%L ms"),
                      #     dict(dtickrange=[1000, 60000], value="%H:%M:%S s"),
                      #     dict(dtickrange=[60000, 3600000], value="%H:%M m"),
                      #     dict(dtickrange=[3600000, 86400000], value="%H:%M h"),
                      #     dict(dtickrange=[86400000, 604800000], value="%e. %b d"),
                      #     dict(dtickrange=[604800000, "M1"], value="%e. %b w"),
                      #     dict(dtickrange=["M1", "M12"], value="%b '%y M"),
                      #     dict(dtickrange=["M12", None], value="%Y Y")
                      # ]
                       tickformat=eval(Notation[0]),
                       showgrid=True,
                       gridwidth=0.5,
            ),
            margin={'l': 80, 'b': 52, 't': 57, 'r': 63},
            legend=dict(
                    font=dict(
                        size=16,
                        family="Montserrat",
                        color=eval(DBColor[1])
                    ),
                    orientation="h",
                    ),

            plot_bgcolor = eval(DBColor[0]),
            paper_bgcolor= eval(DBColor[0]),#"#252f3b",
            font= dict(
                    family="Montserrat",
                    size=15,
                    color=eval(DBColor[1])
            ),
            images=dict(
                source="https://raw.githubusercontent.com/cldougl/plot_images/add_r_img/vox.png",
                xref="paper", yref="paper",
                x=1, y=1.05,
                sizex=0.2, sizey=0.2,
                xanchor="right", yanchor="bottom"
                ),
            title=dict(text =str(KPISelect)+' over time per '+Level2Entitytype, #+' -     selected: '+str(Level2NameSelect),
                              font =dict(family='Montserrat',
                              size=22,
                              color = eval(DBColor[1])),
            ),
            hovermode='closest',
            transition = {'duration': 500},
        )
    }

@app.callback(
    Output('graph-level2compare', 'figure'),
        [Input('GrainSelect', 'value'),
        Input("KPISelect", "value"),
        Input("Level1NameSelect", "value"),
        Input("Level2NameSelect", "value"),
        Input("DBColorVar", "value")
        ]
)

def update_level2Graph(GrainSelect,KPISelect,Level1NameSelect,Level2NameSelect,DBColorVar):
    dff = update_filter(df, GrainSelect,KPISelect,Level1NameSelect,Level2NameSelect)
    traces2 = []
    DBColor = DBColorDEF(DBColorVar)
    for i in df.Level2Name.unique():
        df_by_Level2Name = dff[dff['Level2Name'] == i]
        traces2.append(dict(
            y=df_by_Level2Name['Level2Name'],
            x=df_by_Level2Name['Numerator'],
            color=df_by_Level2Name['Level2Name'],
            type= 'bar',
            orientation="h",
            name=i,
            transforms = [dict(
                type='aggregate',
                groups=df_by_Level2Name['Level2Name'],
                aggregations=[
                dict(target='Numerator', func='sum', enabled=True)
            ])
        ]
        ))

    return {
        'data': traces2,
        'layout': dict(
            type='bar',
            xaxis=dict(type= 'string',
                        title= '',
                        gridcolor=eval(DBColor[0]),
                        range= [df_by_Level2Name['Numerator'].min(), df_by_Level2Name['Numerator'].max()],
                        showgrid=False,
                        gridwidth=0.1,
                        showline=True,
                        font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1])
                        )
            ),
            yaxis=dict(title= '',
                       gridcolor=eval(DBColor[0]),
                       showline=True,
                       showgrid=True,
                       categoryorder="total ascending",
                       gridwidth=0.5,
            ),
            margin={'l': 80, 'b': 52, 't': 57, 'r': 63},
            legend=dict(
                    font=dict(
                        size=16,
                        family="Montserrat",
                        color=eval(DBColor[1])
                    ),
                    orientation="h",
                    ),

            plot_bgcolor = eval(DBColor[0]),
            paper_bgcolor= eval(DBColor[0]),
            font= dict(
                    family="Montserrat",
                    size=15,
                    color=eval(DBColor[1])
            ),
            title=dict(text ='Compare over level 2',
                              font =dict(family='Montserrat',
                              size=22,
                              color = eval(DBColor[1]))),
            hovermode='closest',
            transition = {'duration': 500},
        )
    }


#x = update_figure(GrainSelected='MonthName')
#print(x)

if __name__ == "__main__":
    app.run_server(debug=True)  #,config=config
