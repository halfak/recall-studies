"""
Gets scores for a set of revisions

Usage:
    score_revisions <ores> <context> <model>

Options:
    <ores>     The base URL to an ORES instance
    <context>  The name (usually dbname) of the context to score within
    <model>    The name of the model to apply
"""
import sys
from itertools import islice

import docopt
import requests

import mysqltsv


def main():
    args = docopt.docopt(__doc__)

    ores_url = args['<ores>']
    context = args['<context>']
    model = args['<model>']

    revs = mysqltsv.Reader(sys.stdin)

    run(ores_url, context, model, revs)


def run(ores_url, context, model, revs):

    writer = mysqltsv.Writer(sys.stdout, headers=revs.headers + ['proba'])

    for batch in batches(revs):
        rev_ids = [r.rev_id for r in batch]
        probas = get_probas(ores_url, context, model, rev_ids)

        for rev, proba in zip(batch, probas):
            writer.write(list(rev) + [proba])


def batches(revs):
    revs_iter = iter(revs)
    batch = list(islice(revs_iter, 50))
    while len(batch) > 0:
        yield batch
        batch = list(islice(revs_iter, 50))


def get_probas(ores_url, context, model, rev_ids):
    url = "/".join([ores_url, context, model]) + "/"
    response = requests.get(url, params={'revids': "|".join(rev_ids)})
    doc = response.json()
    for rev_id in rev_ids:
        if 'error' in doc[rev_id]:
            sys.stderr.write(doc[rev_id]['error']['message'] + "\n")
        else:
            yield doc[rev_id]['probability']['true']
