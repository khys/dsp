#!/usr/bin/python3
# -*- coding: utf-8 -*-

from flask import Flask, request, json
import time
from werkzeug.routing import BaseConverter
import codecs
import redis


r = redis.StrictRedis(host='10.0.0.3', port='6379', db=0)
app = Flask(__name__)


class RegexConverter(BaseConverter):
    def __init__(self, url_map, *items):
        super(RegexConverter, self).__init__(url_map)
        self.regex = items[0]


app.url_map.converters['regex'] = RegexConverter


@app.route('/win/<regex("[0-9a-zA-Z]*"):user>', methods=['POST'])
def dsp_bid(user):
    if request.headers['Content-Type'] != "application/json":
        return '', 400
    data_r = request.data.decode('utf-8')
    data_dict = json.loads(data_r)
    data_dict['price'] = float(data_dict['price']) * 1000
    data_dict['isClick'] = int(data_dict['isClick'])
    t_budget = float(r.hget(user, 'budget').decode('utf-8')) - float(data_dict['isClick']) * float(r.hget(user, 'cpc').decode('utf-8'))
    r.hset(user, 'budget', t_budget)
    with codecs.open('/home/gordon/budget{}.log'.format(user), 'a', 'utf-8') as writer:
        writer.write("{d},{b}".format(d=int(time.time()), b=t_budget))
        writer.write("\n")
    return '', 204


if __name__ == '__main__':
    app.run()
