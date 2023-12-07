
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from dataRequestService import requestor
import base64
from io import BytesIO

import dash

import pandas as pd
import plotly.express as px
from dash import dcc, html, Output, Input, callback, dash_table


rq=requestor()

set=rq.get_venn_diagram()[1]

fig = venn3(subsets = set, set_labels = ('scopus_id', 'creators', 'subjects'))

buf = BytesIO()
plt.savefig(buf, format="png")

fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
img_src = f'data:image/png;base64,{fig_data}'



max_words_count_df_cn = ['article_ids', 'word_counts']

max_words_count_df = pd.DataFrame(
    dict(zip(max_words_count_df_cn, rq.get_max_words_count(10)))
)

max_subjects_df_cn = ['article_ids', 'subject_count']

max_subjects_count_df = pd.DataFrame(
    dict(zip(max_subjects_df_cn, rq.get_max_subject(10)))
)

max_creators_df_cn = ['article_ids', 'subject_count']

max_creators_count_df = pd.DataFrame(
    dict(zip(max_creators_df_cn, rq.get_max_creators(10)))
)

max_pages_df_cn = ['article_ids', 'page_counts']

max_pages_count_df = pd.DataFrame(
    dict(zip(max_pages_df_cn, rq.get_max_page_count(10)))
)

count_stats_df_cn = ['stat_name', 'article_count']

count_stats_df = pd.DataFrame(
    dict(zip(count_stats_df_cn, rq.get_count_stats()))
)

status_pie_df_cn = ['status', 'article_count']

status_pie_df = pd.DataFrame(
    dict(zip(status_pie_df_cn, rq.get_status_pie_chart()))
)


dash.register_page(__name__)


layout = html.Div([
    html.H1('Диаграмма жйлера'),
    html.Img(id='bar-graph-matplotlib',src=img_src,title="Диаграмма Эйлера множеств статей по наличию поля"),
    dcc.Graph(figure=px.pie(status_pie_df,names=status_pie_df_cn[0],
                            values=status_pie_df_cn[1],
                            labels={status_pie_df_cn[0]: 'Статус',
                                    status_pie_df_cn[1]: 'Количество статей'},
                            title='Круговая диаграмма распределения статей по статусам')),
    dash_table.DataTable(data=max_subjects_count_df.to_dict('records'),
                                         columns=[{"name": i, "id": i} for i in max_subjects_count_df.columns]),
    dash_table.DataTable(data=max_creators_count_df.to_dict('records'),
                                         columns=[{"name": i, "id": i} for i in max_creators_count_df.columns]),
    dash_table.DataTable(data=max_pages_count_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in max_pages_count_df.columns]),
    dash_table.DataTable(data=max_words_count_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in max_words_count_df.columns]),
    dash_table.DataTable(data=count_stats_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in count_stats_df.columns]),
])