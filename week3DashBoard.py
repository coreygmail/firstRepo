# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

app.layout = html.Div(children=[
    dcc.Dropdown(id="dropdown",
    options=[
        {'label': 'All Sites', 'value': 'ALL'},
        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
    ],
    value='ALL',
    placeholder='ALL',
    searchable=True
    ),
    dcc.Graph(id='mygraph'),

    dcc.RangeSlider(id='RangeSlider',
    min=0,max=10000,step=1000,
    marks={0:"0",2500:"2500",5000:"5000",7500:"7500",10000:"10000"},
    value=[0,10000]),

    dcc.Graph(id="scatterplot")
])

@app.callback(
    Output(component_id='mygraph', component_property='figure'),
    Input(component_id='dropdown', component_property='value')
)

def makechart(selectedLaunchSite):
    if selectedLaunchSite=='ALL':
        groupedData = spacex_df.groupby('Launch Site')['class'].sum().reset_index()
        fig=px.pie(groupedData["class"],values="class",
        names=groupedData["Launch Site"])
    else:
        filtered=spacex_df[spacex_df["Launch Site"]==selectedLaunchSite]
        dfLength=filtered.shape[0]
        sumOfYes=filtered["class"].sum()
        sumOfNo=dfLength-sumOfYes
        finalOutput=pd.DataFrame(data={'names':["success","failure"],'output':[sumOfYes,sumOfNo]})
        fig=px.pie(finalOutput["output"],values="output",
        names=finalOutput["names"])
    return fig


@app.callback(
    Output(component_id='scatterplot', component_property='figure'),
    [Input(component_id='dropdown', component_property='value'),
    Input(component_id='RangeSlider',component_property='value')]
)


def makeScatter(selectedLaunchSite,minmax):
    spacex_df.astype({'class':'character'})
    if selectedLaunchSite=='ALL':
        filter1=spacex_df[spacex_df["Payload Mass (kg)"]>minmax[0]]
        filter2=filter1[filter1["Payload Mass (kg)"]<minmax[1]]
        fig=px.scatter(filter2,x="Payload Mass (kg)",y="class",
        color='class')
    else:
        filter1=spacex_df[spacex_df["Payload Mass (kg)"]>minmax[0]]
        filter2=filter1[filter1["Payload Mass (kg)"]<minmax[1]]
        filtered=filter2[filter2["Launch Site"]==selectedLaunchSite]
        fig=px.scatter(filtered,x="Payload Mass (kg)",y="class",
        color='class')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server()
