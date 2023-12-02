import time

import psycopg2
from configparser import ConfigParser


class databaseService():
    host = ""
    port = ""

    def __init__(self, arg):

        config = ConfigParser()
        config.read('config.ini')
        section = 'service_docker' if arg else 'service_local'
        host = config.get(section, 'ip')
        port = config.get(section, 'port')

        reset_count = 0
        # т.к. звпускаем из  сам сервак из докера теперь строка будет такой)
        while (True):
            try:
                self.connection = psycopg2.connect(database="postgres",
                                                   user="postgres",
                                                   host=host,
                                                   password="2b4djnm3ed2dms",
                                                   port=port)
                time.sleep(1)
                break
            except psycopg2.OperationalError as e:
                time.sleep(1)
                if (reset_count > 500):
                    raise psycopg2.OperationalError
                reset_count = reset_count + 1

    def __del__(self):
        self.connection.close()

    # неясно пока зачем но пусть будет

    def getTopTag(self, num_tags=100):
        rows = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select * from top_tags_all limit {num_tags};""")

            self.connection.commit()
            rows = cursor.fetchall()

        finally:
            if self.connection:
                cursor.close()
            return rows

    def getTagsDynamics(self, tag_name, year=2020, month=2020):
        rows = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select subject,year,month,count(article_id) as tag_score  
                       from (
                       select article_id,unnest(subjects) as subject,extract(month FROM cover_date) as month,
                       extract(year FROM cover_date) as year
                       from articles
                       where '{tag_name}'=any(subjects)) as foo
                       where subject = '{tag_name}'
                       group by year,month,subject
                       order by year desc,month desc,tag_score DESC;""")

            self.connection.commit()
            rows = cursor.fetchall()

        finally:
            # Закрытие курсора и соединения
            if self.connection:
                cursor.close()
            return rows

    def top_mounth_tags(self, tag_count=5):
        rows = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""
            SELECT
                subject,
                year,
                month,
                tag_score
            FROM
                tags_ordered_by_dates
            WHERE
                    rnk <= {tag_count}
            ORDER BY
                year DESC, month DESC, tag_score DESC;""")

            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            # Закрытие курсора и соединения
            if self.connection:
                cursor.close()
            return rows

    def top_pairs_top_tags(self, top_tags=10, pairs_count=10):
        rows = []
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""with top_tags as(
                        select main_tag,tag_score
                        from top_tags_all
						limit {top_tags}),
                         joined_info as
                             (
                                 select top_tags.main_tag,top_tags.tag_score,unnest(array_remove(subjects,top_tags.main_tag)) as subject
                                 from top_tags inner join articles on top_tags.main_tag=ANY(articles.subjects)
                             ),
                         
                         calculated_counts as
                             (
                                 select main_tag,subject,tag_score ,count(subject) as second_tag_score from joined_info
                                 group by main_tag, subject,tag_score
                             ),
                    
                         ranked_info as
                             (
                                 select calculated_counts.*, row_number() over( partition by main_tag order by second_tag_score desc) as rnk
                                 from  calculated_counts
                             )
                    
                    select main_tag,subject,round(second_tag_score*100.00/sum(second_tag_score) over (partition by main_tag),2) as percentage
                    from ranked_info
                    where rnk<={pairs_count}
                    order by tag_score desc, second_tag_score desc;""")

            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def get_articles_by_tag(self, tag_name):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select array_agg(article_id),
                    array_agg(cover_date)
                    from articles
                    where '{tag_name}'=Any(subjects);
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def top_pairs(self, tag_name, pairs_count=100):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select subject,count(*) as tag_score from
                        (select article_id,unnest(subjects) as subject from articles where '{tag_name}'=any(subjects)) as subj
                    where subject!='{tag_name}'
                    group by subject
                    order by tag_score desc limit {pairs_count};""")
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def histogram(self):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select size as word_count,count(article_id) as count_articles
                    from
                        words_tittle 
                    group by word_count
                    order by word_count;
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def author_histogram(self):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select array_length(creators,1) as auth_count,count(article_id) as count_articles
                    from
                        articles
                    where creators is not null
                    group by array_length(creators,1)
                    order by array_length(creators,1);
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def authors_subject_counts_hist(self,size=10):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select auth_count,subj_count,count_articles, round(100*count_articles/(sum(count_articles) over (partition by auth_count)),2) percent from
                        (select array_length(creators,1) as auth_count,array_length(subjects,1) as subj_count,count(article_id) as count_articles,
                        dense_rank() over (PARTITION BY array_length(creators,1) order by count(article_id) desc ) as rnk
                        from
                        articles
                        where creators is not null and articles.subjects is not null
                        group by array_length(creators,1), array_length(subjects,1)) as data
                    where rnk<={size}
                    order by auth_count,count_articles desc;
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def find_articles_by_tittle_size(self, size):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""select data.article_id ,data.size as word_count, a.title
                    from
                        words_tittle as data join articles a on data.article_id=a.article_id
                    where size={size};
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows

    def get_top_authors(self, author_count):
        rows = []
        cursor = False;
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                f"""SELECT
                        UNNEST(creators) AS author,
                        COUNT(*) AS article_count
                    FROM
                        articles
                    WHERE
                            status = 2
                    GROUP BY
                        author
                    ORDER BY
                        article_count DESC
                    LIMIT {author_count};
                    """)
            self.connection.commit()
            rows = cursor.fetchall()
        finally:
            if self.connection:
                cursor.close()
            return rows
