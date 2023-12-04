import sys

import pandas as pd

from clientCode.dataRequestService import requestor
import time

start_time = time.time()
rq = requestor()
if (False):#todo пример забора  всех примеров(таким макараром я его тут скипаю, но можно потестить)

    names_arr_1 = ['subject', 'year', 'month', 'tag_count'];

    tag_dyn_df = pd.DataFrame(
        dict(zip(names_arr_1, rq.get_all_tags_dynamics()))#этот запрос может длиться 20 секунд
        #и займёт примерно 300 мб оперативы, но зато можно без задержек получать динамики для любого тега
        #поидее можно юзануть и запрос get_tag_dynamics т.к. я его несколько оптимизировал
        #но тут стоит подумать
    )
    df = tag_dyn_df.loc[tag_dyn_df[names_arr_1[0]] == 'COVID-19']#забираем динамику только для ковидла
    print(df[names_arr_1])


def get_data_for_pie_chart(original_df, arr, selected_main_tag, full=False):
    data_in = original_df.loc[original_df[arr[0]] == selected_main_tag]
    perc = 100.00 - sum([float(i) for i in data_in[arr[3]].to_list()])

    #data_in = data_in[[arr[1], arr[3]]]
    if full:#суть  этой опции состоит в том, что мы можем считать долю использования по разному
        #a) мы можем взять топ 10 парных тегов и посчитать процент использовани только среди них
        # тогда в качестве колонки для оси y можно брать колонку names_arr_2[3]
        #б) можно посчитать процент использования относительно общего числа(не только тех например 10 что мы взяли)
        # тогда я решил добавлять ряд с подписью Other, который будет добивать все осташееся место в pie chart
        # y=arr[3]
        new_row = {arr[1]: 'Other', arr[3]: perc}
        data_in = pd.concat([data_in, pd.DataFrame([new_row])], ignore_index=True)
    return data_in


# todo это пример того как можно получить данные для pie_chart на второй стрпанице
names_arr_2 = ['main_tag', 'subject', 'percentage', 'total_percentage'];

tag_dyn_df2 = pd.DataFrame(
    dict(zip(names_arr_2, rq.get_top_paired_tags_f_top_tags(10, 10)))
)

data = get_data_for_pie_chart(tag_dyn_df2, names_arr_2, 'SARS-CoV-2',True)
print("--- %s seconds ---" % (time.time() - start_time))
print(data)

# [print(elem) for elem in res]
