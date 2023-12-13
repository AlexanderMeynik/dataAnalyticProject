
import matplotlib.pyplot as plt
from matplotlib_venn import venn3
from dataRequestService import requestor
import base64
from io import BytesIO

import dash

import pandas as pd
import plotly.express as px
from dash import dcc, html, Output, Input, callback, dash_table

rq = requestor()

set = rq.get_venn_diagram()[1]

fig = venn3(subsets=set, set_labels=('scopus_id', 'creators', 'subjects'))

buf = BytesIO()
plt.savefig(buf, format="png")

fig_data = base64.b64encode(buf.getbuffer()).decode("ascii")
img_src = f'data:image/png;base64,{fig_data}'

max_words_count_df_cn = ['Pii индекс статьи', 'Число слов в заголовке']

max_words_count_df = pd.DataFrame(
    dict(zip(max_words_count_df_cn, rq.get_max_words_count(10)))
)

max_subjects_df_cn = ['Pii индекс статьи', 'Число ключевых слов']

max_subjects_count_df = pd.DataFrame(
    dict(zip(max_subjects_df_cn, rq.get_max_subject(10)))
)

max_creators_df_cn = ['Pii индекс статьи', 'Число авторов']

max_creators_count_df = pd.DataFrame(
    dict(zip(max_creators_df_cn, rq.get_max_creators(10)))
)

max_pages_df_cn = ['Pii индекс статьи', 'Число страниц']

max_pages_count_df = pd.DataFrame(
    dict(zip(max_pages_df_cn, rq.get_max_page_count(10)))
)

count_stats_df_cn = ['Параметр', 'Число']

count_stats_df = pd.DataFrame(
    dict(zip(count_stats_df_cn, rq.get_count_stats()))
)

status_pie_df_cn = ['status', 'article_count']

status_pie_df = pd.DataFrame(
    dict(zip(status_pie_df_cn, rq.get_status_pie_chart()))
)


dash.register_page(__name__)


layout = html.Div([
    html.H1('Диаграмма Эйлера'),
    html.Img(id='bar-graph-matplotlib', src=img_src, title="Диаграмма Эйлера множеств статей по наличию поля"),
    dcc.Graph(figure=px.pie(status_pie_df, names=status_pie_df_cn[0],
                            values=status_pie_df_cn[1],
                            labels={status_pie_df_cn[0]: 'Статус',
                                    status_pie_df_cn[1]: 'Количество статей'},
                            title='Круговая диаграмма распределения статей по статусам')),
    dash_table.DataTable(data=max_subjects_count_df.to_dict('records'),
                                         columns=[{"name": i, "id": i} for i in max_subjects_count_df.columns],
                         style_table={
                             'overflowX': 'auto',
                             'width': '95%',
                             'margin': '20px auto',
                             'border-spacing': '50%',
                             'border': '1px solid #ddd',
                             'boxShadow': '0px 0px 15px 0px rgba(0,0,0,0.1)',
                             'backgroundColor': '#88BDBC',
                         },
                         style_cell={
                             'padding': '10px',
                             'border': '1px solid #ddd',
                             'width': '50%',
                         },
                         style_header={
                             'backgroundColor': 'white',
                             'fontWeight': 'bold',
                             'fontSize': '18px',
                         },
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': c},
                                 'textAlign': 'left',
                                 'border': '2px solid #ddd',
                             } for c in ['your_column_ids_here']
                         ],
                         style_header_conditional=[
                             {'if': {'column_id': 'your_column_id_here'}, 'textAlign': 'center'},
                         ],
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 0},
                                 'backgroundColor': '#254E58',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                         ],
                         ),
    dash_table.DataTable(data=max_creators_count_df.to_dict('records'),
                                         columns=[{"name": i, "id": i} for i in max_creators_count_df.columns],
                         style_table={
                             'overflowX': 'auto',
                             'width': '95%',
                             'margin': '20px auto',
                             'border-spacing': '50%',
                             'border': '1px solid #ddd',
                             'boxShadow': '0px 0px 15px 0px rgba(0,0,0,0.1)',
                             'backgroundColor': '#88BDBC',
                         },
                         style_cell={
                             'padding': '10px',
                             'border': '1px solid #ddd',
                             'width': '50%',
                         },
                         style_header={
                             'backgroundColor': 'white',
                             'fontWeight': 'bold',
                             'fontSize': '18px',
                         },
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': c},
                                 'textAlign': 'left',
                                 'border': '2px solid #ddd',
                             } for c in ['your_column_ids_here']
                         ],
                         style_header_conditional=[
                             {'if': {'column_id': 'your_column_id_here'}, 'textAlign': 'center'},
                         ],
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 0},
                                 'backgroundColor': '#254E58',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                         ],
                         ),
    dash_table.DataTable(data=max_pages_count_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in max_pages_count_df.columns],
                         style_table={
                             'overflowX': 'auto',
                             'width': '95%',
                             'margin': '20px auto',
                             'border-spacing': '50%',
                             'border': '1px solid #ddd',
                             'boxShadow': '0px 0px 15px 0px rgba(0,0,0,0.1)',
                             'backgroundColor': '#88BDBC',
                         },
                         style_cell={
                             'padding': '10px',
                             'border': '1px solid #ddd',
                             'width': '50%',
                         },
                         style_header={
                             'backgroundColor': 'white',
                             'fontWeight': 'bold',
                             'fontSize': '18px',
                         },
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': c},
                                 'textAlign': 'left',
                                 'border': '2px solid #ddd',
                             } for c in ['your_column_ids_here']
                         ],
                         style_header_conditional=[
                             {'if': {'column_id': 'your_column_id_here'}, 'textAlign': 'center'},
                         ],
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 0},
                                 'backgroundColor': '#254E58',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                         ],
                         ),
    dash_table.DataTable(data=max_words_count_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in max_words_count_df.columns],
                         style_table={
                             'overflowX': 'auto',
                             'width': '95%',
                             'margin': '20px auto',
                             'border-spacing': '50%',
                             'border': '1px solid #ddd',
                             'boxShadow': '0px 0px 15px 0px rgba(0,0,0,0.1)',
                             'backgroundColor': '#88BDBC',
                         },
                         style_cell={
                             'padding': '10px',
                             'border': '1px solid #ddd',
                             'width': '50%',
                         },
                         style_header={
                             'backgroundColor': 'white',
                             'fontWeight': 'bold',
                             'fontSize': '18px',
                         },
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': c},
                                 'textAlign': 'left',
                                 'border': '2px solid #ddd',
                             } for c in ['your_column_ids_here']
                         ],
                         style_header_conditional=[
                             {'if': {'column_id': 'your_column_id_here'}, 'textAlign': 'center'},
                         ],
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 0},
                                 'backgroundColor': '#254E58',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                         ],
                         ),
    dash_table.DataTable(data=count_stats_df.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in count_stats_df.columns],
                         style_table={
                             'overflowX': 'auto',
                             'width': '95%',
                             'margin': '20px auto',
                             'border-spacing': '50%',
                             'border': '1px solid #ddd',
                             'boxShadow': '0px 0px 15px 0px rgba(0,0,0,0.1)',
                             'backgroundColor': '#88BDBC',
                         },
                         style_cell={
                             'padding': '10px',
                             'border': '1px solid #ddd',
                             'width': '50%',
                         },
                         style_header={
                             'backgroundColor': 'white',
                             'fontWeight': 'bold',
                             'fontSize': '18px',
                         },
                         style_cell_conditional=[
                             {
                                 'if': {'column_id': c},
                                 'textAlign': 'left',
                                 'border': '2px solid #ddd',
                             } for c in ['your_column_ids_here']
                         ],
                         style_header_conditional=[
                             {'if': {'column_id': 'your_column_id_here'}, 'textAlign': 'center'},
                         ],
                         style_data_conditional=[
                             {
                                 'if': {'row_index': 0},
                                 'backgroundColor': '#254E58',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'odd'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                             {
                                 'if': {'row_index': 'even'},
                                 'backgroundColor': '#88BDBC',
                                 'color': 'white'
                             },
                         ],
                         ),
])
