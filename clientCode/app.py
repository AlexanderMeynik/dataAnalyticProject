import dash
from dash import Dash, html, dcc
from dataRequestService import requestor

app = Dash(__name__, use_pages=True)

app.layout = html.Div([
    html.H1('Дэшбsорд аналитики данных с платформы scienceDirect'),
    html.Div([
        html.Div(
            dcc.Link(
                f"{page['name']} - {page['path']}", href=page["relative_path"])
        ) for page in dash.page_registry.values()
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug = True, port = 8050)