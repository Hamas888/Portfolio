# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input,Output,State
import plotly.express as px
from dash.exceptions import PreventUpdate

# Read the airline data into pandas dataframe
df =  pd.read_csv('airline_data.csv')
df=df[['Year','Month','CancellationCode','Reporting_Airline','OriginState','DestState','AirTime','Flights',
       'CarrierDelay', 'WeatherDelay', 'NASDelay', 'SecurityDelay', 'LateAircraftDelay','DivAirportLandings']]
#print(list(df.columns))

app=dash.Dash(__name__,
              meta_tags=[{'name': 'viewpoint',
                          'content': 'width=device-width,initial-scale=1.0'}]  # for mobiles
              )
# REVIEW1: Clear the layout and do not display exception till callback gets executed
app.config.suppress_callback_exceptions = True

app.layout=html.Div(children=[
    html.H1('Airline Flight Statistics',style={'backgroundColor':'#FCE205','textAlign':'center','color':'black','font-size':30}),
    html.Div([
        html.Div([
            html.Div(html.H1('Report Type: ',style={'color':'white','font-size':20})),
            html.Div(dcc.Dropdown(id='dp-1',placeholder='Select a report type',options=[{'label':'Yearly airline performance report','value':'op1'},
                                                                                     {'label':'Yearly average flight delay statistics','value':'op2'}],
                                  style={'width':600}),style={'marginLeft':35})
        ],style={'display':'flex'}),
    html.Br(),
    html.Div([
            html.Div(html.H1('Choose Year: ',style={'color':'white','font-size':20})),
            html.Div(dcc.Dropdown(id='dp-2',placeholder='Select a year',options=[{'label':x,'value':x}
                                                                               for x in range(2005,2021)],style={'width':600}),style={'marginLeft':35})
        ],style={'display':'flex'})
    ],style={'marginLeft':200}),
    html.Div([],id='plot1'),
    html.Div([
        html.Div([],id='plot2'),
        html.Div([],id='plot3'),
    ],style={'display':'flex'}),
    html.Div([
        html.Div([], id='plot4'),
        html.Div([], id='plot5'),
    ],style={'display':'flex'})
],style={'background-color':'black'})

@app.callback(
    [Output('plot1','children'),
     Output('plot2','children'),
     Output('plot3','children'),
     Output('plot4','children'),
     Output('plot5','children')],
    [Input('dp-1','value'),
     Input('dp-2','value')],
    # REVIEW4: Holding output state till user enters all the form information. In this case, it will be chart type and year
    [State("plot1", 'children'), State("plot2", "children"),
     State("plot3", "children"), State("plot4", "children"),
     State("plot5", "children")
     ]
)
def Show(op,val,c1,c2,c3,c4,c5):
    if op=='op1':
        dff = df[df['Year'] == val]
        #plot1
        db = dff.groupby(['Month','CancellationCode'])['Flights'].sum().reset_index()
        fb=px.bar(db,x='Month', y='Flights', color='CancellationCode', title='Monthly Flight Cancellation')
        # plot2
        dl = dff.groupby(['Month', 'Reporting_Airline'])['AirTime'].mean().reset_index()
        fl = px.line(dl,x='Month', y='AirTime', color='Reporting_Airline', title='Average monthly flight time (minutes) by airline')
        # plot3
        dp = dff[dff['DivAirportLandings' ]!= 0.0]
        fp = px.pie(dp,values='Flights', names='Reporting_Airline', title='% of flights by reporting airline')
        # plot4
        dc = dff.groupby(['OriginState'])['Flights'].sum().reset_index()
        fc = px.choropleth(dc,
                           locations='OriginState',
                           color='Flights',
                           hover_data=['OriginState', 'Flights'],
                           locationmode='USA-states',  # Set to plot as US States
                           color_continuous_scale='redor',
                           range_color=[0, dc['Flights'].max()]
                           )
        fc.update_layout(
            title_text='Number of flights from origin state',
            geo_scope='usa')
        # plot5
        dt = dff.groupby(['DestState', 'Reporting_Airline'])['Flights'].sum().reset_index()
        ft = px.treemap(dt,
                    path=['DestState','Reporting_Airline'],
                    values='Flights',
                    color='Flights',
                    color_continuous_scale='redor',
                    title='Flight count by airline to destination state')
        return [dcc.Graph(figure=fb),
                    dcc.Graph(figure=fl),
                    dcc.Graph(figure=fp),
                    dcc.Graph(figure=fc),
                    dcc.Graph(figure=ft)
                   ]
    elif op == 'op2':
        dff = df[df['Year'] == val]
        #plot1
        ac = dff.groupby(['Month', 'Reporting_Airline'])['CarrierDelay'].mean().reset_index()
        cf = px.line(ac, x='Month', y='CarrierDelay', color='Reporting_Airline',title='Average carrier delay time (minutes) by airline')
        # plot2
        aw = dff.groupby(['Month', 'Reporting_Airline'])['WeatherDelay'].mean().reset_index()
        wf = px.line(aw, x='Month', y='WeatherDelay', color='Reporting_Airline',title='Average weather delay time (minutes) by airline')
        # plot3
        an = dff.groupby(['Month', 'Reporting_Airline'])['NASDelay'].mean().reset_index()
        nf = px.line(an, x='Month', y='NASDelay', color='Reporting_Airline',title='Average NAS delay time (minutes) by airline')
        # plot4
        ase = dff.groupby(['Month', 'Reporting_Airline'])['SecurityDelay'].mean().reset_index()
        sf = px.line(ase, x='Month', y='SecurityDelay', color='Reporting_Airline',title='Average security delay time (minutes) by airline')
        # plot5
        al = dff.groupby(['Month', 'Reporting_Airline'])['LateAircraftDelay'].mean().reset_index()
        lf = px.line(al, x='Month', y='LateAircraftDelay', color='Reporting_Airline',title='Average late delay time (minutes) by airline')
        return [dcc.Graph(figure=cf),
                dcc.Graph(figure=wf),
                dcc.Graph(figure=nf),
                dcc.Graph(figure=sf),
                dcc.Graph(figure=lf)]
    else:
        raise PreventUpdate


if __name__=='__main__':
    app.run()