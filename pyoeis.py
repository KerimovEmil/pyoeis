import codecs
import json
import os
import re
import requests

from collections import OrderedDict


def get_oeis_names():
    oeis_names = OrderedDict()

    with codecs.open(os.path.join(os.getcwd(), 'data', 'oeis_names.json'), 'r', 'utf-8') as f:
        oeis_names = json.load(f)

    return oeis_names


def get_oeis_seq_meta(sid):
    return json.loads(requests.get('https://oeis.org/search?q={}&fmt=json'.format(sid)).text)


def get_oeis_seq_table(sid):
    table = OrderedDict()

    res = requests.get('http://oeis.org/{}/b{}.txt'.format(sid, sid[1:]))
    lines = [s for s in res.text.split('\n') if s]

    for li in lines:
        n, an = map(int, li.split(' '))
        seq[n] = an

    return table


def save_oeis_seq_table(sid, fullpath):
    table = get_oeis_seq_table(sid)

    with codecs.open(fullpath, 'w', 'utf-8') as f:
        json.dump(table, f)

