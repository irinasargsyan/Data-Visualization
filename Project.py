import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
from datetime import datetime as dt
import plotly.graph_objs as go
import pandas as pd
import plotly.express as px
from plotly.subplots import make_subplots


app = dash.Dash(__name__)

df = pd.read_csv(r"C:\Users\HP\Desktop\IrinaSargsyanHW\Data Visualization\Project\athlete_events.csv")

def f(row):
    if row['Medal'] == 'Gold':
        val = 1
    elif row['Medal'] == 'Silver':
        val = 1
    elif row['Medal'] == 'Bronze':
        val = 1
    else:
        val = 0
    return val

df['Medalist'] = df.apply(f, axis = 1)
df2 = df.groupby('NOC')['Medalist'].sum()
df2 = df2.to_frame()
df2 = df2.nlargest(30, ['Medalist'])
df2['Country'] = df2.index

data = go.Choropleth(
    locations = df2['Country'],
    locationmode = 'ISO-3',
    z = df2['Medalist'],
    marker = go.choropleth.Marker(
        line = go.choropleth.marker.Line(
            color = 'rgb(240,255,240)',
            width = 1.5
        )
    ),
    colorbar = go.choropleth.ColorBar(
        title = 'Number of medals per country',
        bgcolor = 'rgb(238,195,109)'
    )
)

layout = go.Layout(
    geo = go.layout.Geo(
        scope = 'world',
        showlakes = True,
        lakecolor = 'rgb(240,255,240)'
    )
)

figure_1 = go.Figure(data = data, layout = layout)
figure_1.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="#203647",)


df1 = df[df["Season"] == "Summer"]
df2 = df[df["Season"] == "Winter"]
label1 = df1['Sex'].value_counts().index
values1 = df1['Sex'].value_counts().values
label2 = df2['Sex'].value_counts().index
values2 = df2['Sex'].value_counts().values

fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]])
fig.add_trace(go.Pie(labels=label1, values=values1, name="Summer"),
              1, 1)
fig.add_trace(go.Pie(labels=label2, values=values2, name="Winter"),
              1, 2)

fig.update_traces(hole=0.7, hoverinfo="label+percent+name")

fig.update_layout(
    annotations=[dict(text='Summer', x=0.18, y=0.5, font_size=20, showarrow=False),
                 dict(text='Winter', x=0.82, y=0.5, font_size=20, showarrow=False)])



available_indicators = df['Sport'].unique()
available_indicators2 = df['NOC'].unique()



colors = {
    'background': 'rgb(238,195,109)',
    'text': '#202020'
}


app.layout = html.Div(style={'backgroundColor': colors['background']}, children=[
    html.H1(
        children='Olympic Games',
        style={
            'textAlign': 'center',
            'color': colors['text']
        }
    ),

    dcc.Graph(
    id="my-graph",
    figure = figure_1),
    
    html.Img(src='/assets/317285.jpg'),
    
    html.Div([
        
     html.P("Values:"),
    dcc.Dropdown(
        id = 'values', 
        value = 'Age', 
        options=[{'value': x, 'label': x} 
                 for x in ["Age", "Height", "Weight"]]),
        
        dcc.Graph(id = "donut-chart"),
        ]),
    
    dcc.Graph(
    id="my-graph3",
    figure = fig),
    
       html.Div([
        
     html.P("Sport"),
    dcc.Dropdown(
        id = 'sport', 
        value = 'Figure Skating', 
        options=[{'value': x, 'label': x} 
                 for x in available_indicators]),
        
    html.Table([
        html.Tr([html.Td(['Country']), html.Td(id = 'winner')]),
        ]),
           html.Img(src='/assets/olympics-logo.jpg')
       ])

])

@app.callback(
    Output("donut-chart", "figure"), 
    [Input("values", "value")])
def generate_chart(values):
    fig = px.histogram(df, x = values)
    fig.update_layout(
    margin=dict(l=20, r=20, t=20, b=20),
    paper_bgcolor="#203647")
    return fig

@app.callback(
    Output('winner', 'children'), 
    [Input("sport", "value")])
def callback_a(sport):    
    df1 = df[df['Sport'] == sport]
    df1 = df1.groupby('NOC')["Medalist"].sum()
    df1 = df1.nlargest(30)
    return df1.index[0]


if __name__ == '__main__':
    app.run_server(debug = True)
 











    

    
    
    