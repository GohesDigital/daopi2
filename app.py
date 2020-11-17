import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import plotly.graph_objects     as go
from dash.dependencies import Input, Output, State
import datetime
# import mysql.connector
from sqlalchemy import create_engine

import pandas as pd
import flask
import glob
import os
import dash_bootstrap_components as dbc
import json

image_directory = '/Users/chriddyp/Desktop/'
list_of_images = [os.path.basename(x) for x in glob.glob('{}*.png'.format(image_directory))]
static_image_route = '/static/'

# engine = create_engine('mysql+pymysql://root:Handschoen92@localhost:3306/kpiframework')
# dbConnection    = engine.connect()

# SQL Retrieve data
keys = ['d_kpi_id', 'd_level0_id', 'd_level1_id', 'd_level2_id']  # 'd_date_id',
keysl1 = ['d_kpi_id', 'd_level0_id', 'd_level1_id']
ListGrain = ['int_day', 'int_month', 'int_quarter', 'int_year']

# Dataframes
# f_kpi           = pd.read_sql("select * from kpiframework.f_kpi", dbConnection);

KPIFramework = pd.DataFrame(
    pd.read_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/KPIFramework_Python.csv'));

columnsdf1 = KPIFramework.columns.tolist()
columnsdf1.remove('d_level2_id')
columnsdf1.remove('Numerator')
columnsdf1.remove('Denominator')
columnsdf1.remove('Numerator_LP')
columnsdf1.remove('Denominator_LP')
columnsdf1.remove('Period_int_lp')

columnsdf2 = KPIFramework.columns.tolist()
columnsdf2.remove('Numerator')
columnsdf2.remove('Denominator')
columnsdf2.remove('Numerator_LP')
columnsdf2.remove('Denominator_LP')
columnsdf2.remove('Period_int_lp')

KPIFrameworkl1 = KPIFramework.groupby(columnsdf1, as_index=False).agg(
    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})
KPIFrameworkl2 = KPIFramework.groupby(columnsdf2, as_index=False).agg(
    {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'})

KPIFrameworkl1.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/KPIFrameworkl1.csv',
                      index=False)
KPIFrameworkl2.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/KPIFrameworkl2.csv',
                      index=False)

# KPIFramework    = pd.concat([KPIFrameworkDay, KPIFrameworkMonth,KPIFrameworkQuarter,KPIFrameworkYear])
d_kpi = pd.DataFrame(
    pd.read_csv("C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/d_kpi.csv", sep=';',
                index_col=False));
# d_kpi           = pd.DataFrame(pd.read_excel(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/d_kpi.xlsx',sheet_name='1'));  #, columns=['d_kpi_id', 'KPIName'], index_col=0)
d_level0 = pd.DataFrame(pd.read_excel(
    r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/LEVEL0_Blockchain_Library.xlsx',
    sheet_name='1'));
d_level1 = pd.DataFrame(
    pd.read_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/LEVEL1_ICON_Library.csv',
                sep=';', index_col=False));
d_level2 = pd.DataFrame(
    pd.read_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/LEVEL2_ICON_Library.csv',
                sep=';', index_col=False));

df_list_l1 = [KPIFrameworkl1, d_kpi, d_level0, d_level1]
df_list = [KPIFrameworkl2, d_kpi, d_level0, d_level1, d_level2]  # d_date

# dff.drop(dff.filter(regex='Level2').columns, axis=1, inplace=True)
# dff.drop(dff.filter(regex='level2').columns, axis=1, inplace=True)

# dfflevel1 = dff.groupby('d_kpi_id').agg({'Denominator': 'sum', 'Numerator': 'sum'})

dfl1 = df_list_l1[0]
for i, x in zip(df_list_l1[1:], range(len(keysl1))):
    dfl1 = dfl1.merge(i, on=keysl1[x])

dfl1["Period_int"] = pd.to_datetime(dfl1["Period_int"])

dfl1.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/dfl1.csv', index=False)

dfl2 = df_list[0]
for g, t in zip(df_list[1:], range(len(keys))):
    dfl2 = dfl2.merge(g, on=keys[t])


dfl2Compare = df_list[0]
for g, t in zip(df_list[1:], range(len(keys))):
    dfl2Compare = dfl2Compare.merge(g, on=keys[t])

dfl2["Period_int"] = pd.to_datetime(dfl2["Period_int"])
dfl2Compare["Period_int"] = pd.to_datetime(dfl2Compare["Period_int"])

dfl2.to_csv(r'C:/Users/nickh/PycharmProjects/daopi2/assets/Attributes/Generic attributes/dfl2.csv', index=False)
href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"

KPINameList = dfl2['KPIName'].unique()
GrainNameList = dfl2['Grain'].unique()
Level1NameList = dfl2['Level1Name'].unique()
Level2NameList = dfl2['Level2Name'].unique().tolist()
# Level3NameList = dfl2['Level3Name'].unique()

KPINameListCompare = dfl2Compare['KPIName'].unique()
GrainNameListCompare = dfl2Compare['Grain'].unique()
Level1NameListCompare = dfl2Compare['Level1Name'].unique()
Level2NameListCompare = dfl2Compare['Level2Name'].unique().tolist()

KPINameColor = dict(d_kpi.set_index('d_kpi_id')['KPIName'].to_dict())
Level0NameColor = dict(d_level0.set_index('LevelName')['Color'].to_dict())
Level1NameColor = dict(d_level1.set_index('Level1Name')['Level1Color'].to_dict())
Level2NameColor = dict(d_level2.set_index('Level2Name')['Level2Color'].to_dict())
# Level3NameColor = dict(d_level3.set_index('d_level3_id')['Level3Name'].to_dict())
# dfl2['Level1Color'] = dfl2['Level1Color'].apply(lambda x: "'" + str(x) + "'")
print(Level1NameColor)
columnsdftotal = KPIFramework.columns.tolist()
columnsdftotal.remove('d_level0_id')
columnsdftotal.remove('d_level1_id')
columnsdftotal.remove('d_level2_id')
columnsdftotal.remove('Numerator')
columnsdftotal.remove('Denominator')
columnsdftotal.remove('Numerator_LP')
columnsdftotal.remove('Denominator_LP')
columnsdftotal.remove('Period_int_lp')

pd.set_option('display.expand_frame_repr', False)


app = dash.Dash(__name__)
#app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
tab1_content = dbc.CardBody(
    dbc.Row([
    dbc.Col(
        dcc.Graph(id='graph-overall-time',
                  config={
                    'modeBarButtonsToAdd': ['customButton'],
                    'modeBarButtonsToRemove': ['zoom2d','hoverCompareCartesian','logo'],
                    'displaylogo': False,
                  },
                  className="pretty_graph"
                  )
        ,className="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6"
    ),
    dbc.Col(
        dcc.Graph(id='graph-level1compare',
                  config={
                      'modeBarButtonsToAdd': ['customButton'],
                      'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'logo'],
                      'displaylogo': False,
                  },
                  className="pretty_graph2"
                  )
        ,className="col-12 col-sm-12 col-md-12 col-lg-5 col-xl-5"
    )
    ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_tab"
)

tab2_content = dbc.CardBody(
    dbc.Row([
    dbc.Col(
        dcc.Graph(id='graph-with-slider',
                  config={
                      'modeBarButtonsToAdd': ['customButton'],
                      'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'logo'],
                      'displaylogo': False,
                  },
                  className="pretty_graph"
                  )
        ,className="col-12 col-sm-12 col-md-12 col-lg-6 col-xl-6"
    ),
    dbc.Col(
        dcc.Graph(id='graph-level2compare',
                  config={
                      'modeBarButtonsToAdd': ['customButton'],
                      'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'logo'],
                      'displaylogo': False,
                  },
                 className="pretty_graph2"
                  )
        ,className="col-12 col-sm-12 col-md-12 col-lg-5 col-xl-5"
    ),
    ],className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12"
    ),className="row-cols-sm-12 row-cols-md-12 row-cols-lg-12 row-cols-xl-12 pretty_tab"
)

tab1_compare = dbc.CardBody(
    dbc.Row([
    dbc.Col(
        dcc.Graph(id='graph-compare-kpi',
                  config={
                    'modeBarButtonsToAdd': ['customButton'],
                    'modeBarButtonsToRemove': ['zoom2d','hoverCompareCartesian','logo'],
                    'displaylogo': False,
                  },
                  className="pretty_graph"
                  )
        ,className="col-12 col-sm-12 col-md-12 col-lg-7 col-xl-8"
),
    ]
),
)


tabs = html.Div(dbc.Tabs(
    [dbc.Tab(label="Tab 1", children=[tab1_content]),
     dbc.Tab(label="Tab 2", children=[tab2_content]),
  #   dbc.Tab(label="Tab 3", children=[tab3_content]),
    ]
    ,card="true"

),
),

tabscompare = html.Div(dbc.Tabs(
    [dbc.Tab(label="Tab 1", children=[tab1_compare]),
  #   dbc.Tab(label="Tab 3", children=[tab3_content]),
    ]
    ,card="true"

),
),

tabscontainer = html.Div(dbc.Tabs(
    [dbc.Tab(label="Tab 1", children=[tabs]),
     dbc.Tab(label="Tab 2", children=[tabscompare]),
  #   dbc.Tab(label="Tab 3", children=[tab3_content]),
    ]
    ,card="true"

),
),

#tabs2 = dbc.Tabs(
#    [dbc.Tab(label="Tab 3", children=[tab3_content]),
#    ]
#    ,card="true"
#),
#

RadioStyle = html.Div([
    daq.BooleanSwitch(
        id='DarkLightSwitch',
        on=True,
        color="#01002a",
        label="Dark",
        labelPosition="top"
    ),
    ],
)

Radiograin = html.Div([
        dbc.RadioItems(
            id="GrainSelect",
            options=[{'label': i, 'value': i} for i in GrainNameList],
            value="MonthName",
            labelStyle={'display': 'inline-block'},
            style=dict(
               family="Montserrat",
               size=10,
               inline='True',
               color="#d4d4d4",
               align="right"
           ),
        ),
    ],
        id="RadioItemContainer",
       # className="eight columns",
),

    #    className="dcc_control",
    # style={'width': '48%', 'float': 'left', 'display': 'inline-block'}


Levelsdropdown = dbc.Card([html.Div(dcc.Dropdown(
    id="Level1NameSelect",
    options=[{'label': i, 'value': i} for i in Level1NameList],
    multi=True,
   # className="dcc_control",
    style =
    {
        "font-size": "14px",
      #  "color": "#01002a",
        "background-color": "#144a68"
    },
    value=["ICON Blockchain", "Ethereum"],
    )#,className="dcc_control"
    ),
    html.Div(dcc.Dropdown(
        id="Level2NameSelect",
        options=[{'label': str(i), 'value': str(i)} for i in Level2NameList],
        multi=True,
     #   className="dash-bootstrap",
        style =
        {
        "font-size": "14px",
      #  "color": "#01002a",
        "background-color": "#144a68"
        },
        value=["Blockmove", "ICON Foundation", "ReliantNode"],
    ),
    ),
],
    body=True,
    className="pretty_container",
    id="TimeContainer",
  #  className="control_label",
)
KPIdropdown = html.Div([
    dbc.Select(
        id="KPISelect",
        options=[{'label': i, 'value': i} for i in KPINameList],
        value="percentage stake health",
  ),
],
    className="pretty_container",
    id="KPIContainer",
)
KPIdropdownCompare = html.Div([
    dbc.Select(
        id="KPISelectCompare",
        options=[{'label': i, 'value': i} for i in KPINameListCompare],
        value="number of selfstaked",
    ),
],
    className="pretty_container",
    id="KPIContainerCompare",
)
nav = dbc.Nav(
    [
        dbc.NavItem(dbc.NavItem("Active",className="flex-sm-fill text-sm-center nav-link active", active=True)),
        dbc.NavItem(dbc.NavItem("A link",className="flex-sm-fill text-sm-center nav-link active", active=True)),
        dbc.NavItem(dbc.NavItem("Another link",className="flex-sm-fill text-sm-center nav-link active", active=True)),
        dbc.NavItem(dbc.NavItem("Disabled",className="flex-sm-fill text-sm-center nav-link active", active=True)),
    ],
    pills=True,
)

fade = html.Div(
[dbc.Button(
            "Toggle fade", id="fade-transition-button", className="mb-3"
        ),
        dbc.Fade(
        dbc.Card(
        dbc.CardBody(
            [ html.P(["Print icon: ",
                        html.Span(className="glyphicon glyphicon-search"),
                                #  style ={
                                #        "color": "#144a68"
                                #        })
                        ],
                        style = {
                        "color": "#144a68"
                         }
                ),
                html.Div(Levelsdropdown,
                        id='Levels'),
                html.Div(KPIdropdown,
                        id='KPI'),
                html.Div(KPIdropdownCompare,
                        id='KPICompare'),
            ]
        ),className='pretty_container'
        ),
        id="fade-transition",
        is_in=True,
        style={"transition": "opacity 100ms ease"}

)
],className='pretty_container'
)

@app.callback(
    Output("fade-transition", "is_in"),
    [Input("fade-transition-button", "n_clicks")],
    [State("fade-transition", "is_in")],
)
def toggle_fade(n, is_in):
    if not n:
        # Button has never been clicked
        return True
    return not is_in

app.layout = html.Div([
    dbc.Row([dbc.Col(
        fade,className="col-sm-12 col-md-12 col-lg-2 col-xl-3"
        ),
        dbc.Col(
            [
            html.Div(nav),
            html.Div(RadioStyle,
                    className="col-sm-4 col-md-4 col-lg-2 col-xl-1"
                    ),
            html.Div(Radiograin,
                    className="col-sm-6 col-md-6 col-lg-5 col-xl-1"
                    ),
            html.Div(tabs,
                     id="tabcontainer"
                     ),
            html.Div(dcc.Graph(id='graph-compare-kpi',
                          config={
                              'modeBarButtonsToRemove': ['zoom2d', 'hoverCompareCartesian', 'logo'],
                              'displaylogo': False,
                          },
                        ),className="col-sm-12 col-md-12 col-lg-10 col-xl-9 "
                     ),
        ],className="col-sm-12 col-md-12 col-lg-10 col-xl-9"
        ),

        #dbc.Col(
        #    [
        #    html.Div(tabs2,
        #             id="tabcontainer2",
        #           #   className="pretty_container"
        #             )
        #    ],className="col-lg-6"
        #)
    ]#,className="row-cols-lg-6"
    ),
],
)
def CalculationLogic(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level2Name['Numerator'] / df_by_Level2Name['Denominator']"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level2Name['Numerator']"
        return CalculationString


def CalculationLogic2(Calculation):
    if Calculation == 2:
        CalculationString = "df_by_Level1Name['Numerator'] / df_by_Level1Name['Denominator']"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "df_by_Level1Name['Numerator']"
        return CalculationString

def CalculationLogicTotal(Calculation):
    if Calculation == 2:
        CalculationString = "dff['Numerator'] / dff['Denominator']"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "dff['Numerator']"
        return CalculationString

def CalculationLogicTotalCompare(Calculation):
    if Calculation == 2:
        CalculationString = "dffcomp['Numerator'] / dffcomp['Denominator']"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "dffcomp['Numerator']"
        return CalculationString

def AggregateNumerator(Calculation):
    if Calculation == 2:
        CalculationString = "'sum'"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "'avg'"
        return CalculationString
    elif Calculation == 3:
        CalculationString = "'max'"
        return CalculationString


def AggregateDenominator(Calculation):
    if Calculation == 2:
        CalculationString = "'sum'"
        return CalculationString
    elif Calculation == 1:
        CalculationString = "'avg'"
        return CalculationString
    elif Calculation == 3:
        CalculationString = "'max'"
        return CalculationString


def DBColorDEF(DBColor):
    if DBColor == 'False':
        ColorHex = ['"#d8d6c8"', '"#191970"']
        return ColorHex
    elif DBColor == 'True':
        ColorHex = ['"#144a68"', '"#c1c1c1"']
        return ColorHex

def NotationDEF(Notation):
    if Notation == '%':
        Notation = ['".1%"']
        return Notation
    elif Notation == '#':
        Notation = ['""']
        return Notation
    elif Notation == '$':
        Notation = ['"$"']
        return Notation

#def Level0_Attribuut(d_kpi,KPISelect):
#    Level0_Attribuut = d_kpi['Level0_Attribuut'][
#        (d_kpi["KPIName"] == KPISelect)
#        ]
#    return Level0_Attribuut
#
#@app.callback(
#    Output('Level0_Attribuut', 'value'),
#    [Input("KPISelect", "value"),
#     ]
#)



def update_filter(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect):
    dff = dfl2[
        (dfl2["Grain"] == GrainSelect)
        & (dfl2["KPIName"] == KPISelect)
        & (dfl2["Level1Name"].isin(Level1NameSelect))
        & dfl2["Level2Name"].isin(Level2NameSelect)
        ]
    return dff

def update_filter_compare(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect):
    dffcomp = dfl2Compare[
        (dfl2Compare["Grain"] == GrainSelect)
        & (dfl2Compare["KPIName"] == KPISelectCompare)
        & (dfl2Compare["Level1Name"].isin(Level1NameSelect))
        & dfl2Compare["Level2Name"].isin(Level2NameSelect)
        ]
    return dffcomp


def update_filter_l1(dfl1, GrainSelect, KPISelect, Level1NameSelect):  # ,Level2NameSelect
    dff = dfl1[
        (dfl1["Grain"] == GrainSelect)
        & (dfl1["KPIName"] == KPISelect)
        & (dfl1["Level1Name"].isin(Level1NameSelect))
        #  & df["Level2Name"].isin(Level2NameSelect)
        ]
    return dff


#@app.callback(
#    Output('hover-data', 'children'),
#    [Input('graph-overall-time', 'hoverData')])
#def display_hover_data(hoverData):
#    print(hoverData)
#    return json.dumps(hoverData, indent=2)
#
#
#@app.callback(
#    Output('click-data', 'children'),
#    [Input('graph-overall-time', 'clickData')])
#def display_click_data(clickData):
#    print(clickData)
#    return json.dumps(clickData, indent=2)
#
#
#@app.callback(
#    Output('selected-data', 'children'),
#    [Input('graph-overall-time', 'selectedData')])
#def display_selected_data(selectedData):
#    print(selectedData)
#    return json.dumps(selectedData, indent=2)
#
#
#@app.callback(
#    Output('relayout-data', 'children'),
#    [Input('graph-overall-time', 'relayoutData')])
#def display_relayout_data(relayoutData):
#    print(relayoutData)
#    return json.dumps(relayoutData, indent=2)


@app.callback(
    dash.dependencies.Output('DarkLightSwitch', 'label'),
    [dash.dependencies.Input('DarkLightSwitch', 'on')])

def update_output(on):
    return format(on)


@app.callback(
    Output('graph-overall-time', 'figure'),
    [Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("DarkLightSwitch", "label"),
     # Input("Level2NameSelect", "value"),
   #  Input("DBColorVar", "value"),
     ]
)

def update_mainfigure(GrainSelect, KPISelect, Level1NameSelect, DarkLightSwitch):  # ,Level2NameSelect
    dff = update_filter_l1(dfl1, GrainSelect, KPISelect, Level1NameSelect)  # ,Level2NameSelect
    traces3 = []
    DBColor = DBColorDEF(DarkLightSwitch)
    linecolor = "'"+str(dff.Level1Color.unique()[0])+"'"
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    Calculation = dff.Calculation.unique()[0]
    for i in dfl1.Level1Name.unique():
        df_by_Level1Name = dff[dff['Level1Name'] == i]
        y = eval(CalculationLogic2(Calculation))
        traces3.append(dict(
            x=df_by_Level1Name['Period_int'],
            y=y,
            text=df_by_Level1Name['Level1Name'],
            color=df_by_Level1Name['Level1Name'],
            color_discrete_map=Level1NameColor,
            mode='lines',
            line=dict(
                width=5,
                shape="spline",
               # color=eval(linecolor)
            ),
            opacity=0.7,
            marker=dict(
                size=10,
                color="transparent",
                line=dict(width=1,
                          color="white"
                        ),
            ),
            fill='tozeroy',
            type='Scatter',
            name=i,
            transforms=dict(
                type='aggregate',
                groups=df_by_Level1Name['Period_int'],
                aggregations=[
                    dict(target='Numerator', func=AggregateNumerator(Calculation)),  # , enabled=True
                    dict(target='Denominator', func=AggregateDenominator(Calculation))  # , enabled=True
                ]
            ),
        )
        )
    return {
        'data': traces3,
    #    'config': configmodebar,
        'layout': dict(
            xaxis=dict(type='string',
                       title='',
                       gridcolor=eval(DBColor[0]),  # '#c4c4c4',
                       range=[df_by_Level1Name['Period_int'].min() + datetime.timedelta(days=-10),
                              df_by_Level1Name['Period_int'].max() + datetime.timedelta(days=10)],
                       showgrid=False,
                       gridwidth=0.1,
                       showline=True,
                       linewidth=2,
                       linecolor=df_by_Level1Name['Level1Color'].unique().astype(str),
                       font=dict(
                           size=14,
                           family="Trocchi",
                           color=eval(DBColor[1]),  # '#c1c1c1'
                       )
                       ),
            yaxis=dict(title='',
                       range=[df_by_Level1Name['Numerator'].min() * 0.9, df_by_Level1Name['Numerator'].max() * 1.1],
                       gridcolor=eval(DBColor[0]),  # '#252f3b',
                       showline=True,
                       linecolor=df_by_Level1Name['Level1Color'].unique().astype(str),
                       linewidth=2,
                       tickformat=eval(Notation[0]),
                       showgrid=True,
                       gridwidth=0.5,
                       font=dict(
                           size=14,
                           family="Trocchi",
                           color=eval(DBColor[1]),  # '#c1c1c1'
                       )
                       ),
            margin={'l': 80, 'b': 52, 't': 57, 'r': 63},
            legend=dict(
                font=dict(
                    size=16,
                    family="Trocchi",
                    color=eval(DBColor[1])
                ),
                orientation="h",
                yanchor="top",
                y=0.99,
                x=0.01,
                xanchor="left",
            ),
            autosize=True,
            plot_bgcolor=eval(DBColor[0]),
            paper_bgcolor=eval(DBColor[0]),  # "#252f3b",
            font=dict(
                family="Trocchi",
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
            title=dict(text=str(KPISelect) + ' over time',  # +' -     selected: '+str(Level2NameSelect),
                       font=dict(family='Trocchi',
                                 size=22,
                                 color=eval(DBColor[1])),
                       ),
            hovermode='closest',
            transition={'duration': 500},
        )
    }


@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input("DarkLightSwitch", "label"),
     ]

)
def update_figure(GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect, DarkLightSwitch):
    dff = update_filter(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect)
    traces = []
    DBColor = DBColorDEF(DarkLightSwitch)
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    # KPIName = str(eval(KPISelect))
    Level2Entitytype = str(dff.Level2Entitytype.unique()[0])
    Calculation = dff.Calculation.unique()[0]
    for i in dfl2.Level2Name.unique():
        df_by_Level2Name = dff[dff['Level2Name'] == i]
        # Calculation = df_by_Level2Name.Calculation.unique()[0]
        y = eval(CalculationLogic(Calculation))
        traces.append(dict(
            x=df_by_Level2Name['Period_int'],  ##df_by_Level2Name['d_date_id'],
            y=y,  # "df_by_Level2Name['Numerator']", # y(), #df_by_Level2Name['Numerator'],
            text=df_by_Level2Name['Level2Name'],
            color=df_by_Level2Name['Level2Name'],
            color_discrete_map=Level2NameColor,
            mode='lines+markers',
            opacity=0.7,
#           marker={
#               'size': 15,
#               'line': {'width': 0.5, 'color': 'white'}
#           },
            type='Scatter',
            name=i,
            line=dict(
                width=5,
                shape="spline",
 #               color=eval(linecolor)
            ),
            fill='tozeroy',
            transforms=[dict(
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
            xaxis=dict(type='string',
                       title='',
                       gridcolor=eval(DBColor[0]),  # '#c4c4c4',
                       range=[df_by_Level2Name['Period_int'].min() + datetime.timedelta(days=-10),
                              df_by_Level2Name['Period_int'].max() + datetime.timedelta(days=10)],
                       showgrid=False,
                       gridwidth=0.1,
                       showline=True,
                       linewidth=2,
                       linecolor=df_by_Level2Name['Level1Color'].unique().astype(str),
                       font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1]),  # '#c1c1c1'
                       )
                       ),
            yaxis=dict(title='',
                       range=[df_by_Level2Name['Numerator'].min() * 0.9, df_by_Level2Name['Numerator'].max() * 1.1],
                       gridcolor=eval(DBColor[0]),  # '#252f3b',
                       showline=True,
                       linecolor=df_by_Level2Name['Level1Color'].unique().astype(str),
                       linewidth=2,
                       tickformat=eval(Notation[0]),
                       showgrid=True,
                       gridwidth=0.5,
                       ),
            margin={'l': 80, 'b': 32, 't': 37, 'r': 3},
            autosize=True,
            legend=dict(
                font=dict(
                    size=14,
                    family="Trocchi",
                    color=eval(DBColor[1])
                ),
                # orientation="h",
                yanchor="top",
                y=1,
                x=1.01,
                xanchor="left",
            ),
           # legend=dict(
           #     font=dict(
           #         size=16,
           #         family="Montserrat",
           #         color=eval(DBColor[1])
           #     ),
           #     orientation="h",
           # ),
            plot_bgcolor=eval(DBColor[0]),
            paper_bgcolor=eval(DBColor[0]),  # "#252f3b",
            font=dict(
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
            title=dict(text=str(KPISelect) + ' over time per ' + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(family='Montserrat',
                                 size=22,
                                 color=eval(DBColor[1])),
                       ),
            hovermode='closest',
            transition={'duration': 500},
        )
    }

@app.callback(
    Output('graph-compare-kpi', 'figure'),
    [Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("KPISelectCompare", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input("DarkLightSwitch", "label"),
     ]
)


def update_kpicompare(GrainSelect, KPISelect, KPISelectCompare,Level1NameSelect, Level2NameSelect, DarkLightSwitch):
    dfftmp = pd.DataFrame(update_filter(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect))
    dfftmp.fillna(value=0, inplace=True)
    dffcomptmp = update_filter_compare(dfl2Compare, GrainSelect, KPISelectCompare, Level1NameSelect, Level2NameSelect)
    dffcomptmp.fillna(value=0, inplace=True)
    dff = dfftmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'});
    dffcomp = dffcomptmp.groupby(columnsdftotal, as_index=False, sort=False).agg(
        {'Denominator': 'sum', 'Numerator': 'sum', 'Denominator_LP': 'sum', 'Numerator_LP': 'sum'});
    tracestotal = []
    traceskpi = []
    traceskpicomp = []
    DBColor = DBColorDEF(DarkLightSwitch)
    Notation = NotationDEF(str(dfftmp.Notation.unique()[0]))
    NotationComp = NotationDEF(str(dffcomptmp.Notation.unique()[0]))
    KPIList = [KPISelect,KPISelectCompare]
    appendList1 = [tracestotal, traceskpi]
    appendList2 = [tracestotal, traceskpicomp]
    Level2Entitytype = str(dfftmp.Level2Entitytype.unique()[0])
    Calculation = dfftmp.Calculation.unique()[0]
    CalculationComp = dffcomptmp.Calculation.unique()[0]
    ycomp = eval(CalculationLogicTotalCompare(CalculationComp))
    y = eval(CalculationLogicTotal(Calculation))
    xrange = []
    rangekpi = []
    rangekpicomp = []
    for i in appendList1:
        i.append(dict(
            x=dff['Period_int'],
            y=y,
            yaxis='y1',
            mode='lines',
            opacity=0.7,
 #           marker={
 #               'size': 15,
 #               'line': {'width': 0.5, 'color': 'white'}
 #           },
            type='Scatter',
            line=dict(
                width=5,
                shape="spline",
                #               color=eval(linecolor)
            ),
            name=KPIList[0],
            transforms=[dict(
                type='aggregate',
                groups=dff['Period_int'],
                aggregations=[
                    dict(target='Numerator', func='sum', enabled=True),
                    dict(target='Denominator', func='sum', enabled=True)
                ]
            ),
            ]
    ))
    for j in appendList2:
        j.append(dict(
            x=dff['Period_int'],  ##df_by_Level2Name['d_date_id'],
            y=ycomp,  # "df_by_Level2Name['Numerator']", # y(), #df_by_Level2Name['Numerator'],
            # text=df_by_Level2Name['Level2Name'],
            # color=df_by_Level2Name['Level2Name'],
            # color_discrete_map=Level2NameColor,
            mode='lines',
            yaxis='y2',
            secondary_y=True,
            opacity=0.7,
 #           marker={
 #               'size': 15,
 #               'line': {'width': 0.5, 'color': 'white'}
 #           },
            type='Scatter',
            line=dict(
                width=5,
                shape="spline",
                #               color=eval(linecolor)
            ),
            name=KPIList[1],
            transforms=[dict(
                type='aggregate',
                groups=dffcomp['Period_int'],
                aggregations=[
                    dict(target='Numerator', func='sum', enabled=True),
                    dict(target='Denominator', func='sum', enabled=True)
                ]
        ),
        ]
    ))
    rangekpi.append(max(max([x['y'] for x in traceskpi]))*1.1)
    rangekpi.append(min(min([x['y'] for x in traceskpi]))*0.9)
    rangekpicomp.append(max(max([x['y'] for x in traceskpicomp]))* 1.1)
    rangekpicomp.append(min(min([x['y'] for x in traceskpicomp]))* 0.9)
    xrange.append(min(min([x['x'] for x in traceskpi])) + datetime.timedelta(days=-10))
    xrange.append(max(max([x['x'] for x in traceskpi])) + datetime.timedelta(days=10))
    return {
        'data': tracestotal,
        'layout': dict(
            xaxis=dict(type='string',
                       title='',
                       gridcolor=eval(DBColor[0]),  # '#c4c4c4',
                       range=xrange,
                       showgrid=False,
                       gridwidth=0.1,
                       showline=True,
                       linewidth=2,
                     #  linecolor=dff['Level1Color'].unique().astype(str),
                       font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1]),  # '#c1c1c1'
                       )
                       ),
            yaxis=dict(title=str(KPISelect) ,
                       range=rangekpi,
                       gridcolor=eval(DBColor[0]),  # '#252f3b',
                       showline=True,
                      # linecolor=dff['Level1Color'].unique().astype(str),
                       linewidth=2,
                       tickformat=eval(Notation[0]),
                       showgrid=True,
                       gridwidth=0.5,
                       yaxis='y1',
                       secondary_y=False
                       ),
            yaxis2=dict(title= str(KPISelectCompare),
                        range=rangekpicomp,
                       #gridcolor=eval(DBColor[0]),  # '#252f3b',
                       showline=True,
                       #linecolor=df_by_Level2NameCompare['Level1Color'].unique().astype(str),
                       linewidth=2,
                       tickformat=eval(NotationComp[0]),
                       #showgrid=True,
                       #gridwidth=0.5,
                       yaxis='y2',
                       secondary_y=True,
                       #anchor="x",
                       overlaying="y",
                       side="right"
                       ),
            margin={'l': 80, 'b': 52, 't': 57, 'r': 63},
            autosize=True,
            secondary_y=True,
            legend=dict(
                font=dict(
                    size=16,
                    family="Trocchi",
                    color=eval(DBColor[1])
                ),
                orientation="h",
                yanchor="top",
                y=0.99,
                x=0.01,
                xanchor="left",
            ),
            plot_bgcolor=eval(DBColor[0]),
            paper_bgcolor=eval(DBColor[0]),  # "#252f3b",
            font=dict(
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
            title=dict(text=str(KPISelect) + ' over time per vergeleken met ' + str(KPISelectCompare) + ' ' + Level2Entitytype,
                       # +' -     selected: '+str(Level2NameSelect),
                       font=dict(family='Montserrat',
                                 size=22,
                                 color=eval(DBColor[1])),
                       ),
            hovermode='closest',
            transition={'duration': 500},
        )
    }

@app.callback(
    Output('graph-level1compare', 'figure'),
    [Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("DarkLightSwitch", "label")
     ]
)
def update_level1Graph(GrainSelect, KPISelect, Level1NameSelect, DarkLightSwitch):
    dff = update_filter_l1(dfl1, GrainSelect, KPISelect, Level1NameSelect)
    traces2 = []
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    DBColor = DBColorDEF(DarkLightSwitch)
    Calculation = dff.Calculation.unique()[0]
    xrangel1 = []
    for i in dfl1.Level1Name.unique():
        df_by_Level1Name = dff[dff['Level1Name'] == i]
        x = eval(CalculationLogic2(Calculation))
        traces2.append(dict(
            y=df_by_Level1Name['Level1Name'],
            x=x,
            text=x,
            textposition='inside',
            type='bar',
            color=df_by_Level1Name['Level1Name'],
            color_discrete_map={'ICON Blockchain': '#00ced1', 'Ethereum': '#00ced1'},
            orientation="h",
            name=i,
            transforms=[dict(
                type='aggregate',
                groups=df_by_Level1Name['Level1Name'],
                aggregations=[
                    dict(target='Numerator', func='sum', enabled=True),
                    dict(target='Denominator', func='sum', enabled=True)
                ]
            ),
            ]
        ))
    #xrangel1.append(0)
    #xrangel1.append(1)
    #xrangel1.append(max(max(t['x'] for t in traces2)))
    #print(xrangel1)
    #print(traces2)
    return {
        'data': traces2,
        'layout': dict(
            type='bar',
            color_discrete_map={'ICON Blockchain': '#00ced1', 'Ethereum': '#00ced1'},
            xaxis=dict(type='string',
                       title='',
                       gridcolor=eval(DBColor[0]),
                       range=xrangel1, #[df_by_Level1Name['Numerator'].min(), df_by_Level1Name['Numerator'].max()],
                       showgrid=False,
                       gridwidth=0.1,
                       showline=True,
                       tickformat=eval(Notation[0]),
                       font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1])
                       )
                       ),
            yaxis=dict(title='',
                       gridcolor=eval(DBColor[0]),
                       showline=True,
                       showgrid=True,
                       categoryorder="total ascending",
                       gridwidth=0.5,
                       ),
            margin={'l': 140, 'b': 32, 't': 37, 'r': 20},
            #legend=dict(
            #    font=dict(
            #        size=14,
            #        family="Trocchi",
            #        color=eval(DBColor[1])
            #    ),
            #   # orientation="h",
            #    yanchor="top",
            #    y=1,
            #    x=1.01,
            #    xanchor="left",
            #),
            autosize=True,
            plot_bgcolor=eval(DBColor[0]),
            paper_bgcolor=eval(DBColor[0]),
            font=dict(
                family="Trocchi",
                size=15,
                color=eval(DBColor[1])
            ),
            title=dict(text='Compare over level 2',
                       font=dict(family='Montserrat',
                                 size=22,
                                 color=eval(DBColor[1]))),
            hovermode='closest',
            transition={'duration': 500},
        )
    }

@app.callback(
    Output('graph-level2compare', 'figure'),
    [Input('GrainSelect', 'value'),
     Input("KPISelect", "value"),
     Input("Level1NameSelect", "value"),
     Input("Level2NameSelect", "value"),
     Input("DarkLightSwitch", "label")
     ]
)
def update_level2Graph(GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect, DarkLightSwitch):
    dff = update_filter(dfl2, GrainSelect, KPISelect, Level1NameSelect, Level2NameSelect)
    traces2 = []
    Notation = NotationDEF(str(dff.Notation.unique()[0]))
    DBColor = DBColorDEF(DarkLightSwitch)
    Calculation = dff.Calculation.unique()[0]
    for i in dfl2.Level2Name.unique():
        df_by_Level2Name = dff[dff['Level2Name'] == i]
        x = eval(CalculationLogic(Calculation))
        traces2.append(dict(
            y=df_by_Level2Name['Level2Name'],
            x=x,
            text=x,
            textposition='inside',
            texttemplate="%{value:.01%}",
            textformat=eval(Notation[0]),
            color=df_by_Level2Name['Level2Name'],
            type='bar',
            orientation="h",
            name=i,
            color_discrete_map=Level2NameColor,
            transforms=[dict(
                type='aggregate',
                groups=df_by_Level2Name['Level2Name'],
                aggregations=[
                    dict(target='Numerator', func='sum', enabled=True),
                    dict(target='Denominator', func='sum', enabled=True)
                ])
            ]
        ))

    return {
        'data': traces2,
        'layout': dict(
            type='bar',
            xaxis=dict(type='string',
                       title='',
                       gridcolor=eval(DBColor[0]),
                       range=[df_by_Level2Name['Numerator'].min(), df_by_Level2Name['Numerator'].max()],
                       showgrid=False,
                       gridwidth=0.1,
                       showline=True,
                       tickformat=eval(Notation[0]),
                       font=dict(
                           size=14,
                           family="Montserrat",
                           color=eval(DBColor[1])
                       )
                       ),
            yaxis=dict(title='',
                       gridcolor=eval(DBColor[0]),
                       showline=True,
                       showgrid=True,
                       categoryorder="total ascending",
                       gridwidth=0.5,
                       ),
            margin={'l': 140, 'b': 32, 't': 37, 'r': 20},
            showlegend=False,
            #legend=dict(
            #    font=dict(
            #        size=14,
            #        family="Trocchi",
            #        color=eval(DBColor[1])
            #    ),
            #   # orientation="h",
            #    yanchor="top",
            #    y=1,
            #    x=1.01,
            #    xanchor="left",
            #),
            autosize=True,
            plot_bgcolor=eval(DBColor[0]),
            paper_bgcolor=eval(DBColor[0]),
            font=dict(
                family="Montserrat",
                size=15,
                color=eval(DBColor[1])
            ),
            title=dict(text='Compare over level 2',
                       font=dict(family='Montserrat',
                                 size=22,
                                 color=eval(DBColor[1]))),
            hovermode='closest',
            transition={'duration': 500},
        )
    }

if __name__ == "__main__":
    app.run_server(debug=True) #,config=config
