import psycopg2
import time
start_time = time.time()

from dataRequestService import requestor

rq = requestor()
'''rq.get_tag_dynamics(tag_name='COVID-19')
res = rq.get_hist()
print("word_counts:", res[0])
print("articles_count:", res[1])'''
#res=rq.get_top_tags(20)
#res=rq.get_tag_dynamics('COVID-19')
res = rq.get_monthly_tags(5)#opt
#res = rq.get_top_paired_tags_f_top_tags(5,5)
#res=rq.get_articles_by_tag_name('COVID-19')

#res=rq.get_pairs_for_one_tag('COVID-19',100)


#res=rq.get_hist()
#res=rq.get_articles_with_title_word_count(2)#аналогично предыдущему исп. тот же mat view

#res=rq.get_pairs_for_one_tag('COVID-19',1000) #оптимиз с то пары

#res = rq.get_top_paired_tags_f_top_tags(5,5)
print("--- %s seconds ---" % (time.time() - start_time))
[print(elem) for elem in res ];
print(len(res[0]))
