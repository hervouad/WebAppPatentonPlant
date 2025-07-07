from dash import Dash, dcc, html
import pandas as pd
import plotly.graph_objects as go
import numpy as np

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
# ... charger toutes les autres nécessaires

# Créer l'app Dash
app = Dash(__name__)
app.title = "Dashboard Brevets"

# Construire les figures avec tes fonctions déjà créées
from functions import plot_documents_interactif, plot_horizontal_stacked_bar, plot_by_country_with_labels, plot_top_applicants_colored

fig1 = plot_documents_interactif(pub_year, app_year, fam_year)   # passe les bons DataFrames
fig2 = plot_horizontal_stacked_bar(df_pub_kind, df_app_kind, df_Fam_kind)
fig3 = plot_by_country_with_labels(df_pub_ctry, df_app_ctry, df_Fam_ctry, top_n=10)
fig4 = plot_top_applicants_colored(df_pub, df_app, df_Fam)

# Définir l'agencement de l'app
app.layout = html.Div([
    html.H1("Dashboard des brevets"),
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
                html.H4("C12N ... Mutation or Genetic Engineering"),
                html.Ul([
                    html.Li("C12N 2310/20, C12N9/222, C12N9/224, C12N9/226 — CRISPR"),
                ]),
                html.H4("Jurisdictions"),
                html.Ul([
                    html.Li("EP, US, WO"),
                ])
            ], style={"fontSize": "18px", "padding": "20px"})
        ]),
        dcc.Tab(label='Publications par an', children=[dcc.Graph(figure=fig1)]),
        dcc.Tab(label='Répartition par type', children=[dcc.Graph(figure=fig2)]),
        dcc.Tab(label='Origine des pays', children=[dcc.Graph(figure=fig3)]),
        dcc.Tab(label='Top applicants', children=[dcc.Graph(figure=fig4)]),
        
    ])
])