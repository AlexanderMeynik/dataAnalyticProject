import calendar
from datetime import datetime, date

import dash
from dash import dash_table
from dash import dcc, html, Output, Input, callback
import pandas as pd

import plotly.express as px

from dataRequestService import requestor
from dateutil.relativedelta import relativedelta

rq = requestor()

paired_tags_df_col_names = ['main_tag', 'subject', 'percentage', 'total_percentage']
paired_tags_data = pd.DataFrame(
    dict(zip(paired_tags_df_col_names, rq.get_top_paired_tags_f_top_tags(1000, 10)))
)
pairs_count=1000;
second_df_names = ['subjects', 'tag_scores']
# чтобы лишний раз не плодить http запросов
# я решил просто запросить блок данных, который я масштабирую, если число на слайдере
# превосходит, то что у нас имеется
top_tags_data = pd.DataFrame(
    dict(zip(second_df_names, rq.get_top_tags(100)))
)

tag_dynamic_df_col_names = ['subject', 'year', 'month', 'tag_count'];

tag_dyn_df = pd.DataFrame(
    dict(zip(tag_dynamic_df_col_names, rq.get_all_tags_dynamics()))  # этот запрос может длиться 20 секунд
    # и займёт примерно 300 мб оперативы, но зато можно без задержек получать динамики для любого тега
    # поидее можно юзануть и запрос get_tag_dynamics т.к. я его несколько оптимизировал
    # но тут стоит подумать
)
# print(df[tag_dynamic_df_col_names])

# массив имён колонок для dataframe, который показывает зависимость распределений числа тегов от числа авторов


monthly_to_tafs_df_cn = ['subject', 'years', 'months', 'tag_scores']
monthly_to_tags_df = pd.DataFrame(
    dict(zip(monthly_to_tafs_df_cn, rq.get_monthly_tags(5)))
)

years = monthly_to_tags_df[monthly_to_tafs_df_cn[1]].tolist()
months = monthly_to_tags_df[monthly_to_tafs_df_cn[2]].tolist()
dates = []
for i in range(len(years)):
    dates.append(date(year=int(years[i]), month=int(months[i]), day=1))
monthly_to_tags_df.insert(4, 'date', dates)

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
    dcc.Dropdown(id='first_dropdown', options=[], value=[]),
    dcc.Checklist(id='checkList', options=[{'label': 'Среди всех тегов', 'value': 'selected'}]),
    html.Div([
        dcc.Graph(
            id='tags_pairs_pie_chart',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        ),
        dcc.Graph(
            id='tag_dynamics_line_chart',
            figure={}, style={'resize': 'horizontal', 'overflow': 'visible'}
        )
    ], style={'display': 'flex', 'resize': 'horizontal', 'overflow': 'auto'}),
    dcc.DatePickerSingle(id='datePicker', min_date_allowed=date(1978, 8, 5),
                         max_date_allowed=date(2023, 9, 10),
                         initial_visible_month=date(2022, 6, 5),
                         date=date(2022, 6, 5)),
    html.Div(id="DataTable", children=[])
])


@callback(
    Output("top_tag-histogram2", "figure"),
    Output("first_dropdown", "options"),
    Output("first_dropdown", "value"),
    Input("tag-count-slider2", "value"),
    config_prevent_initial_callbacks=False
)
def refresh_top_tags2(val):
    global rq
    global paired_tags_data
    global pairs_count
    if(val>pairs_count):
        paired_tags_data = pd.DataFrame(
            dict(zip(paired_tags_df_col_names, rq.get_top_paired_tags_f_top_tags(val*2, 10)))
        )
        pairs_count = val * 2

    global top_tags_data
    if val > top_tags_data[second_df_names[0]].size:  # если


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

    options = sort_values[second_df_names[0]];
    value = options[0];

    return figure2, options, value


def get_data_for_pie_chart(original_df, arr, selected_main_tag, full=False):
    data_in = original_df.loc[original_df[arr[0]] == selected_main_tag]
    perc = 100.00 - sum([float(i) for i in data_in[arr[3]].to_list()])
    row_index = 2
    if full:
        row_index = 3
        new_row = {arr[1]: 'Other', arr[2]: 0, arr[3]: perc}
        data_in = pd.concat([data_in, pd.DataFrame([new_row])], ignore_index=True)
    # return data_in

    figures = px.pie(data_in,
                     names=arr[1],
                     values=arr[row_index],
                     labels={arr[1]: 'Парное ключевое слово', arr[row_index]: 'Процент'},
                     title=f'Круговая диаграмма самых популярных парных ключевых<br>слов для ключевого слова {selected_main_tag}'
                     )

    figures.update_layout(
        font_family="Courier New",
        title_font_family="Times New Roman",
        title_font=dict(size=14),
        title_x=0.5
    )
    return figures


@callback(
    Output("tags_pairs_pie_chart", "figure"),
    Output("tag_dynamics_line_chart", "figure"),
    Input("first_dropdown", "value"),
    Input("checkList", "value"),
)
def get_graphs(val, val2):




    df = tag_dyn_df.loc[tag_dyn_df[tag_dynamic_df_col_names[0]] == val]  # забираем динамику только для ковидла
    years = df[tag_dynamic_df_col_names[1]].tolist()
    months = df[tag_dynamic_df_col_names[2]].tolist()
    dates = []
    for i in range(len(years)):
        dates.append(date(year=int(years[i]), month=int(months[i]), day=1))
    df.insert(4, 'datest', dates)
    #

    full = (val2 is not None and len(val2) > 0 and val2[0] == 'selected')

    # pie_data=paired_tags_data[paired_tags_data[paired_tags_df_col_names[0]] == val]
    figure = get_data_for_pie_chart(paired_tags_data, paired_tags_df_col_names, val, full)
    df = df.loc[df['datest'] < date(year=2024, month=1, day=1)]
    figure2 = px.line(df,
                      x='datest',
                      y=tag_dynamic_df_col_names[3],
                      labels={'datest': 'Дата', tag_dynamic_df_col_names[3]: 'Количество статей'},
                      title=f'Линейная диаграмма динамики использования ключевого слова {val}'
                      )

    figure2.update_layout()

    return figure, figure2


@callback(
    Output("DataTable", "children"),
    Input("datePicker", "date"),

)
def sdqds(val):
    val = date.fromisoformat(val)
    # val=date(val)
    first_day, day_count = calendar.monthrange(val.year, val.month)
    a1 = date(year=val.year, month=val.month, day=1)
    a2 = date(year=val.year, month=val.month, day=day_count)

    data = monthly_to_tags_df.loc[monthly_to_tags_df['date'] == a1]
    # data = data.loc[data['date'] < a2]
    data1 = data[[monthly_to_tafs_df_cn[0], monthly_to_tafs_df_cn[3]]]

    output = []

    output.append(html.H2(f"Самые популярные теги в {calendar.month_name[a1.month]} {a1.year}"))

    output.append(dash_table.DataTable(data=data1.to_dict('records'),
                                            columns=[{"name": i, "id": i} for i in data1.columns],
                  style_as_list_view=True,
                  style_cell={'padding': '5px'},
                  style_header={
                      'backgroundColor': 'white',
                      'fontWeight': 'bold'
                  },
                  style_cell_conditional=[
                      {
                          'if': {'column_id': c},
                          'textAlign': 'left'
                      } for c in ['Date', 'Region']
                  ],
                  )
                  )

    output.append(html.P(f"{a1}"))
    output.append(html.P(f"{a2}"))
    output.append(html.P(f"{data1}"))
    return output
