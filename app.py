from flask import Flask, render_template, request
from flask.ext.sqlalchemy import SQLAlchemy
from flask import jsonify
from stop_words import stops
from collections import Counter
from bs4 import BeautifulSoup
from rq import Queue
from rq.job import Job
from worker import conn
import operator
import os
import requests
import re
import nltk
import json
from word_counter import *

##########################
##### Configuration ######
##########################

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
db = SQLAlchemy(app)
q = Queue(connection=conn)

from models import *

##########################
######### Routes #########
##########################

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html', results=results)


@app.route('/start', methods=['POST'])
def start():
    # get url
    data = json.loads(request.data)
    url = data['url']
    if 'http://' not in url[:7]:
        url = 'http://' + url
    # start job
    job = q.enqueue_call(
        func=count_and_save, args=(url,), result_ttl=5000
    )
    return job.get_id()

@app.route('/results/<job_key>', methods=['GET'])
def results(job_key):
    job = Job.fetch(job_key, connection=conn)

    if job.is_finished:
        result = Result.query.filter_by(id=job.result).first()
        results = sorted(
            result.result_no_stop_words.items(),
            key=operator.itemgetter(1),
            reverse=True
        )[:10]
        return jsonify(results)
    else:
        return 'Nay!', 202

if __name__ == '__main__':
    app.run('0.0.0.0', 5000)
