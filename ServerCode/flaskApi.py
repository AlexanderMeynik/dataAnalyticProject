import os
import sys
import time

import psycopg2
from flask import Flask
from dbService import databaseService
from flask import jsonify, request

app = Flask(__name__)
docker = True
if len(sys.argv) >= 2 and sys.argv[1] == 'local':
    docker = False

db = databaseService(docker)

@app.get('/')
def index():
    return jsonify("hello client"),200

@app.get('/top_tags')
def send_top_tags():
    try:
        source = request.args.get('tag_count')
        return jsonify(db.getTopTag(source)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top articles" + error, 401


@app.get('/tag_dynamics')
def tag_dynamics():
    source = request.args.get('tag_name')
    if not source:
        return "Not supported argument configuration", 400
    try:
        return jsonify(db.getTagsDynamics(source)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


@app.get('/top_month_tags')
def top_mth_tag():
    source = request.args.get('tag_count')

    try:
        if source:
            return jsonify(db.top_mounth_tags(source)), 200
        else:
            return jsonify(db.top_mounth_tags()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting monthly tags" + error, 401


@app.get('/top_pairs_top_tags')
def tag_pair_top_tags():
    top_count = request.args.get('top_count')
    top_pairs = request.args.get('pair_count')
    print(top_count, top_pairs)
    try:
        return jsonify(db.top_pairs_top_tags(top_count, top_pairs)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top pairs for top tags" + error, 401


@app.get('/get_articles_by_tag')
def getartbytag():
    name = request.args.get('tag_name')
    if not name:
        return "Not supported argument configuration", 400
    try:
        return jsonify(db.get_articles_by_tag(name)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


@app.get('/top_pairs')
def gettagstoppairs():
    name = request.args.get('tag_name')
    if not name:
        return "Not supported argument configuration", 400
    count = request.args.get('pair_count')
    try:
        return jsonify(db.top_pairs(name, count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top pairs for tag" + error, 401


@app.get('/size_histogram')
def hist1():
    try:
        return jsonify(db.histogram()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting title size histogram" + error, 401

@app.get('/auth_count_histogram')
def hist2():
    try:
        return jsonify(db.author_histogram()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting title size histogram" + error, 401

@app.get('/authors_subject_counts_histogram')
def hist3():
    size = request.args.get('size')
    try:
        return jsonify(db.authors_subject_counts_hist(size)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting title size histogram" + error, 401

@app.get('/find_articles_by_tittle_size')
def tittlesizefind():
    wordcount = request.args.get('size')
    if not wordcount:
        return "Not supported argument configuration", 400
    try:
        return jsonify(db.find_articles_by_tittle_size(wordcount)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting articles with specific tag size" + error, 401


@app.get('/get_top_authors')
def findtopAuthors():
    author_count = request.args.get('author_count')
    try:
        return jsonify(db.get_top_authors(author_count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401

@app.get('/get_all_journal_pub_frequency')
def get_all_dyn():
    try:
        return jsonify(db.get_journal_dynamic_all()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401


port = int(os.environ.get('PORT', 5000))


@app.get('/get_journals_for_dynamics')
def get_journ_for_dyn():
    group_count = request.args.get('group_count')
    try:
        return jsonify(db.get_journals_for_dynamics(group_count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401

@app.get('/get_top_tags_for_all_journals')
def get_top_tags_for_all_journals():
    group_count = request.args.get('group_count')
    try:
        return jsonify(db.get_top_tags_in_journals(group_count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401

@app.get('/get_top_creators_for_all_journals')
def get_top_creators_for_all_journals():
    group_count = request.args.get('group_count')
    try:
        return jsonify(db.get_top_authors_in_journals(group_count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401

@app.get('/get_top_authors_by_journals_count')
def get_top_creators_by_journal_count():
    try:
        return jsonify(db.get_top_authors_by_journal_count()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401

@app.get('/get_all_tags_dynamics')
def get_all_tags_dynamics():
    try:
        return jsonify(db.get_all_tags_dynamics()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting top authors" + error, 401


port = int(os.environ.get('PORT', 5000))
#from waitress import serve


#app.run(debug=True, host='0.0.0.0', port=port)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
    #serve(app, host="0.0.0.0", port=port)#todo try to run with waitress
