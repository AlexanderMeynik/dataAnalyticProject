import dash
from dash import Dash, html, dcc
from dataRequestService import requestor

app = Dash(__name__, use_pages=True)

external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css']

header_style = {
    'background-color': '#88BDBC',
    'color': 'white',
    'padding': '20px',
    'text-align': 'center'
}

button_container_style = {
    'display': 'flex',
    'flex-wrap': 'wrap',
    'justify-content': 'center',  # Центрирование кнопок
    'margin-top': '20px',  # Отступ от заголовка
    'margin-bottom': '20px',
}

button_style = {
    'margin-right': '20px',
    'margin-bottom': '10px',
    'padding': '10px',
    'border': '2px solid #254E58',
    'border-radius': '8px',
    'text-decoration': 'none',
    'font-size': '16px',
    'cursor': 'pointer',
    'background-color': '#254E58',
    'color': 'white',
    'margin-bottom': '20px',
}

page_names = ['Главная', 'Первая страница', 'Вторая страница', 'Третья страница', 'Четвертая страница']
app.layout = html.Div([
    html.Div(html.H1('Дэшборд аналитики данных с платформы scienceDirect'), style=header_style),
    html.Div(style=button_container_style, children=[
        html.Div(
            dcc.Link(
                f"{page_names[i]}", href=page["relative_path"],
                style=button_style
            )
        ) for i, page in enumerate(dash.page_registry.values())
    ]),
    dash.page_container
])

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', debug=True, port=8050)
