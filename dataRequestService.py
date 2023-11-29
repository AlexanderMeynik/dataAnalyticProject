import requests
import json

from requests import RequestException

dec = json.JSONDecoder();


class requestor:
    def check_status(self, r):
        if (r.status_code != 200):
            # print()
            raise RequestException(r.url, r.status_code, r.headers)

    # дофига методов пока не сделано, можно зеркалить класс для api
    def __init__(self):
        # пока не упаковал в докер ip будет таким
        self.url_start = 'http://127.0.0.1:5000'

    def get_top_tags(self, tag_count=10):
        r = requests.get(self.url_start + '/top_tags', params={'tag_count': tag_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        subjects = [element[0] for element in arrays]  # string[]
        tag_scores = [element[1] for element in arrays]  # int[]
        return subjects, tag_scores

    def get_tag_dynamics(self, tag_name):
        r = requests.get(self.url_start + '/tag_dynamics', params={'tag_name': tag_name})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        subject = [element[0] for element in arrays]  # string[]
        years = [element[1] for element in arrays]  # int[]
        months = [element[2] for element in arrays]  # int[]
        tag_scores = [element[3] for element in arrays]  # int[]
        return subject, years, months, tag_scores

    def get_monthly_tags(self, tag_count):
        r = requests.get(self.url_start + '/top_month_tags', params={'tag_count': tag_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        subject = [element[0] for element in arrays]  # todo проверить выходные результаты
        years = [element[1] for element in arrays]  # int[]
        months = [element[2] for element in arrays]  # int[]
        tag_scores = [element[3] for element in arrays]  # string
        return subject, years, months, tag_scores

    def get_top_paired_tags_f_top_tags(self, top_count, pair_count):
        r = requests.get(self.url_start + '/top_pairs_top_tags',
                         params={'top_count': top_count, 'pair_count': pair_count})
        self.check_status(r)

        arrays = dec.decode(r.content.decode())

        main_tags = [element[0] for element in arrays]  # string[]
        paired_tags = [element[1] for element in arrays]  # string[]
        percentages = [element[2] for element in arrays]  # float[]
        return main_tags, paired_tags, percentages

    def get_articles_by_tag_name(self, tag_name):
        r = requests.get(self.url_start + '/get_articles_by_tag',
                         params={'tag_name': tag_name})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        article_ids = [element[0] for element in arrays]  # string[]
        cover_dates = [element[1] for element in arrays]  # string[]
        return article_ids, cover_dates

    def get_pairs_for_one_tag(self, tag_name,pair_count=10):
        r = requests.get(self.url_start + '/top_pairs',
                         params={'tag_name': tag_name,'pair_count':pair_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        paired_subjects = [element[0] for element in arrays]  # string[]
        paired_scores = [element[1] for element in arrays]  # int[]
        return paired_subjects, paired_scores

    # из-за регулярок запрос гистограммы скорее всего будет самым долгим среди всех запросов
    def get_hist(self):
        # пока коды не проверял вообще
        r = requests.get(self.url_start + '/size_histogram')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        sizes = [element[0] for element in arrays]  # в запросе 2 колонки вернуться, заберём их в массивы
        element_count = [element[1] for element in arrays]
        return sizes, element_count

    def get_articles_with_title_word_count(self, size):
        r = requests.get(self.url_start + '/find_articles_by_tittle_size',
                         params={'size': size})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        article_ids = [element[0] for element in arrays]  # string[]
        word_counts = [element[1] for element in arrays]  # int[]
        tittles = [element[2] for element in arrays]  # string[]
        return article_ids, word_counts, tittles

    def get_top_authors(self,author_count=10):
        r = requests.get(self.url_start + '/get_top_authors',
                         params={'author_count': author_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        creators = [element[0] for element in arrays]  # string[]
        article_counts = [element[1] for element in arrays]  # int[]

        return creators, article_counts
