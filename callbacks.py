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
    Input('kind-dropdown2', 'value'),
    Input('china-toggle', 'value'),
    )
    def update_figure(kind, chi):
        return plot_by_country(kind, chi)
    
    @app.callback(
    Output('top-applicants-fig', 'figure'),
    Input('kind-dropdown3', 'value'),
    Input('auth-dropdown', 'value'),
    Input('top-dropdown', 'value')
    )
    def update_top_applicants_fig(kind, auth, top):
        return plot_top_applicants(kind, auth, top)


