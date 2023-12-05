import dash
from dash import dcc, html, Output, Input, callback
import pandas as pd

import plotly.express as px

from dataRequestService import requestor

rq = requestor()

second_df_names = ['subjects', 'tag_scores']
top_tags_data = pd.DataFrame(
    dict(zip(second_df_names, rq.get_top_tags(100)))
)

auth_count_hist_df_cn = ['auth_count', 'articles_count']
auth_count_hist_df = pd.DataFrame(
    dict(zip(auth_count_hist_df_cn, rq.get_auth_hist()))
)

word_count_hist_df_cn = ['word_count', 'articles_count']
word_count_hist_df = pd.DataFrame(
    dict(zip(word_count_hist_df_cn, rq.get_hist()))
)

size_correlation_df_col_names = ['auth_count', 'subj_count', 'article_count', 'percentages']

size_correlation_df = pd.DataFrame(
    dict(zip(size_correlation_df_col_names, rq.get_auth_subj_count_hist(10)))
)

dash.register_page(__name__)

# Define the layout of the app
layout = html.Div([

    html.Div([
        dcc.Graph(
            id='author_count_histogram',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        ),
        dcc.Graph(
            id='word_count_histogram',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        )
    ], style={'display': 'flex', 'resize': 'horizontal', 'overflow': 'auto'}),


    html.Div([
        dcc.Graph(
            id='pie-chart',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        ),
        dcc.Graph(
            id='tag-histogram',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        )
    ], style={'display': 'flex', 'resize': 'horizontal', 'overflow': 'auto'}),
    html.P("Количество авторов у статьи"),
    dcc.Slider(id="my-input", min=1, max=80, value=1, step=1,
               marks={i * 10: '{}'.format(10 * i) for i in range(8)},
               tooltip={"placement": "bottom", "always_visible": True}),
])


@callback(
    Output("pie-chart", "figure"),
    Output("tag-histogram", "figure"),
    Input("my-input", "value"),
)
def refresh_graphs(val):
    sort_values = size_correlation_df.loc[size_correlation_df[size_correlation_df_col_names[0]] == val]

    pie_plot = px.pie(sort_values, names=size_correlation_df_col_names[1],
                      values=size_correlation_df_col_names[3],
                      labels={size_correlation_df_col_names[1]: 'Число ключевых слов',
                              size_correlation_df_col_names[3]: 'Количество статей'},
                      title='Круговая диаграмма распределения статей по количеству '
                            'ключевых слов')
    pie_plot.update()

    bar_plot = px.bar(sort_values,
                      x=size_correlation_df_col_names[1], y=size_correlation_df_col_names[2],
                      labels={size_correlation_df_col_names[1]: 'Количество ключевых слов',
                              size_correlation_df_col_names[2]: 'Процент статей'},
                      title='Гистограмма распределения количества статей по числу ключевых слов',

                      )
    bar_plot.update_layout()
    bar_plot.update()

    return pie_plot, bar_plot


@callback(
    Output("author_count_histogram", "figure"),
    Output("word_count_histogram", "figure"),
    Input("my-input", "value"),
)
def refresh_graphs(val):
    auth_bar = px.bar(auth_count_hist_df,
                      x=auth_count_hist_df_cn[0], y=auth_count_hist_df_cn[1],
                      labels={auth_count_hist_df_cn[0]: 'Число авторов статьи',
                              auth_count_hist_df_cn[1]: 'Количество статей'},
                      title='Гистограмма распределения количества статей по числу ключевых авторов',
                      )
    auth_bar.update_xaxes(range=[1, 30])
    auth_bar.update_layout()
    auth_bar.update()


    word_in_tittle_bar = px.bar(word_count_hist_df,
                                x=word_count_hist_df_cn[0], y=word_count_hist_df_cn[1],
                                labels={word_count_hist_df_cn[0]: 'Число слов заголовке статьи',
                                        word_count_hist_df_cn[1]: 'Количество статей'},
                                title='Гистограмма распределения количества статей по числу слов в заголовке',
                                )
    word_in_tittle_bar.update_layout()
    word_in_tittle_bar.update()
    word_in_tittle_bar.update_xaxes(range=[1, 30])

    return auth_bar, word_in_tittle_bar


