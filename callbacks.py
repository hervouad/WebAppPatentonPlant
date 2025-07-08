from dash import Input, Output
from functions import plot_documents_interactif, plot_horizontal_stacked_bar

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


