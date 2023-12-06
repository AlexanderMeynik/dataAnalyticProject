import dash
from dash import html
from datetime import datetime, date
from dataRequestService import requestor
import pandas as pd
import plotly.express as px
from dash import dcc, html, Output, Input, callback, dash_table

dash.register_page(__name__)

rq = requestor()
journals_for_dyn_df_cn = ['journal_names', 'number_of_months', 'articles_published_in_journal',
                          'articles_per_month']

journals_for_dyn_df = pd.DataFrame(
    dict(zip(journals_for_dyn_df_cn, rq.get_journals_for_dynamics(2)))
)
# rem = 5
# journals_for_dyn_df = journals_for_dyn_df.tail(len(journals_for_dyn_df.index) - rem)
pd.set_option('display.max_columns', None)

journals_dynamics_df_cn = ['journal_names', 'years', 'months',
                           'article_counts']
# я таким образом просто именую наши колонки в dat frame
journals_dynamics_df = pd.DataFrame(
    dict(zip(journals_dynamics_df_cn, rq.get_all_journals_dynamic()))
)

years = journals_dynamics_df[journals_dynamics_df_cn[1]].tolist()
months = journals_dynamics_df[journals_dynamics_df_cn[2]].tolist()
dates = []
for i in range(len(years)):
    if years[i] is None or months[i] is None:
        dates.append(date(year=1600, month=1, day=1))
    else:
        dates.append(date(year=int(years[i]), month=int(months[i]), day=1))
journals_dynamics_df.insert(4, 'dates', dates)

top_tags_all_df_cn = ['journal_names', 'subject', 'tag_counts']
top_tags_all_df = pd.DataFrame(
    dict(zip(top_tags_all_df_cn, rq.get_top_tags_for_all_journals(10)))
)

top_auth_all_df_cn = ['journal_names', 'creator', 'tag_counts']
top_auth_all_df = pd.DataFrame(
    dict(zip(top_auth_all_df_cn, rq.get_top_authors_for_all_journals(10)))
)

top_auth_by_jorn_df_cn = ['creator', 'journal_count']
# я таким образом просто именую наши колонки в dat frame
top_auth_by_jorn_df = pd.DataFrame(
    dict(zip(top_auth_by_jorn_df_cn, rq.get_top_authors_by_journal_num(100)))

)
lst = journals_for_dyn_df[journals_for_dyn_df_cn[0]].tolist();
layout = html.Div([
    dcc.Graph(
            id='author_top_histogram',
            figure={}
        ),
    html.P("Размер топа"),
    dcc.Slider(id="author_top_slider", min=1, value=10, step=1,
               marks={2 ** i: '{}'.format(2 ** i) for i in range(11)},
               tooltip={"placement": "bottom", "always_visible": True}),
    dcc.Dropdown(id='journal_select_dropdown', options=lst, value=lst[0]),

    dcc.Graph(
        id='journal_activity_bubble',
        figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
    ),
    html.Div([
        dcc.Graph(
            id='top_tags_pie',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        ),
        dcc.Graph(
            id='top_creators',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        )
    ], style={'display': 'flex', 'resize': 'horizontal', 'overflow': 'auto, margin: 0 auto'}),
])


@callback(
    Output('author_top_histogram', 'figure'),
    Input('author_top_slider', 'value'),

)
def updateGraph(val):
    global top_auth_by_jorn_df
    if (val > len(top_auth_by_jorn_df.index)):
        top_auth_by_jorn_df = pd.DataFrame(
            dict(zip(top_auth_by_jorn_df_cn, rq.get_top_authors_by_journal_num(val * 2)))
        )
    data = top_auth_by_jorn_df.head(val);

    figure = px.bar(data,
                    x=top_auth_by_jorn_df_cn[0], y=top_auth_by_jorn_df_cn[1],
                    labels={top_auth_by_jorn_df_cn[0]: 'Автор', top_auth_by_jorn_df_cn[1]: 'Количество журналов'},
                    title='Топ авторов по числу журналов, где они публиковались',

                    )
    figure.update_layout()
    figure.update()

    return figure


@callback(
    Output('journal_activity_bubble', 'figure'),
    Output('top_tags_pie', 'figure'),
    Output('top_creators', 'figure'),
    Input('journal_select_dropdown', 'value'),

)
def updateGraphs(val):
    data = journals_dynamics_df.loc[journals_dynamics_df[journals_dynamics_df_cn[0]] == val]

    '''figure = px.scatter(data,
                     x=journals_dynamics_df_cn[1],
                     y=journals_dynamics_df_cn[2],
                        size=journals_dynamics_df_cn[3],
                     labels={journals_dynamics_df_cn[1]: 'Год', journals_dynamics_df_cn[2]: 'Месяц'},
                     #title=f'Круговая диаграмма самых популярных парных ключевых<br>слов для ключевого слова {selected_main_tag}'
                     )'''

    figure = px.line(data,
                     x='dates',
                     y=journals_dynamics_df_cn[3],
                     labels={'dates': 'Дата', journals_dynamics_df_cn[3]: 'Число статей'},
                     title=f'Динамика публикаций в журнале {val}'
                     )

    figure.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        title_font=dict(size=14),
        title_x=0.5
    )

    data2 = top_tags_all_df.loc[top_tags_all_df[top_tags_all_df_cn[0]] == val]
    figure1 = px.pie(data2,
                     names=top_tags_all_df_cn[1],
                     values=top_tags_all_df_cn[2],
                     labels={top_tags_all_df_cn[1]: 'Ключевое слово', top_tags_all_df_cn[2]: 'Число статей'},
                     title=f'Круговая диаграмма самых популярных ключевых<br>слов для статей из журнала {val}'
                     )

    figure1.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        title_font=dict(size=14),
        title_x=0.5
    )

    data3 = top_auth_all_df.loc[top_auth_all_df[top_auth_all_df_cn[0]] == val]

    figure2 = px.pie(data3,
                     names=top_auth_all_df_cn[1],
                     values=top_auth_all_df_cn[2],
                     labels={top_auth_all_df_cn[1]: 'Автор', top_auth_all_df_cn[2]: 'Число статей'},
                     title=f'Круговая диаграмма самых часто публикующихся<br>авторов для статей из журнала {val}'
                     )

    figure2.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        title_font=dict(size=14),
        title_x=0.5
    )

    return figure, figure1, figure2
