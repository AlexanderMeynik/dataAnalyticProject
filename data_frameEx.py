import sys
from datetime import datetime

import pandas as pd

from clientCode.dataRequestService import requestor
import time

start_time = time.time()
rq = requestor()
if (False):
    names_arr_1 = ['subject', 'year', 'month', 'tag_count'];

    tag_dyn_df = pd.DataFrame(
        dict(zip(names_arr_1, rq.get_all_tags_dynamics()))  # этот запрос может длиться 20 секунд
        # и займёт примерно 300 мб оперативы, но зато можно без задержек получать динамики для любого тега
        # поидее можно юзануть и запрос get_tag_dynamics т.к. я его несколько оптимизировал
        # но тут стоит подумать
    )
    df = tag_dyn_df.loc[tag_dyn_df[names_arr_1[0]] == 'COVID-19']  # забираем динамику только для ковидла

    years = df[names_arr_1[1]].tolist()
    months = df[names_arr_1[2]].tolist()
    dates = []
    for i in range(len(years)):
        dates.append(datetime(year=int(years[i]), month=int(months[i]), day=1))
    df.insert(4, 'datest', dates)
    print(df)


def get_data_for_pie_chart(original_df, arr, selected_main_tag, full=False):
    data_in = original_df.loc[original_df[arr[0]] == selected_main_tag]
    perc = 100.00 - sum([float(i) for i in data_in[arr[3]].to_list()])

    # data_in = data_in[[arr[1], arr[3]]]
    if full:  # суть  этой опции состоит в том, что мы можем считать долю использования по разному
        # a) мы можем взять топ 10 парных тегов и посчитать процент использовани только среди них
        # тогда в качестве колонки для оси y можно брать колонку names_arr_2[3]
        # б) можно посчитать процент использования относительно общего числа(не только тех например 10 что мы взяли)
        # тогда я решил добавлять ряд с подписью Other, который будет добивать все осташееся место в pie chart
        # y=arr[3]
        new_row = {arr[1]: 'Other', arr[3]: perc}
        data_in = pd.concat([data_in, pd.DataFrame([new_row])], ignore_index=True)
    return data_in


if (False):
    names_arr_2 = ['main_tag', 'subject', 'percentage', 'total_percentage'];

    tag_dyn_df2 = pd.DataFrame(
        dict(zip(names_arr_2, rq.get_top_paired_tags_f_top_tags(10, 10)))
    )

    data = get_data_for_pie_chart(tag_dyn_df2, names_arr_2, 'SARS-CoV-2', True)
    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)
if (False):
    names_arr_3 = ['journal_names', 'creator', 'articles_published'];

    tag_dyn_df3 = pd.DataFrame(
        dict(zip(names_arr_3, rq.get_top_authors_for_all_journals()))
    )

    data = tag_dyn_df3.loc[tag_dyn_df3[names_arr_3[0]] == 'AACE Clinical Case Reports']

    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)

if (False):
    names_arr_4 = ['journal_names', 'creator', 'tags_count'];

    tag_dyn_df4 = pd.DataFrame(
        dict(zip(names_arr_4, rq.get_top_tags_for_all_journals(12)))
    )

    data = tag_dyn_df4.loc[tag_dyn_df4[names_arr_4[0]] == 'AACE Clinical Case Reports']

    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)
if (False):
    names_arr_5 = ['creator', 'journal_count', ];

    tag_dyn_df5 = pd.DataFrame(
        dict(zip(names_arr_5, rq.get_top_authors_by_journal_num(14)))
    )

    # data=tag_dyn_df5.loc[tag_dyn_df5[names_arr_5[0]] == 'AACE Clinical Case Reports']
    data = tag_dyn_df5
    print("--- %s seconds ---" % (time.time() - start_time))
    print(data)
if (False):
    auth_count_hist_df_cn = ['auth_count', 'articles_count']
    auth_count_hist_df = pd.DataFrame(
        dict(zip(auth_count_hist_df_cn, rq.get_auth_hist()))
    )
    print(auth_count_hist_df)

if (False):
    journals_for_dyn_df_cn = ['word_count', 'articles_count']
    # я таким образом просто именую наши колонки в dat frame
    journals_for_dyn_df = pd.DataFrame(
        dict(zip(journals_for_dyn_df_cn, rq.get_hist()))
    )
    print(journals_for_dyn_df)

if (False):
    journals_for_dyn_df_cn = ['name', 'articles_count']
    # я таким образом просто именую наши колонки в dat frame
    journals_for_dyn_df = pd.DataFrame(
        dict(zip(journals_for_dyn_df_cn, rq.get_venn_diagram()))
    )
    print(journals_for_dyn_df)

from dateutil.relativedelta import relativedelta
from datetime import date
if (True):

    monthly_to_tafs_df_cn = ['subject', 'years', 'months', 'tag_scores']
    # я таким образом просто именую наши колонки в dat frame
    monthly_to_tags_df = pd.DataFrame(
        dict(zip(monthly_to_tafs_df_cn, rq.get_monthly_tags(5)))
    )

    years = monthly_to_tags_df[monthly_to_tafs_df_cn[1]].tolist()
    months = monthly_to_tags_df[monthly_to_tafs_df_cn[2]].tolist()
    dates = []
    for i in range(len(years)):
        dates.append(date(year=int(years[i]), month=int(months[i]), day=1))
    monthly_to_tags_df.insert(4, 'date', dates)

    latest = (monthly_to_tags_df['date'].unique().tolist())

    count = 10
    # datPickeeSingle get year and mounth
    date = monthly_to_tags_df['datest'].to_list()[count]
    # datetime.now()+relativedelta(months=-6)
    ddd = monthly_to_tags_df.loc[monthly_to_tags_df['datest'] == latest[8]]
    print(ddd)

    print(latest, end='\n')

    # https://dash.plotly.com/dash-core-components/datepickerrange

    currentMonth = datetime.now().month
    # print(word_count_hist_df.loc)

if (False):
    journals_for_dyn_df_cn = ['journal_names', 'number_of_months', 'articles_published_in_journal',
                              'articles_per_month']
    # я таким образом просто именую наши колонки в dat frame
    journals_for_dyn_df = pd.DataFrame(
        dict(zip(journals_for_dyn_df_cn, rq.get_journals_for_dynamics(2)))
    )
    #rem = 5
    #journals_for_dyn_df = journals_for_dyn_df.tail(len(journals_for_dyn_df.index) - rem)
    pd.set_option('display.max_columns', None)

    print(journals_for_dyn_df[journals_for_dyn_df_cn[0]].tolist())


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
            dates.append(datetime(year=1600,month=1,day=1))
        else:
            dates.append(datetime(year=int(years[i]), month=int(months[i]), day=1))
    journals_dynamics_df.insert(4, 'dates', dates)

    # print(journals_dynamics_df)

    top_tags_all_df_cn = ['journal_names', 'subject', 'tag_counts']
    # я таким образом просто именую наши колонки в dat frame
    top_tags_all_df = pd.DataFrame(
        dict(zip(top_tags_all_df_cn, rq.get_top_tags_for_all_journals(10)))
    )

    top_auth_all_df_cn = ['journal_names', 'creator', 'tag_counts']
    # я таким образом просто именую наши колонки в dat frame
    top_auth_all_df = pd.DataFrame(
        dict(zip(top_auth_all_df_cn, rq.get_top_authors_for_all_journals(10)))

    )

    top_auth_by_jorn_df_cn = ['creator', 'journal_count']
    # я таким образом просто именую наши колонки в dat frame
    top_auth_by_jorn_df = pd.DataFrame(
        dict(zip(top_auth_by_jorn_df_cn, rq.get_top_authors_by_journal_num(20)))

    )

    data = journals_dynamics_df.loc[journals_dynamics_df[journals_dynamics_df_cn[0]] == 'Surface Science Reports']

    print(top_tags_all_df.loc[top_tags_all_df[top_tags_all_df_cn[0]] == 'Surface Science Reports'])
    print('\n\n\n\n')
    print(top_auth_all_df.loc[top_auth_all_df[top_auth_all_df_cn[0]] == 'Surface Science Reports'])
    print('\n\n\n\n')
    print(top_auth_by_jorn_df)
    print('\n\n\n\n')
    print(data)
