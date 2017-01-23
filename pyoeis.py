import codecs
import json
import os
import re
import requests

from collections import OrderedDict


def get_oeis_names():
    """
        The list of all OEIS sequence IDs and their names contained in this
        gzipped file

            https://oeis.org/names.gz

        has been converted to a static local JSON file, stored in the data
        subdirectory of this repository. This method loads that and returns
        it as a dict.
    """
    oeis_names = OrderedDict()

    with codecs.open(
        os.path.join(os.getcwd(), 'data', 'oeis_names.json'), 'r', 'utf-8'
    ) as f:
        oeis_names = json.load(f)

    return oeis_names


def get_oeis_sequence_meta(sid):
    """
        Returns the sequence metadata dictionary - more information can be
        found here:

            http://oeis.org/wiki/JSON_Format,_Compressed_Files
    """
    return json.loads(
        requests.get('https://oeis.org/search?q={}&fmt=json'.format(sid)).text
    )


def get_oeis_sequence_table(sid):
    """
        Gets the table of terms of the sequence #sid (should regex match
        'A(\d+) (.*)') from its remote b-file, e.g. the b-file for the
        sequence A001221 is located at

            https://oeis.org/A001221/b001221.txt

        More information can be found here:

            http://oeis.org/wiki/B-files
    """
    table = OrderedDict()

    res = requests.get('http://oeis.org/{}/b{}.txt'.format(sid, sid[1:]))
    lines = [
        s for s in res.text.split('\n') if s and re.match(r'(\d+) (\d+)', s)
    ]

    for li in lines:
        n, an = map(int, li.split(' '))
        table[n] = an

    return table


def save_oeis_sequence_table(
    sid, fullpath=os.path.join(os.getcwd(), '{}_table.json'.format(sid))
):
    """
        Saves the sequence table/dict as a local JSON file (full path required,
        including file name).
    """
    table = get_oeis_sequence_table(sid)

    with codecs.open(fullpath, 'w', 'utf-8') as f:
        json.dump(table, f)

