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

def plot_documents_interactif(authority='EP'):
    global pub_year, app_year, fam_year

    # Filtrage par autorité
    pub_filtered = pub_year[pub_year['Auth'] == authority]
    app_filtered = app_year[app_year['Auth'] == authority]
    fam_filtered = fam_year[fam_year['Auth'] == authority]

    # Création des séries
    pub_counts = pub_filtered.set_index('Year')['Count']
    app_counts = app_filtered.set_index('Year')['Count']
    fam_counts = fam_filtered.set_index('Year')['Count']

    # Fusion dans un DataFrame unique
    df_merged = pd.DataFrame({
        'Publication': pub_counts,
        'Application': app_counts,
        'Family': fam_counts
    }).fillna(0).astype(int).sort_index()

    # Couleurs personnalisées pour les barres
    colors = ['#636EFA', '#00CC96', '#EF553B']

    traces = [
        go.Bar(name='Publication', x=df_merged.index, y=df_merged['Publication'], marker_color=colors[0]),
        go.Bar(name='Application', x=df_merged.index, y=df_merged['Application'], marker_color=colors[1]),
        go.Bar(name='Family', x=df_merged.index, y=df_merged['Family'], marker_color=colors[2]),
    ]

    # Création de la figure
    fig = go.Figure(data=traces)

    # Mise à jour de la mise en page
    fig.update_layout(
        barmode='group',
        height=600,
        template='plotly_white',
        title={
            'text': f"Number of documents per year ({authority})",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color='#222', family='Arial')
        },
        xaxis=dict(
            title=dict(
                text="Year",
                font=dict(size=18),
                ),
            tickmode='linear',
            ticks='outside',
            showgrid=False,
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            title=dict(
                text="Number of documents",
                font=dict(size=18),
                ),
            ticks='outside',
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        legend=dict(
            title='Document kind',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=60, r=30, t=80, b=60)
    )

    return fig


def plot_horizontal_stacked_bar(kind='Publication'):
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

    # Sélection des données selon le type
    if kind == 'Publication':
        data = prepare_data(df_pub_kind)
    elif kind == 'Application':
        data = prepare_data(df_app_kind)
    elif kind == 'Family':
        data = prepare_data(df_Fam_kind)
    else:
        raise ValueError("Invalid kind")

    # Création des traces
    traces = [
        go.Bar(name='Firms', y=data.index, x=data['F'], orientation='h', marker_color='steelblue'),
        go.Bar(name='Universities', y=data.index, x=data['U'], orientation='h', marker_color='darkorange'),
        go.Bar(name='Individuals', y=data.index, x=data['I'], orientation='h', marker_color='seagreen'),
    ]

    # Création de la figure
    fig = go.Figure(data=traces)

    fig.update_layout(
        barmode='stack',
        template='plotly_white',

        title={
            'text': f"Number of documents by jurisdiction (kind: {kind})",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color='#222', family='Arial')
        },
        xaxis=dict(
            title=dict(
                text="Number of documents",
                font=dict(size=18),
                ),
            #tickmode='linear',
            #ticks='outside',
            showgrid=False,
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            #title='Jurisdiction',
            title=dict(
                text="Jurisdiction",
                font=dict(size=18),
                ),
            ticks='outside',
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        legend=dict(
            title='Applicant type',
            orientation='h',
            yanchor='bottom',
            y=1.02,
            xanchor='center',
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=60, r=30, t=80, b=60)
    )

    return fig

def plot_by_country(kind='Publication'):
    global df_pub_ctry, df_app_ctry, df_Fam_ctry
    top_n = 10

    data_dict = {
        'Publication': df_pub_ctry,
        'Application': df_app_ctry,
        'Family': df_Fam_ctry
    }

    df = data_dict[kind]
    authorities = ['EP', 'US', 'WO']

    # Calcule les top pays
    top_countries = df.groupby('Country')['Count'].sum().nlargest(top_n).index
    df['Country'] = df['Country'].apply(lambda x: x if x in top_countries else 'Autres')

    # Regroupe par autorité et pays
    grouped = df.groupby(['Auth', 'Country'])['Count'].sum().reset_index()
    pivot_df = grouped.pivot(index='Auth', columns='Country', values='Count').fillna(0)
    pivot_df = pivot_df.reindex(authorities)

    # Création des barres
    traces = []
    for country in pivot_df.columns:
        traces.append(go.Bar(
            name=country,
            y=pivot_df.index,
            x=pivot_df[country],
            orientation='h',
            text=[country] * len(pivot_df),
            textposition='inside',
            insidetextanchor='start',
            hovertemplate='%{x} documents – %{text} (%{y})<extra></extra>'
        ))

    # Création de la figure
    fig = go.Figure(data=traces)

    fig.update_layout(
        barmode='stack',
        template='plotly_white',

        title={
            'text': f"Applicants nationality by jurisdiction (kind: {kind})",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color='#222', family='Arial')
        },
        xaxis=dict(
            title=dict(
                text="Number of documents",
                font=dict(size=18),
                ),
            #tickmode='linear',
            #ticks='outside',
            showgrid=False,
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            #title='Jurisdiction',
            title=dict(
                text="Jurisdiction",
                font=dict(size=18),
                ),
            ticks='outside',
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        legend=dict(
            title='Applicants nationality',
            orientation='h',
            yanchor='top',
            y=-0.2,
            xanchor='center',
            x=0.5,
            font=dict(size=14)
        ),
        margin=dict(l=60, r=30, t=80, b=60)
    )
    return fig



def plot_top_applicants(kind='Publication', auth='EP'):
    global df_pub, df_app, df_Fam
    top_n = 20

    data_dict = {
        'Publication': df_pub,
        'Application': df_app,
        'Family': df_Fam
    }

    kind_colors = {'F': "#4d7896", 'U': "#588658", 'I': "#995959"}  # Firms, Universities, Individuals

    df = data_dict[kind].copy()
    df_grouped = df.groupby(['Auth', 'Applicant', 'Kind'])['Count'].sum().reset_index()

    df_auth = df_grouped[df_grouped['Auth'] == auth]
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
        name=f"{kind} – {auth}",
        orientation='h',
        text=sorted_kinds.values,
        marker_color=sorted_colors,
        textposition='auto',
        hovertemplate='<b>%{y}</b><br>Kind: %{text}<br>Documents: %{x}<extra></extra>'
    )

    fig = go.Figure(data=[trace])

    fig.update_layout(
        #height=600
        template='plotly_white',

        title={
            'text': f"Top {top_n} Applicants (kind: {kind}, jurisdiction: {auth})",
            'x': 0.5,
            'xanchor': 'center',
            'font': dict(size=24, color='#222', family='Arial')
        },
        xaxis=dict(
            title=dict(
                text="Number of documents",
                font=dict(size=18),
                ),
            #tickmode='linear',
            #ticks='outside',
            showgrid=False,
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        yaxis=dict(
            #title='Jurisdiction',
            title=dict(
                text="Applicants",
                font=dict(size=18),
                ),
            ticks='outside',
            tickmode='array',
            tickvals=list(sorted_applicants),
            ticktext=list(sorted_applicants),
            showgrid=True,
            gridcolor='lightgrey',
            linecolor='black',
            mirror=True,
            #title_font=dict(size=18),
            tickfont=dict(size=14)
        ),
        margin=dict(l=60, r=30, t=80, b=60)
    )

    return fig
