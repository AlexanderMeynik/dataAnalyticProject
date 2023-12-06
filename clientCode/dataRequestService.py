import requests
import json

from requests import RequestException

dec = json.JSONDecoder();


class requestor:
    def check_status(self, r):
        if (r.status_code != 200):
            # print()
            raise RequestException(r.url, r.status_code, r.headers)

    def __init__(self,docker=True):
        self.url_start = 'http://server_dev:5000'#todo make config for different variants
        #todo uncoment if run locally
        #self.url_start = 'http://127.0.0.1:5000'

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

        subject = [element[0] for element in arrays]
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
        percentages = [element[2] for element in
                       arrays]  # float[] в этом поле насчитывается процент появлений среди только выбранных пар
        total_percentages = [element[3] for element in
                             arrays]  # float[] здесь же мы считаем процент к общему числу тегов
        return main_tags, paired_tags, percentages, total_percentages

    def get_articles_by_tag_name(self, tag_name):
        r = requests.get(self.url_start + '/get_articles_by_tag',
                         params={'tag_name': tag_name})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        article_ids = [element[0] for element in arrays]  # string[]
        cover_dates = [element[1] for element in arrays]  # string[]
        return article_ids, cover_dates

    def get_pairs_for_one_tag(self, tag_name, pair_count=10):
        r = requests.get(self.url_start + '/top_pairs',
                         params={'tag_name': tag_name, 'pair_count': pair_count})
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
        sizes = [element[0] for element in arrays]  # int[] в запросе 2 колонки вернуться, заберём их в массивы
        element_count = [element[1] for element in arrays]  # int[]
        return sizes, element_count

    def get_auth_hist(self):
        r = requests.get(self.url_start + '/auth_count_histogram')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        auth_count = [element[0] for element in arrays]
        element_count = [element[1] for element in arrays]
        return auth_count, element_count

    def get_auth_subj_count_hist(self, size=10):
        r = requests.get(self.url_start + '/authors_subject_counts_histogram', params={'size': size})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        auth_count = [element[0] for element in arrays]  # int[]
        subj_count = [element[1] for element in arrays]  # int[]
        article_count = [element[2] for element in arrays]  # int[]
        percentages = [element[3] for element in arrays]  # float[]
        return auth_count, subj_count, article_count, percentages

    def get_articles_with_title_word_count(self, size):
        r = requests.get(self.url_start + '/find_articles_by_tittle_size',
                         params={'size': size})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        article_ids = [element[0] for element in arrays]  # string[]
        word_counts = [element[1] for element in arrays]  # int[]
        tittles = [element[2] for element in arrays]  # string[]
        return article_ids, word_counts, tittles

    def get_top_authors(self, author_count=10):
        r = requests.get(self.url_start + '/get_top_authors',
                         params={'author_count': author_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        creators = [element[0] for element in arrays]  # string[]
        article_counts = [element[1] for element in arrays]  # int[]

        return creators, article_counts

    def get_all_journals_dynamic(self):
        r = requests.get(self.url_start + '/get_all_journal_pub_frequency')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        journal_names = [element[0] for element in arrays]  # string[]
        years = [element[1] for element in arrays]  # int[]
        months = [element[2] for element in arrays]  # int[]
        article_counts = [element[3] for element in arrays]  # int[]
        return journal_names, years, months, article_counts

    def get_journals_for_dynamics(self, group_count=10):
        r = requests.get(self.url_start + '/get_journals_for_dynamics',
                         params={'group_count': group_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        journal_names = [element[0] for element in arrays]  # string[]
        number_of_months = [element[1] for element in arrays]  # int[]
        articles_published_in_journal = [element[2] for element in arrays]  # int[]
        articles_per_month = [element[3] for element in arrays]  # int[]
        # rnk = [element[4] for element in arrays]  # int[]
        return journal_names, number_of_months, articles_published_in_journal, articles_per_month

    def get_top_tags_for_all_journals(self, group_count=10):

        r = requests.get(self.url_start + '/get_top_tags_for_all_journals',
                         params={'group_count': group_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        journal_names = [element[0] for element in arrays]  # string[]
        subject = [element[1] for element in arrays]  # string[]
        tag_counts = [element[2] for element in arrays]  # int[]

        # rnk = [element[3] for element in arrays]  # int[]
        return journal_names, subject, tag_counts

    def get_top_authors_for_all_journals(self, group_count=10):


        r = requests.get(self.url_start + '/get_top_creators_for_all_journals',
                         params={'group_count': group_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        journal_names = [element[0] for element in arrays]  # string[]
        creator = [element[1] for element in arrays]  # string[]
        articles_published = [element[2] for element in arrays]  # int[]

        # rnk = [element[3] for element in arrays]  # int[]
        return journal_names, creator, articles_published

    def get_top_authors_by_journal_num(self,auth_count=10):
        r = requests.get(self.url_start + '/get_top_authors_by_journals_count',
                         params={'auth_count': auth_count}
                         )
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        creator = [element[0] for element in arrays]  # string[]
        journal_count = [element[1] for element in arrays]  # int[]
        return creator, journal_count

    def get_all_tags_dynamics(self):
        r = requests.get(self.url_start + '/get_all_tags_dynamics')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        subject = [element[0] for element in arrays]  # string[]
        year = [element[1] for element in arrays]  # int[]
        month = [element[2] for element in arrays]  # int[]
        tag_count = [element[3] for element in arrays]  # int[]
        return subject, year, month, tag_count

    def get_venn_diagram(self):
        r = requests.get(self.url_start + '/get_venn_diagram')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        set_name = [element[0] for element in arrays]  # string[]
        cardinality = [element[1] for element in arrays]  # int[]
        return set_name,cardinality

    def get_max_creators(self, auth_count=10):
        r = requests.get(self.url_start + '/get_max_auth',
                         params={'auth_count': auth_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        article_ids = [element[0] for element in arrays]  # string[]
        author_count = [element[1] for element in arrays]  # int[]
        return article_ids,author_count

    def get_max_subject(self, subj_count=10):
        r = requests.get(self.url_start + '/get_max_subj',
                         params={'subj_count': subj_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        article_ids = [element[0] for element in arrays]  # string[]
        subject_count = [element[1] for element in arrays]  # int[]
        return article_ids,subject_count
    def get_max_words_count(self, group_count=10):
        r = requests.get(self.url_start + '/get_max_word_count',
                         params={'group_count': group_count})
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        article_ids = [element[0] for element in arrays]  # string[]
        word_counts = [element[1] for element in arrays]  # int[]
        return article_ids,word_counts
#rq=requestor()
#res=rq.get_max_words_count(100)
#[print(elem) for elem in res]