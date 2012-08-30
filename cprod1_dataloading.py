import json
import csv

from os import path
from collections import defaultdict

def load_product_catalog(fname):
    return json.loads(open(fname, 'r').read())['Product']

def load_dataset(fname):
    return json.loads(open(fname, 'r').read())['TextItem']

def load_labels(fname):
    return ({
        'id': row['id'].split(':')[0],
        'first': int(row['id'].split(':')[1].split('-')[0]),
        'last': int(row['id'].split(':')[1].split('-')[1]),
        'catalogids': row['documents'].split() if row['documents'] != '0' else []
    } for row in csv.DictReader(open(fname, 'r')))

def load_all(root, verbose=True):
    if verbose: print('Loading product catalog...')
    prods = load_product_catalog(path.join(root, 'products.json'))

    if verbose: print('Loading supervised trainingset')
    trainset = load_dataset(path.join(root, 'training-annotated-text.json'))

    if verbose: print('Loading the hand-generated labels')
    #labels = load_labels(path.join(root, 'training-disambiguated-product-mentions.csv'))
    labels = load_labels(path.join(root, 'training-disambiguated-product-mentions.csv'))

    return prods, trainset, labels

def labels_by_doc(labels):
    docs = defaultdict(list)
    for label in labels:
        docs[label['id']].append({'first': label['first'], 'last': label['last'], 'ids': label['catalogids']})
    return docs

