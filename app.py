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
app = Dash(__name__,
           meta_tags=[{'name':'viewport',
                       'content': 'with=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'}])
app.title = "Crispr patents on agricultural plants"

# Construire les figures avec tes fonctions déjà créées
from functions import plot_documents_interactif, plot_horizontal_stacked_bar, plot_by_country, plot_top_applicants

fig1 = plot_documents_interactif()   # passe les bons DataFrames
fig2 = plot_horizontal_stacked_bar()
fig3 = plot_by_country()
fig4 = plot_top_applicants()

# Définir l'agencement de l'app
app.layout = html.Div([
    html.H1("Cripsr patents on agricultural plants",
        style={
            'textAlign': 'center',
            'fontSize': '32px',
            'marginBottom': '30px'
            }
        ),

    dcc.Tabs(children=[

        dcc.Tab(
        label='Information',
        children=[
        html.Div(
            [
                 html.Div([
                        html.P([
                            "This Dash web application provides interactive visualizations of patent data related to the use of CRISPR technologies in agricultural plants. ",
                            "The aim is to offer insights into application trends and distributions of CRISPR-related patents in plant biotechnology."
                        ],
                        style={'fontSize': '20px', 'margin': '0'})
                    ],
                    style={
                        'border': '2px solid #ccc',
                        'borderRadius': '12px',
                        'backgroundColor': '#f9f9f9',
                        'padding': '20px',
                        'marginBottom': '30px',
                        'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)',
                        'width': '80%',
                        'marginLeft': 'auto',
                        'marginRight': 'auto'
                    }),

                html.Div([
                    html.H2("Data source & availability", style={'marginBottom': '20px'}),


                    html.P([
                        "The raw data originate from PatStat Online. ",
                        "They were extracted using a specific SQL query available in a public GitHub repository. ",
                        ],
                        style={'fontSize': '20px', 'marginBottom': '30px'}),

                    html.P([
                        "All transformed data used for generating the visualizations are also available for download at the same location."
                        ],
                        style={'fontSize': '20px', 'marginBottom': '30px'})
                ]),
                html.Div([
                    html.A("🔗 View the GitHub repository",
                    href="https://github.com/hervouad/WebAppPatentonPlant",
                    target="_blank",
                    style={'fontSize': '20px', 'float': 'right', 'margin': '10px 30px'})
                ]),

                html.Div([
                    html.H2("Codes IPC / CPC", style={'marginBottom': '10px'}),
                    html.H4("A01H — New Plants (in agriculture)"),
                    html.P([
                        "At least one of the following codes must be present in the patent application: ",
                        ],
                        style={'fontSize': '20px', 'marginBottom': '30px'}),
                    html.Ul([
                        html.Li("A01H 1/ — Modifying genotypes"),
                        html.Li("A01H 3/ — Modifying phenotypes"),
                        html.Li("A01H 4/ — Reproduction by tissue culture techniques"),
                        html.Li("A01H 5/ — Angiosperms // plant parts"),
                        html.Li("A01H 6/ — Angiosperms // botanic taxonomy"),
                    ], style={'fontSize': '20px','width': '95%', 'margin': '0 auto'}),
                    html.H4("C12N — Mutation or Genetic Engineering", style={'marginTop': '20px'}),
                    html.P([
                        "And at least one of the following codes must be present in the patent application: ",
                        ],
                        style={'fontSize': '20px', 'marginBottom': '30px'}),
                    html.Ul([
                        html.Li("C12N 2310/20, C12N9/222, C12N9/224, C12N9/226 — CRISPR patents"),
                    ], style={'fontSize': '20px','width': '95%', 'margin': '0 auto'}),
                ]),
                html.Div([
                    html.H2("Jurisdictions", style={'marginTop': '30px'}),
                    html.H4("From PatStat:"),
                    html.Ul([
                        html.Li("EP: 210 publications, 126 applications, 116 families"),
                        html.Li("US: 283 publications, 178 applications, 58 families"),
                        html.Li("WO: 223 publications, 196 applications, 184 families"),
                        html.Li("716 publications total"),
                    ], style={'fontSize': '20px','width': '95%', 'margin': '0 auto'}),
                ]),
            ],
            style={"fontSize": "20px", "padding": "30px","width": "80%", "margin": "0 auto"}
        )
        ],
        style={'fontSize': '22px'},
        selected_style={'fontSize': '22px', 'fontWeight': 'bold'}
        ),

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
            }),

        html.Div([
            html.P([
                html.Strong("Comments: "),
                html.Br(),
                "Publications and applications for the US jurisdiction depend heavily on one patent family (from the University of California)."
                ]),
            html.P("Dates differ by document type: publication date for publications, application date for applications, and first filing date for families."),
            html.P("There are fewer applications and families in the most recent years because they are not yet published."),
            ],
            style={
                'border': '2px solid #ccc',
                'borderRadius': '12px',
                'backgroundColor': '#f9f9f9',
                'padding': '20px',
                'marginBottom': '30px',
                'marginTop': '20px',
                'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)',
                'width': '80%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'fontSize': '20px',
                'lineHeight': '1.6'
            })

        ], style={'padding': '20px'})

        ],
        style={'fontSize': '22px'},  # Style normal
        selected_style={'fontSize': '22px', 'fontWeight': 'bold'}),

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
                }),
            
            html.Div([
            html.P([
                html.Strong("Comments: "),
                html.Br(),
                "Nonprofit org. include universities, governemental agencies, and some private nonprofit research institutions."
                ]),
            html.P("If a single patent application lists multiple applicants, the patent count is divided equally among them."),
            html.P("For example, the University of California shares a patent with Emmanuelle Charpentier. In the U.S., this single patent appears in 143 publications. It is therefore considered that each applicant holds 71.5 patent publications."),
            ],
            style={
                'border': '2px solid #ccc',
                'borderRadius': '12px',
                'backgroundColor': '#f9f9f9',
                'padding': '20px',
                'marginBottom': '30px',
                'marginTop': '20px',
                'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)',
                'width': '80%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'fontSize': '20px',
                'lineHeight': '1.6'
            })


            ], style={'padding': '20px'}),
        ],
        style={'fontSize': '22px'},  # Style normal
        selected_style={'fontSize': '22px', 'fontWeight': 'bold'}),

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
                }),

        html.Div([
            html.P([
                html.Strong("Comments: "),
                html.Br(),
                "Nationality is indicated only for legal entities; \"I\" stands for individuals."
                ]),
            html.P("Nationality reflects the current status, not the status at the time of application."),
            html.P("For example, Monsanto applications are now considered German, even though they were originally filed under the U.S. company."),
            ],
            style={
                'border': '2px solid #ccc',
                'borderRadius': '12px',
                'backgroundColor': '#f9f9f9',
                'padding': '20px',
                'marginBottom': '30px',
                'marginTop': '20px',
                'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)',
                'width': '80%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'fontSize': '20px',
                'lineHeight': '1.6'
            })
            ], style={'padding': '20px'}),
        ],
        style={'fontSize': '22px'},  # Style normal
        selected_style={'fontSize': '22px', 'fontWeight': 'bold'}),
        
        dcc.Tab(label='Top 20 applicants', children=[
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
                }),

        html.Div([
            html.P([
                html.Strong("Comments: "),
                html.Br(),
                "Applicant names have been updated to reflect the current situation, similar to how nationalities were handled."
                ]),
            html.P("For example, Monsanto applications are now considered Bayer applications."),
            ],
            style={
                'border': '2px solid #ccc',
                'borderRadius': '12px',
                'backgroundColor': '#f9f9f9',
                'padding': '20px',
                'marginBottom': '30px',
                'marginTop': '20px',
                'boxShadow': '2px 2px 8px rgba(0, 0, 0, 0.1)',
                'width': '80%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'fontSize': '20px',
                'lineHeight': '1.6'
            })

            ], style={'padding': '20px'}), 
        ],
        style={'fontSize': '22px'},  # Style normal
        selected_style={'fontSize': '22px', 'fontWeight': 'bold'}), 

    ],
    parent_style={
        'marginBottom': '30px',
        'border': '1px solid lightgrey',
        'borderRadius': '5px'
    },
    colors={
        'border': 'lightgrey',
        'primary': '#2a3f5f',  # Couleur active
        'background': '#f9f9f9'
    },
    )
])

register_callbacks(app)

if __name__ == '__main__':
    app.run(debug=True, port=8050)