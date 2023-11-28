import requests
import json
dec=json.JSONDecoder();
class requestor:
    #дофига методов пока не сделано, можно зеркалить класс для api
    def __init__(self):
        #пока не упаковал в докер ip будет таким
        self.url_start = 'http://127.0.0.1:5500'

    def get_tag_dynamics(self, tag_name):

        r = requests.get(self.url_start + '/tag_dynamics', params={'tag_name': tag_name})
        print(dec.decode(r.content.decode()))
    #из-за регулярок запрос гистограммы скорее всего будет самым долгим среди всех запросов
    def get_hist(self):
        #пока коды не проверял вообще
        r = requests.get(self.url_start + '/size_histogram')
        res = dec.decode(r.content.decode())
        sizes=[element[0] for element in res]#в запросе 2 колонки вернуться, заберём их в массивы
        element_count = [element[1] for element in res]
        return sizes,element_count



rq = requestor()
rq.get_tag_dynamics(tag_name='COVID-19')
res=rq.get_hist()
print("word_counts:", res[0])
print("articles_count:", res[1])
