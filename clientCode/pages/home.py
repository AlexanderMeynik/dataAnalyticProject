import dash
from dash import html

dash.register_page(__name__, path='/')

layout = html.Div([
    html.H1('Это базовая страница'),
    html.Div('Здесь ничего не будет'),
])