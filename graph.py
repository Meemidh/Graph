import os
import dash
import dash_html_components as html
import dash_core_components as dcc
import pandas as pd
# import dash_daq as daq
from dash.dependencies import Input, Output
import plotly.express as px
from datetime import datetime as dt

pd.options.mode.chained_assignment = None  



data = pd.read_csv('result_sentiment.csv',encoding='utf-8-sig') 

data['datetime'] = pd.to_datetime(data['datetime']).dt.floor('H')

date_time_range = pd.date_range(start="2021-08-17", end="2021-08-19" , freq="60min" )

df = pd.DataFrame(data=date_time_range,columns=['datetime'])
df['negative'] = 0
df['neutral'] = 0
df['positive'] = 0

for i in range(len(df)):
    df['negative'][i] = len(data[(data['result']==-1) & (data['datetime'] == df['datetime'][i])])
    df['neutral'][i]  = len(data[(data['result']==0) & (data['datetime']  == df['datetime'][i])])
    df['positive'][i] = len(data[(data['result']==1) & (data['datetime']  == df['datetime'][i])])



# col_options = [dict(label=x, value=x) for x in df.columns]
# dimensions = ["x", "y", "sentiment", "facet_col", "facet_row"]


app = dash.Dash(__name__)

server = app.server

app.layout = html.Div([
    html.H1("Demo: Plotly Express in Dash with Tips Dataset"),
    
    dcc.DatePickerRange(
        id='my-date-picker-range',
        min_date_allowed = dt(2021, 8, 1),
        max_date_allowed = dt(2022, 12, 31),
        start_date = dt(2021, 8, 1),
        end_date = dt(2021, 10, 1),
        start_date_placeholder_text ='DD/MM/YYYY'
    ),
    html.H2("  "),
    
    dcc.Graph(id="graph", style={"width": "95%" ,"display": "inline-block"})
    
])


@app.callback(Output("graph", "figure"),   
              [Input("my-date-picker-range","start_date"),
                Input("my-date-picker-range","end_date")]
              )

def make_figure(start_date,end_date):
    
    date_time_range = pd.date_range(start= start_date , end= end_date , freq="60min")
     
    df = pd.DataFrame(data=date_time_range,columns=['datetime'])
    df['negative'] = 0
    df['neutral'] = 0
    df['positive'] = 0

    for i in range(len(df)):
        df['negative'][i] = len(data[(data['result']==-1) & (data['datetime'] == df['datetime'][i])])
        df['neutral'][i]  = len(data[(data['result']==0) & (data['datetime']  == df['datetime'][i])])
        df['positive'][i] = len(data[(data['result']==1) & (data['datetime']  == df['datetime'][i])])
    
    
    return px.line( 
        df,
        x='datetime',
        y=['negative','neutral','positive'],
        labels={
                     "datetime": "Day ,time(hr) ",
                     "value": "Count",
                     "variable" : "Sentiment"
                                      
                 },
        
        color_discrete_map={
                 "negative": "red",
                 "neutral": "green",
                 "positive": "blue"
             },
            
        height=700,
    )

app.run_server(debug=True)