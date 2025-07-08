from dash import Input, Output # type: ignore
from functions import plot_documents_interactif, plot_horizontal_stacked_bar, plot_by_country, plot_top_applicants

def register_callbacks(app):
    @app.callback(
        Output('graph-documents', 'figure'),
        Input('authority-dropdown', 'value')
    )
    def update_graph(authority):
        return plot_documents_interactif(authority)
    
    @app.callback(
    Output('kind-bar-graph', 'figure'),
    Input('kind-dropdown', 'value')
    )
    def update_kind_bar_graph(kind):
        return plot_horizontal_stacked_bar(kind)
    
    @app.callback(
    Output('country-fig', 'figure'),
    Input('kind-dropdown2', 'value')
    )
    def update_figure(kind):
        return plot_by_country(kind)
    
    @app.callback(
    Output('top-applicants-fig', 'figure'),
    Input('kind-dropdown3', 'value'),
    Input('auth-dropdown', 'value')
    )
    def update_top_applicants_fig(kind, auth):
        return plot_top_applicants(kind, auth)


