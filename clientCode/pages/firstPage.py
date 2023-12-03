import dash
from dash import dcc, html, Output, Input, callback
import pandas as pd

import plotly.express as px

from dataRequestService import requestor

rq = requestor()

first_df_names = ['main_tag', 'subject', 'percentage']
paired_tags_data = pd.DataFrame(
    dict(zip(first_df_names, rq.get_top_paired_tags_f_top_tags(100, 10)))
)

# res = rq.get_pairs_for_one_tag('COVID-19', 10)
second_df_names = ['subjects', 'tag_scores']
# чтобы лишний раз не плодить http запросов
# я решил просто запросить блок данных, который я масштабирую, если число на слайдере
# превосходит, то что у нас имеется
top_tags_data = pd.DataFrame(
    dict(zip(second_df_names, rq.get_top_tags(100)))
)
# массив имён колонок для dataframe, который показывает зависимость распределений числа тегов от числа авторов


dash.register_page(__name__)

# Define the layout of the app
layout = html.Div([
    dcc.Graph(
        id='top_tag-histogram2',
        figure={}
    ),
    html.P("Количество тегов"),
    dcc.Slider(id="tag-count-slider2", min=1, value=10, step=1,
               marks={2 ** i: '{}'.format(2 ** i) for i in range(11)},
               tooltip={"placement": "bottom", "always_visible": True}),
    html.Div(id='graphs-div', children=[], style={'display': 'flex', 'overflowY': 'auto'}),
    # html.Div(id='graphs-div', children=[], style={'display': 'flex', 'resize': 'horizontal', 'overflow': 'auto'}),
    html.P("Количество авторов у статьи"),
    dcc.Slider(id="my-input2", min=1, max=20, value=10, step=1,
               tooltip={"placement": "bottom", "always_visible": True}),
])


@callback(
    Output("graphs-div", "children"),
    Input("my-input2", "value"),
    config_prevent_initial_callbacks=False
)
def refresh_graphs2(val):
    global paired_tags_data

    global top_tags_data
    if val > paired_tags_data[first_df_names[0]].size:  # если

        global rq
        paired_tags_data = pd.DataFrame(
            dict(zip(first_df_names, rq.get_top_paired_tags_f_top_tags(val * 2, 10)))
        )

    # sort_values = paired_tags_data.head(val)
    df2 = paired_tags_data[first_df_names[0]].unique().tolist()[0:val]

    output = []

    output.append(html.P(f"Header in div {val},size {len(df2)}"));
    for elem in df2:
        figure = px.pie(paired_tags_data[paired_tags_data[first_df_names[0]] == elem],
                        names=first_df_names[1],
                        values=first_df_names[2],
                        title=f'Круговая диаграмма распределения пар ключевых слов<br>для ключевого слова {elem}',
                        )

        figure.update_layout(
            font_family="Courier New",
            font_color="blue",
            title_font_family="Times New Roman",
            legend_title_font_color="green",
            title_font=dict(size=14),
            title_x=0.5
        )
        pie_chart = dcc.Graph(
            id=f"pie-chart-{elem}",  # Provide a unique ID for each graph
            figure=figure  # Use the figure attribute of the Figure object
        )

        output.append(html.Div(pie_chart,style={'margin': '10px'}))

        #output.append(pie_chart)
    output.append(html.P(f"Header ,size {len(output)}"))
    return output


@callback(
    Output("top_tag-histogram2", "figure"),
    Input("tag-count-slider2", "value"),
    config_prevent_initial_callbacks=False
)
def refresh_top_tags2(val):
    # res = rq.get_pairs_for_one_tag('COVID-19',val)
    # df2 = pd.DataFrame({'name': res[0], 'count': res[1]})
    global top_tags_data
    if val > top_tags_data[second_df_names[0]].size:  # если

        global rq
        top_tags_data = pd.DataFrame(
            dict(zip(second_df_names, rq.get_top_tags(val * 2)))
        )
    sort_values = top_tags_data.head(val)

    figure2 = px.bar(sort_values,
                     x=second_df_names[0], y=second_df_names[1],
                     labels={second_df_names[0]: 'Ключевое слово', second_df_names[1]: 'Количество статей'},
                     title='Гистограмма распределения количества статей по числу ключевых слов',

                     )
    figure2.update_layout()
    figure2.update()

    return figure2

# we select some basik property to update
# then we choose inputs(can be many)
# ve can pass changed data
# to change output we must return sth
