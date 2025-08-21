from dash import Dash, html, dcc, Input, Output, callback
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

app = Dash(title='FPL Predictor', external_stylesheets=[dbc.themes.BOOTSTRAP])

# dataset
df = pd.read_csv('data/final.csv')

# main variable
season = '2023'
method_att_mid = 'points'
method_def = 'points'
method_gk = 'points'

app.layout = html.Div([
    # font link
    html.Link(
        href='https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap',
        rel='stylesheet'
    ),
    # title
    html.H1(
        'Fantasy Premier League Predictor',
        style={
            'font-family': '"Inter", sans-serif',
            'text-align': 'center',
            'font-size': '60px',
            'font-weight': '700',
            'margin-bottom': '50px',
            'margin-top': '50px'
        }
    ),
    # season selection items
    html.Div(
        dbc.RadioItems(
            id='season-selection',
            className="btn-group",
            inputClassName="btn-check",
            labelClassName="btn btn-outline-primary",
            labelCheckedClassName="active",
            options=[
                {'label': '2023', 'value': '2023'},
                {'label': '2024', 'value': '2024'},
                {'label': '2025', 'value': '2025'}
            ],
            value=season,
        ),
        style={'text-align': 'center'}
    ),
    dbc.Row(
        [
            # midfielders & attackers graph 
            dbc.Col(
                style={'margin-top': '20px',
                       'margin-bottom': '20px', 'margin-left': '40px'},
                children=[
                    dcc.Graph(
                        id='top_scorers-alltime',
                        figure={}
                    ),
                    html.Div(
                        dbc.RadioItems(
                            id='att-mid-selection',
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {'label': 'points', 'value': 'points',
                                    'color': 'black'},
                                {'label': 'performance', 'value': 'Performance'},
                                {'label': 'goals', 'value': 'goals-scored'},
                            ],
                            value=method_att_mid,
                        ),
                        style={'text-align': 'center',
                               'margin-top': '5px'}
                    ),
                ]
            ),
            # defenders graph 
            dbc.Col(
                style={'margin-top': '20px',
                       'margin-bottom': '20px', 'margin-left': '300px'},
                children=[
                    dcc.Graph(
                        id='top_defenders',
                        figure={}
                    ),
                    html.Div(
                        dbc.RadioItems(
                            id='def-selection',
                            className="btn-group",
                            inputClassName="btn-check",
                            labelClassName="btn btn-outline-primary",
                            labelCheckedClassName="active",
                            options=[
                                {'label': 'points', 'value': 'points'},
                                {'label': 'performance', 'value': 'Performance'},
                                {'label': 'clean sheets', 'value': 'clean-sheets'}
                            ],
                            value=method_def,
                        ),
                        style={'text-align': 'center'}
                    ),
                ]
            )
        ]
    ),

    # goalkeepers graph
    dbc.Row([
        html.Div(
            style={'display': 'flex', 'flex-direction': 'column', 'justify-content': 'center', 'align-items': 'center'},
            children=[
                dbc.Col(
                    style={'margin-top': '50px',
                           'margin-bottom': '20px'},
                    children=[
                        dcc.Graph(
                            id='top_goalies',
                            figure={}
                        ),
                        html.Div(
                            dbc.RadioItems(
                                id='gk-selection',
                                className="btn-group",
                                inputClassName="btn-check",
                                labelClassName="btn btn-outline-primary",
                                labelCheckedClassName="active",
                                options=[
                                    {'label': 'points', 'value': 'points'},
                                    {'label': 'performance',
                                        'value': 'Performance'},
                                    {'label': 'clean sheets',
                                        'value': 'clean-sheets'},
                                    {'label': 'penalties saved',
                                     'value': 'penalties-saved'},
                                ],
                                value=method_gk,
                            ),
                            style={'text-align': 'left',
                                   'margin-left': '150px'}
                        )]
                )]
        )
    ])

])

@callback(
    Output('top_scorers-alltime', 'figure'),
    Input('season-selection', 'value'),
    Input('att-mid-selection', 'value')
)
def update_fig(seas, meth):
    global season
    global method_att_mid
    season = seas if seas != None else season
    method_att_mid = meth if meth != None else method_att_mid
    top_scorers = df[(df.season_year.astype('str') == season) & (df.role.isin(['Midfielder', 'Forward']))].sort_values(
        method_att_mid, ascending=False).head(10)
    fig = px.bar(top_scorers,
                 x=top_scorers[method_att_mid],
                 y=top_scorers.name.map(lambda x: x.split()[
                                        0] + ' ' + x.split()[-1]),
                 width=800, height=600,
                 labels={method_att_mid: method_att_mid,
                         'y': 'Players', 'name': 'Players'},
                 title=f'Top Attackers & Midfielders in {season}')
    return fig


@callback(
    Output('top_defenders', 'figure'),
    Input('season-selection', 'value'),
    Input('def-selection', 'value')
)
def update_fig(seas, meth):
    global season
    global method_def
    season = seas if seas != None else season
    method_def = meth if meth != None else method_def
    top_defenders = df[(df.role == 'Defender') & (df.season_year.astype(
        'str') == season)].sort_values(method_def, ascending=False).head(10)
    fig = px.bar(top_defenders,
                 x=top_defenders[method_def],
                 y=top_defenders.name.map(
                     lambda x: x.split()[0] + ' ' + x.split()[-1]),
                 width=800, height=600,
                 labels={method_def: method_def,
                         'y': 'Players', 'name': 'Players'},
                 title=f'Top Defenders in {season}')
    return fig


@callback(
    Output('top_goalies', 'figure'),
    Input('season-selection', 'value'),
    Input('gk-selection', 'value')
)
def update_fig(seas, meth):
    global season
    global method_gk
    season = seas if seas != None else season
    method_gk = meth if meth != None else method_gk
    top_goalies = df[(df.role == 'Goalkeeper') & (df.season_year.astype(
        'str') == season)].sort_values(method_gk, ascending=False).head(10)

    fig = px.bar(top_goalies,
                 x=top_goalies[method_gk],
                 y=top_goalies.name.map(
                     lambda x: x.split()[0] + ' ' + x.split()[-1]),
                 width=800, height=600,
                 labels={method_gk: method_gk,
                         'y': 'Players', 'name': 'Players'},
                 title=f'Top Goalkeepers in {season}')
    return fig


if __name__ == '__main__':
    app.run(debug=False)
