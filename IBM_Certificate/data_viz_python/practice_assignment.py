import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
from dash import no_update

#reading data to a pandas dataframe

car_data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DA0101EN-SkillsNetwork/labs/Data%20files/automobileEDA.csv',
                      encoding = "ISO-8859-1")

#creating the dash app
app = dash.Dash()

# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

#build layout
app.layout= html.Div(children=[html.H1('Car Automobile Components',
                                        style={'textAlign': 'center',
                                               'color': '#503D36',
                                               'font-size': 50}),
                                #adding outer division
                                html.Div(
                                    #adding first inner division for dropdown
                                    html.Div([html.H2('Drive Wheels Type:', style={'margin-right': '2em'}),
                                #adding dropdown
                                dcc.Dropdown(id = 'demo-dropdown',
                                             options=[
                                    {'label': 'Front wheel drive', 'value':'fwd'},
                                    {'label': 'Rear wheel drive', 'value':'rwd'},
                                    {'label': 'All wheel drive', 'value':'4wd'}
                                ], value='fwd'),
                                    
                                    #adding second inner division for two graphs
                                    html.Div([
                                        html.Div(dcc.Graph(id='plot1')),
                                        html.Div(dcc.Graph(id='plot2'))
                                    ], style={'display':'flex'})])
                                    
                               
                                )])

#creating the decorator

@app.callback([Output(component_id='plot1', component_property='figure'),
               Output(component_id='plot2', component_property='figure')],
              Input(component_id='demo-dropdown', component_property='value'))
def df_per_drive_wheel(value):
    filtered_df = car_data[car_data['drive-wheels']==value].groupby(['drive-wheels','body-style'], as_index=False).mean()
    filtered_df = filtered_df
    fig1 = px.pie(filtered_df, values='price', names='body-style', title="Pie Chart")
    fig2 = px.bar(filtered_df, x='body-style', y='price', title='Bar Chart')

    return [fig1, fig2]

# Run the application                   
if __name__ == '__main__':
    app.run_server()

