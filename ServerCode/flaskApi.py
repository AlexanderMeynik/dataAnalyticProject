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
        return "Error getting tag dynamics" + error, 401


@app.get('/top_pairs_top_tags')
def tag_pair_top_tags():
    top_count = request.args.get('top_count')
    top_pairs = request.args.get('pair_count')
    print(top_count, top_pairs)
    try:
        return jsonify(db.top_pairs_top_tags(top_count, top_pairs)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


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
        return "Error getting tag dynamics" + error, 401


@app.get('/size_histogram')
def hist1():
    try:
        return jsonify(db.histogram()), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


@app.get('/find_articles_by_tittle_size')
def tittlesizefind():
    wordcount = request.args.get('size')
    if not wordcount:
        return "Not supported argument configuration", 400
    count = request.args.get('pair_count')
    try:
        return jsonify(db.find_articles_by_tittle_size(wordcount)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


@app.get('/get_top_authors')
def findtopAuthors():
    author_count = request.args.get('author_count')
    try:
        return jsonify(db.get_top_authors(author_count)), 200
    except (Exception, psycopg2.Error) as error:
        return "Error getting tag dynamics" + error, 401


port = int(os.environ.get('PORT', 5000))
print('signals')
#from waitress import serve


#app.run(debug=True, host='0.0.0.0', port=port)
if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=port)
    #serve(app, host="0.0.0.0", port=port)#todo try to run with waitress
