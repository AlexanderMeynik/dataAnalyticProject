import dash
from dash import dcc, html, Output, Input, callback
import pandas as pd

import plotly.express as px

from dataRequestService import requestor

rq = requestor()
# res = rq.get_pairs_for_one_tag('COVID-19', 10)
second_df_names = ['subjects', 'tag_scores']
#чтобы лишний раз не плодить http запросов
#я решил просто запросить блок данных, который я масштабирую, если число на слайдере
#превосходит, то что у нас имеется
top_tags_data = pd.DataFrame(
    dict(zip(second_df_names, rq.get_top_tags(100)))
)
#массив имён колонок для dataframe, который показывает зависимость распределений числа тегов от числа авторов
first_df_names = ['auth_count', 'subj_count', 'article_count', 'percentages']
#я таким образом просто именую наши колонки в dat frame
authors_subject_count_data = pd.DataFrame(
    dict(zip(first_df_names, rq.get_auth_subj_count_hist(10)))
)


dash.register_page(__name__)

# Define the layout of the app
layout = html.Div([
    dcc.Graph(
        id='top_tag-histogram',
        figure={}
    ),
    html.P("Количество тегов"),
    dcc.Slider(id="tag-count-slider", min=1, value=10, step=1,
               marks={2 ** i: '{}'.format(2 ** i) for i in range(11)},
               tooltip={"placement": "bottom", "always_visible": True}),
    html.Div([
        dcc.Graph(
            id='pie-chart',
            figure={},style={'resize':'horizontal','overflow': 'visible'}
        ),
        dcc.Graph(
            id='tag-histogram',
            figure={},style={'resize':'horizontal','overflow': 'visible'}
        )
    ], style={'display': 'flex','resize':'horizontal','overflow': 'auto'}),
    html.P("Количество авторов у статьи"),
    dcc.Slider(id="my-input", min=1, max=80, value=1, step=1,
               marks={i * 10: '{}'.format(10 * i) for i in range(8)},
               tooltip={"placement": "bottom", "always_visible": True}),
    html.Button(id='my-button', n_clicks=0, children="Show breakdown")
])


@callback(
    Output("pie-chart", "figure"),
    Output("tag-histogram", "figure"),
    Input("my-input", "value"),
    config_prevent_initial_callbacks=False
)
def refresh_graphs(val):
    # res = rq.get_pairs_for_one_tag('COVID-19',val)
    # df2 = pd.DataFrame({'name': res[0], 'count': res[1]})
    sort_values = (authors_subject_count_data[authors_subject_count_data[first_df_names[0]] == val]).sort_values(
        by=first_df_names[1])

    pie_plot = px.pie(sort_values, names=first_df_names[1],
                     values=first_df_names[3], title='Круговая диаграмма распределения статей по количеству '
                                                     'ключевых слов')
    pie_plot.update_layout(legend={'traceorder': 'normal'})
    pie_plot.update()

    bar_plot = px.bar(sort_values,
                     x=first_df_names[1], y=first_df_names[2],
                     labels={first_df_names[1]: 'Количество ключевых слов', first_df_names[2]: 'Количество статей'},
                     title='Гистограмма распределения количества статей по числу ключевых слов',

                     )
    bar_plot.update_layout()
    bar_plot.update()

    return pie_plot, bar_plot


@callback(
    Output("top_tag-histogram", "figure"),
    Input("tag-count-slider", "value"),
    config_prevent_initial_callbacks=False

)
def refresh_top_tags(val):
    # res = rq.get_pairs_for_one_tag('COVID-19',val)
    # df2 = pd.DataFrame({'name': res[0], 'count': res[1]})
    global top_tags_data
    if val > top_tags_data[second_df_names[0]].size:#если

        global rq
        top_tags_data =pd.DataFrame(
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



