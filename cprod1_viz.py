from sys import argv

from cgi import escape

from cprod1_dataloading import *

if __name__ == '__main__':
    root = argv[1] if len(argv) > 1 else 'TrainingSet'

    prods, trainset, labels = load_all(root, verbose=False)
    lbd = labels_by_doc(labels)

    for docid, labels in lbd.iteritems():
        doc = map(escape, trainset[docid])

        for label in labels:
            if label['ids']:
                # It is in the catalog, check out by how much %
                # TODO: some are in catalog many times O.o
                id = label['ids'][0]
                label_len = label['last'] - label['first'] + 1
                prod_len = len(prods[id][0].split())
                overlap = float(label_len) / prod_len

                lightening_color = 255 - int(155*overlap)

                if prods[id][1] == 'CE':
                    style = 'background-color: rgb(255,{},{});'.format(lightening_color, lightening_color)
                elif prods[id][1] == 'AU':
                    style = 'background-color: rgb({},{},255);'.format(lightening_color, lightening_color)
                else:
                    style = 'background-color: rgb({},{},{});'.format(lightening_color, lightening_color, lightening_color)

                style += ' border: 1px solid black;'

            else:
                style = 'color: green; border: 1px solid black;'

            doc[label['first']] = '<span style="' + style + '">' + doc[label['first']]
            doc[label['last']] += '</span>'

        doc = filter(lambda word: '<s>' not in word, doc)
        print('<p>' + ' '.join(doc) + '</p>')
