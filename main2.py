import psycopg2

from dataRequestService import requestor

rq = requestor()
'''rq.get_tag_dynamics(tag_name='COVID-19')
res = rq.get_hist()
print("word_counts:", res[0])
print("articles_count:", res[1])'''



res = rq.get_top_paired_tags_f_top_tags(10, 10)
[print(elem) for elem in res ];