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
        # todo динамика тега, нужна для динамики популярности тега на стр 1
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
        # todo станица с гистограммами(гистограмма с распреде по числу авторов)
        # наверное придётся взять head(60), но скорее больше или что-то того т.к.
        # есть статьи с таким числом авторов(2654) что там всего 1 такая и будет
        # и график в этой части прост будет пустым
        r = requests.get(self.url_start + '/auth_count_histogram')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())
        auth_count = [element[0] for element in arrays]
        element_count = [element[1] for element in arrays]
        return auth_count, element_count

    def get_auth_subj_count_hist(self, size=10):
        # пока коды не проверял вообще
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
        # todo забрал все динамик журналов по годам
        # можно забирать статистики для 1 журнала используя pandas
        # сравнивая name с каким-то val
        r = requests.get(self.url_start + '/get_all_journal_pub_frequency')
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        journal_names = [element[0] for element in arrays]  # string[]
        years = [element[1] for element in arrays]  # int[]
        months = [element[2] for element in arrays]  # int[]
        article_counts = [element[3] for element in arrays]  # int[]
        return journal_names, years, months, article_counts

    def get_journals_for_dynamics(self, group_count=10):
        # todo в этом запросе мы получаем журналы для построения динамик
        # суть запроса состит в том, что для каждого журнала тут
        # получено его имя, число месяцев, в которые журнал публиковался
        # если все загруженные здесь статьи были опубликованы в месяци( то это число булет равно 1)
        # я решил осотртировать данные по числу месяцев( чтобы сначала были журналы
        # где больше разных месяцев с опубликованными статьсями
        # т.к. записей может быть слишком много(и у многих журналов характеристки(number_of_months) дублируются)
        # я добавил поле rank и group count
        # смысл состоит в том, что если у нас много журналов с number_of_months=10
        # то для этой группы заберётся максимум group_count элементов
        # далее в самом падасе можете играться с фильтрами и сортровками
        # чтобы получать нужную выборку журналов
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
        # todo тут мы просто забираем топы group_count журналов для всех
        # журналов
        # эти данные нфжны для таблицы или pie диаграммы
        # на странице 3(про журналы)
        # чтобы получить топ для журнала с можно в pandas фильтровать по 1(по порядку) ряду

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
        # todo аналогично предыдущему, но выводит top group_count
        # авторов по числу публикаций в журнале

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
        # это топ авторов по числу журналов, где он опубликовался
        # т.к. у меня нет данных об id автора
        # я не могу точно сказать будет ли 2 Wan Wey одним человеком
        # или разными
        # todo можео добавить к списку диагармм на 3 странице про журналы
        # стоит брать не все а первые n элементов иначе очень много

        r = requests.get(self.url_start + '/get_top_authors_by_journals_count',
                         params={'auth_count': auth_count}
                         )
        self.check_status(r)
        arrays = dec.decode(r.content.decode())

        creator = [element[0] for element in arrays]  # string[]
        journal_count = [element[1] for element in arrays]  # int[]
        return creator, journal_count

    def get_all_tags_dynamics(self):
        # не знаю зачем, если хотите загрузить 300 мб оперативы можете динамику тегов загружать сразу
        #и прост отфильтровывать
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