from dash import Dash, dcc, html # type: ignore
import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
from callbacks import register_callbacks # type: ignore

# Charger les données
pub_year = pd.read_csv('data/pub_year.csv')
app_year = pd.read_csv('data/app_year.csv')
fam_year = pd.read_csv('data/fam_year.csv')

df_pub_kind = pd.read_csv('data/df_pub_kind.csv')
df_app_kind = pd.read_csv('data/df_app_kind.csv')
df_Fam_kind = pd.read_csv('data/df_Fam_kind.csv')

df_pub_ctry = pd.read_csv('data/df_pub_ctry.csv')
df_app_ctry = pd.read_csv('data/df_app_ctry.csv')
df_Fam_ctry = pd.read_csv('data/df_Fam_ctry.csv')

df_pub = pd.read_csv('data/df_pub.csv')
df_app = pd.read_csv('data/df_app.csv')
df_Fam = pd.read_csv('data/df_Fam.csv')

authorities=['EP','US','WO']

# Créer l'app Dash
app = Dash(__name__)
app.title = "Crispr patents on agricultural plants"

# Construire les figures avec tes fonctions déjà créées
from functions import plot_documents_interactif, plot_horizontal_stacked_bar, plot_by_country, plot_top_applicants

fig1 = plot_documents_interactif()   # passe les bons DataFrames
fig2 = plot_horizontal_stacked_bar()
fig3 = plot_by_country()
fig4 = plot_top_applicants()

# Définir l'agencement de l'app
app.layout = html.Div([
    html.H1("Cripsr patents on agricultural plants"),
    dcc.Tabs([

        dcc.Tab(label='Infos', children=[
            html.Div([
                html.H2("Codes IPC/CPC"),
                html.H4("A01H New Plants"),
                html.Ul([
                    html.Li("A01H 1/ — Modifying genotypes"),
                    html.Li("A01H 3/ — Modifying phenotypes"),
                    html.Li("A01H 4/ — Reproduction by tissue culture techniques"),
                    html.Li("A01H 5/ — Angiosperms // plant parts"),
                    html.Li("A01H 6/ — Angiosperms // botanic taxonomy"),
                ]),
                html.H4("C12N Mutation or Genetic Engineering"),
                html.Ul([
                    html.Li("C12N 2310/20, C12N9/222, C12N9/224, C12N9/226 — CRISPR patents"),
                ]),
                html.H4("Jurisdictions"),
                html.Ul([
                    html.Li("EP, US, WO"),
                ])
            ], style={"fontSize": "18px", "padding": "20px"})
        ]),

        dcc.Tab(label='Publications per year', children=[
        html.Div([
        html.Div([
            html.Label("Select patent authority:", style={
                'fontSize': '20px',
                'fontWeight': 'bold',
                'marginBottom': '10px',
                'display': 'block',
                'textAlign': 'left'}),
            dcc.Dropdown(
                id='authority-dropdown',
                options=[
                    {'label': 'EP', 'value': 'EP'},
                    {'label': 'US', 'value': 'US'},
                    {'label': 'WO', 'value': 'WO'},
                ],
                value='EP',
                clearable=False,
                style={'width': '100%'}
            ),
        ], style={
            'width': '80%',
            'margin': '0 auto',
            'paddingBottom': '20px'
        }),

        html.Div([
            dcc.Graph(id='graph-documents'),
        ], style={
            'width': '80%',
            'margin': '0 auto'
        })
        ])
        ]),

        dcc.Tab(label='Applicants type', children=[
        html.Div([
        html.Div([
                html.Label("Select document type:", style={
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'marginBottom': '10px',
                    'display': 'block',
                    'textAlign': 'left'
                    }),
            dcc.Dropdown(
                id='kind-dropdown',
                options=[
                    {'label': 'Publication', 'value': 'Publication'},
                    {'label': 'Application', 'value': 'Application'},
                    {'label': 'Family', 'value': 'Family'},
                    ],
                value='Publication',
                clearable=False,
                style={'width': '100%'}
            ),
            ], style={
                'width': '80%',
                'margin': '0 auto',
                'paddingBottom': '20px'
            }),

            html.Div([
            dcc.Graph(id='kind-bar-graph'),
                ], style={
                    'width': '80%',
                    'margin': '0 auto'
                })
            ], style={'padding': '20px'}),
        ]),



        dcc.Tab(label='Applicants nationality', children=[
        html.Div([
        html.Div([
                html.Label("Select document type:", style={
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'marginBottom': '10px',
                    'display': 'block',
                    'textAlign': 'left'
                    }),
            dcc.Dropdown(
                id='kind-dropdown2',
                options=[
                    {'label': 'Publication', 'value': 'Publication'},
                    {'label': 'Application', 'value': 'Application'},
                    {'label': 'Family', 'value': 'Family'},
                    ],
                value='Publication',
                clearable=False,
                style={'width': '100%'}
            ),
            ], style={
                'width': '80%',
                'margin': '0 auto',
                'paddingBottom': '20px'
            }),

        html.Div([   
            dcc.Graph(id='country-fig'),  
                ], style={
                    'width': '80%',
                    'margin': '0 auto'
                })
            ], style={'padding': '20px'}),
        ]),
        
        dcc.Tab(label='Top applicants', children=[
        html.Div([
            html.Div([
            html.Div([
                html.Label("Select document type:", style={
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'marginBottom': '10px',
                    'display': 'block',
                    'textAlign': 'left'
                    }),
                dcc.Dropdown(
                    id='kind-dropdown3',
                    options=[
                        {'label': 'Publication', 'value': 'Publication'},
                        {'label': 'Application', 'value': 'Application'},
                        {'label': 'Family', 'value': 'Family'}
                    ],
                    value='Publication',
                    clearable=False
                )
            ], style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                html.Label("Select jurisdiction:", style={
                    'fontSize': '20px',
                    'fontWeight': 'bold',
                    'marginBottom': '10px',
                    'display': 'block',
                    'textAlign': 'left'
                    }),
                dcc.Dropdown(
                    id='auth-dropdown',
                    options=[
                        {'label': 'EP', 'value': 'EP'},
                        {'label': 'US', 'value': 'US'},
                        {'label': 'WO', 'value': 'WO'}
                    ],
                    value='EP',
                    clearable=False
                )
            ], style={'width': '48%', 'display': 'inline-block', 'marginLeft': '4%'})
        ], style={
                'width': '80%',
                'margin': '0 auto',
                'paddingBottom': '20px'}),

        html.Div([   
            dcc.Graph(id='top-applicants-fig'),  
                ], style={
                    'width': '80%',
                    'margin': '0 auto'
                })
            ], style={'padding': '20px'}), 
        ]), 
    ])
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)