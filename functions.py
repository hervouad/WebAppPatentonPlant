import pandas as pd # type: ignore
import plotly.graph_objects as go # type: ignore
import numpy as np # type: ignore
import os

# Chargement des données
df_pub = pd.read_csv(os.path.join("data", "df_pub.csv"))
df_app = pd.read_csv(os.path.join("data", "df_app.csv"))
df_Fam = pd.read_csv(os.path.join("data", "df_Fam.csv"))

df_pub_kind = pd.read_csv(os.path.join("data", "df_pub_kind.csv"))
df_app_kind = pd.read_csv(os.path.join("data", "df_app_kind.csv"))
df_Fam_kind = pd.read_csv(os.path.join("data", "df_Fam_kind.csv"))

df_pub_ctry = pd.read_csv(os.path.join("data", "df_pub_ctry.csv"))
df_app_ctry = pd.read_csv(os.path.join("data", "df_app_ctry.csv"))
df_Fam_ctry = pd.read_csv(os.path.join("data", "df_Fam_ctry.csv"))

pub_year = pd.read_csv(os.path.join('data/pub_year.csv'))
app_year = pd.read_csv(os.path.join('data/app_year.csv'))
fam_year = pd.read_csv(os.path.join('data/fam_year.csv'))


def plot_documents_interactif():
    global pub_year, app_year, fam_year
    # Création d’un dictionnaire pour stocker les traces par autorité
    authorities = ['EP', 'US', 'WO']
    all_traces = []
    buttons = []

    for i, authority in enumerate(authorities):
        # Filtrage par autorité
        pub_filtered = pub_year[pub_year['Auth'] == authority]
        app_filtered = app_year[app_year['Auth'] == authority]
        fam_filtered = fam_year[fam_year['Auth'] == authority]

        # Création des séries
        pub_counts = pub_filtered.set_index('Year')['Count']
        app_counts = app_filtered.set_index('Year')['Count']
        fam_counts = fam_filtered.set_index('Year')['Count']

        # Fusionner dans un DataFrame unique
        df_merged = pd.DataFrame({
            'Publication': pub_counts,
            'Application': app_counts,
            'Family': fam_counts
        }).fillna(0).astype(int).sort_index()

        # Création des trois barres (Publication, Application, Family)
        traces = [
            go.Bar(name='Publication', x=df_merged.index, y=df_merged['Publication'], visible=(i==0)),
            go.Bar(name='Application', x=df_merged.index, y=df_merged['Application'], visible=(i==0)),
            go.Bar(name='Family', x=df_merged.index, y=df_merged['Family'], visible=(i==0)),
        ]
        all_traces.extend(traces)

        # Création d’un bouton pour afficher ces 3 traces uniquement
        visibility = [False] * (3 * len(authorities))
        visibility[i*3:(i+1)*3] = [True, True, True]

        buttons.append(dict(
            label=authority,
            method='update',
            args=[
                {'visible': visibility},
                {'title': f"Nombre de documents par an pour l'autorité : {authority}"}
            ]
        ))

    # Construction de la figure
    fig = go.Figure(data=all_traces)

    fig.update_layout(
        updatemenus=[dict(
            active=0,
            buttons=buttons,
            x=0.5,
            xanchor='center',
            y=1.15,
            yanchor='top'
        )],
        barmode='group',
        height=600,  # plus lisible
        template='plotly_white',
        xaxis_title='Année',
        yaxis_title='Nombre de documents',
        title="Nombre de documents par an pour l'autorité : EP"
    )
    fig.show()

def plot_horizontal_stacked_bar():
    global df_pub_kind, df_app_kind, df_Fam_kind

    # Fonction de préparation des données pour chaque type
    def prepare_data(df, kind_col='Kind'):
        df_grouped = df.groupby(['Auth', kind_col])['Count'].sum().reset_index()
        df_pivot = df_grouped.pivot(index='Auth', columns=kind_col, values='Count').fillna(0)
        for col in ['F', 'U', 'I']:
            if col not in df_pivot.columns:
                df_pivot[col] = 0
        df_pivot = df_pivot[['F', 'U', 'I']].reindex(['EP', 'US', 'WO'])
        return df_pivot

    # Préparation des 3 datasets
    data_pub = prepare_data(df_pub_kind)
    data_app = prepare_data(df_app_kind)
    data_fam = prepare_data(df_Fam_kind)

    # Fonction pour créer les barres pour un dataset donné
    def make_traces(data, visible=True):
        return [
            go.Bar(
                name='Firms',
                y=data.index,
                x=data['F'],
                orientation='h',
                marker_color='steelblue',
                visible=visible
            ),
            go.Bar(
                name='Universities',
                y=data.index,
                x=data['U'],
                orientation='h',
                marker_color='darkorange',
                visible=visible
            ),
            go.Bar(
                name='Individuals',
                y=data.index,
                x=data['I'],
                orientation='h',
                marker_color='seagreen',
                visible=visible
            ),
        ]

    # Créer les 9 traces (3 pour chaque type)
    traces = (
        make_traces(data_pub, visible=True) +
        make_traces(data_app, visible=False) +
        make_traces(data_fam, visible=False)
    )

    # Boutons pour afficher un seul groupe de 3 barres à la fois
    buttons = []
    for i, label in enumerate(['Publications', 'Applications', 'Families']):
        visibility = [False] * 9
        visibility[i*3:(i+1)*3] = [True, True, True]
        buttons.append(dict(
            label=label,
            method='update',
            args=[
                {'visible': visibility},
                {'title': f"Nombre de documents par système (type : {label})"}
            ]
        ))

    # Layout
    fig = go.Figure(data=traces)
    fig.update_layout(
        barmode='stack',
        template='plotly_white',
        title="Nombre de documents par système (type : Publications)",
        xaxis_title="Nombre de documents",
        yaxis_title="Système",
        height=600,  # plus lisible
        updatemenus=[dict(
            buttons=buttons,
            direction='down',
            x=0.5,
            xanchor='center',
            y=1.2,
            yanchor='top',
            active=0
        )],
        legend=dict(title='Type de déposant', orientation='h', yanchor='bottom', y=1.02, xanchor='right', x=1)
    )

    fig.show()

def plot_by_country_with_labels():
    global df_pub_ctry, df_app_ctry, df_Fam_ctry
    top_n=10

    data_dict = {
        'Publication': df_pub_ctry,
        'Application': df_app_ctry,
        'Family': df_Fam_ctry
    }

    doc_types = ['Publication', 'Application', 'Family']
    authorities = ['EP', 'US', 'WO']
    all_traces = []
    buttons = []

    for i, doc_type in enumerate(doc_types):
        df = data_dict[doc_type]

        # Calcule les top pays
        top_countries = df.groupby('Country')['Count'].sum().nlargest(top_n).index
        df['Country'] = df['Country'].apply(lambda x: x if x in top_countries else 'Autres')

        # Regroupe par autorité et pays
        grouped = df.groupby(['Auth', 'Country'])['Count'].sum().reset_index()
        pivot_df = grouped.pivot(index='Auth', columns='Country', values='Count').fillna(0)
        pivot_df = pivot_df.reindex(authorities)  # Assure l’ordre EP, US, WO

        # Ajout des traces
        for j, country in enumerate(pivot_df.columns):
            trace = go.Bar(
                name=country,
                y=pivot_df.index,
                x=pivot_df[country],
                orientation='h',
                visible=(i == 0),
                text=[country] * len(pivot_df),  # Affiche le code pays
                textposition='inside',
                insidetextanchor='start',
                hovertemplate='%{x} documents – %{text} (%{y})<extra></extra>'
            )
            all_traces.append(trace)

        # Gestion de la visibilité
        n_countries = len(pivot_df.columns)
        visibility = [False] * (n_countries * len(doc_types))
        visibility[i * n_countries:(i + 1) * n_countries] = [True] * n_countries

        buttons.append(dict(
            label=doc_type,
            method='update',
            args=[
                {'visible': visibility},
                {'title': f'Nombre de {doc_type.lower()}s par pays d’origine et système'}
            ]
        ))

    # Création de la figure
    fig = go.Figure(data=all_traces)
    fig.update_layout(
        barmode='stack',
        template='plotly_white',
        xaxis_title='Nombre de documents',
        yaxis_title='Système de dépôt',
        title='Nombre de publications par pays d’origine et système',
        height=600,  # plus lisible
        updatemenus=[dict(
            buttons=buttons,
            direction="right",
            pad={"r": 10, "t": 10},
            showactive=True,
            x=0.5,
            xanchor="center",
            y=1.15,
            yanchor="top"
        )],
        legend=dict(
            title="Pays d’origine",
            orientation="v",
            yanchor="top",
            y=1,
            xanchor="left",
            x=1.02
        )
    )

    fig.show()


def plot_top_applicants_colored():
    global df_pub, df_app, df_Fam
    top_n=20

    data_dict = {
        'Publication': df_pub,
        'Application': df_app,
        'Family': df_Fam
    }

    doc_types = ['Publication', 'Application', 'Family']
    authorities = ['EP', 'US', 'WO']
    kind_colors = {'F': '#1f77b4', 'U': '#2ca02c', 'I': '#d62728'}  # Firms, Universities, Individuals

    all_traces = []
    trace_labels = []

    for doc_type in doc_types:
        df = data_dict[doc_type].copy()
        df_grouped = df.groupby(['Auth', 'Applicant', 'Kind'])['Count'].sum().reset_index()

        for authority in authorities:
            df_auth = df_grouped[df_grouped['Auth'] == authority]
            total_counts = df_auth.groupby('Applicant')['Count'].sum()
            top_applicants = total_counts.nlargest(top_n).index

            df_top = df_auth[df_auth['Applicant'].isin(top_applicants)]

            # Déterminer le Kind dominant par applicant
            kind_map = (
                df_top.groupby('Applicant')['Kind']
                .agg(lambda x: x.mode().iloc[0] if not x.mode().empty else 'F')
            )

            # Récupérer les valeurs triées
            counts = df_top.groupby('Applicant')['Count'].sum().loc[top_applicants]
            kinds = kind_map.loc[top_applicants]
            colors = [kind_colors.get(k, 'gray') for k in kinds]

            # Tri décroissant : les plus gros en haut
            sorted_applicants = counts.sort_values(ascending=False).index
            sorted_counts = counts.loc[sorted_applicants]
            sorted_kinds = kinds.loc[sorted_applicants]
            sorted_colors = [kind_colors.get(k, 'gray') for k in sorted_kinds]

            trace = go.Bar(
                x=sorted_counts.values,
                y=sorted_applicants,
                name=f"{doc_type} – {authority}",
                orientation='h',
                visible=False,
                text=sorted_kinds.values,
                marker_color=sorted_colors,
                textposition='auto',
                hovertemplate='<b>%{y}</b><br>Kind: %{text}<br>Documents: %{x}<extra></extra>'
            )

            all_traces.append(trace)
            trace_labels.append((doc_type, authority))

    # Rendre la première trace visible
    all_traces[0].visible = True

    # Boutons pour changer de type de document
    buttons_doc = []
    for doc_type in doc_types:
        visibility = [False] * len(all_traces)
        for j, (dtype, auth) in enumerate(trace_labels):
            if dtype == doc_type and auth == 'EP':
                visibility[j] = True
        buttons_doc.append(dict(
            label=doc_type,
            method='update',
            args=[
                {'visible': visibility},
                {'title': f"Top {top_n} déposants – {doc_type} – EP"}
            ]
        ))

    # Boutons pour changer de juridiction
    buttons_sys = []
    for authority in authorities:
        visibility = [False] * len(all_traces)
        for j, (dtype, auth) in enumerate(trace_labels):
            if dtype == 'Publication' and auth == authority:
                visibility[j] = True
        buttons_sys.append(dict(
            label=authority,
            method='update',
            args=[
                {'visible': visibility},
                {'title': f"Top {top_n} déposants – Publication – {authority}"}
            ]
        ))

    fig = go.Figure(data=all_traces)

    fig.update_layout(
        updatemenus=[
            dict(
                buttons=buttons_doc,
                direction='right',
                showactive=True,
                x=0.3,
                xanchor='center',
                y=1.15,
                yanchor='top'
            ),
            dict(
                buttons=buttons_sys,
                direction='right',
                showactive=True,
                x=0.7,
                xanchor='center',
                y=1.15,
                yanchor='top'
            )
        ],
        template='plotly_white',
        title=f"Top {top_n} déposants – Publication – EP",
        xaxis_title='Nombre de documents',
        yaxis_title='Déposants',
        height=600  # plus lisible
    )

    fig.show()