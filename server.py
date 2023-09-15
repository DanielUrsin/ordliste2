# examples/things.py

# Let's get this party started!
import logging
import os
from wsgiref.simple_server import make_server

import falcon

global adjektiver
adjektiver = None

list_path = 'resources/fullformsliste.txt'
global count
count = 0


logging.basicConfig(filename="wordslog",
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)




def tall_til_tekst(tall):
    '''
    Translates numericial strings to worded numbers in Norwegian.
    Only numbers 1-100 are supported.
    '''

    nullTilTjue = {
        "0":"", "1":"en", "2":"to", "3":"tre", "4":"fire", "5":"fem",
        "6":"seks", "7":"syv", "8":"åtte", "9":"ni", "10":"ti",
       "11":"elleve", "12":"tolv", "13":"tretten", "14":"fjorten",
       "15":"femten", "16":"seksten", "17":"søtten", "18":"atten",
       "19":"nitten"
    }

    tiere = {
        "2":"tjue", "3":"tretti", "4":"førti", "5":"femti",
        "6":"seksti", "7":"søtti", "8":"åtti", "9":"nitti"
    }

    if 0 <= int(tall, 10) < 20:
        tekst = nullTilTjue[tall]
    elif 20 <= int(tall, 10) < 100:
        tekst = tiere[tall[0]]+nullTilTjue[tall[1]]
    elif int(tall, 10) == 100:
        tekst = "hundre"
    else:
        raise ValueError

    return tekst

def populate():
    '''
    Parses the main dictionary file and creates a pure adjective list.
    The adjectives are written to an output file. The output file will be
    OVERWRITTEN each time this fucntion is called.
    '''
    module_dir = os.path.dirname(__file__)  # get current directory
    file_path = os.path.join(module_dir, list_path)
    input = open(file_path, "r", encoding="iso-8859-1", errors='ignore')

    hovedliste = []
    for line in input:
        linje = line.split('\t')
        ord = linje[2]
        klasse = (linje[3].split(' '))
        if ord[0] == '-':
            continue
        if ord[-1] == 'e':
            continue
        if ord[-1] == 't':
            continue
        if 'adj' not in klasse:
            continue
        if 'ub' not in klasse:
            continue
        if 'pos' not in klasse:
            continue
        if 'be' in klasse:
            continue
        hovedliste.append(ord)

    hovedliste = list(set(hovedliste))
    hovedliste.sort(key=str.casefold)

    return hovedliste

def hent_adjektiver(alder):
    '''Returns two adjectives with the same first letter as the input string.'''
    global adjektiver

    ordliste = []
    for line in adjektiver:
        if line[0] == alder[0]:
            ordliste.append(line)

    if not len(ordliste):
        raise ValueError("Ingen ord funnet")

    rand1 = int.from_bytes(os.urandom(4), byteorder='big')%len(ordliste)
    rand2 = int.from_bytes(os.urandom(4), byteorder='big')%len(ordliste)

    return ordliste[rand1], ordliste[rand2]


class WordResource:
    def on_get(self, req, resp):
        """Handles GET requests"""
        global adjektiver
        global count

        if adjektiver == None:
            print("populating")
            adjektiver = populate()
            print("pupulated")
        try:
            alder = req.params.get("alder", 100)
        except:
            alder = 100
        if alder.isnumeric():
            alder = tall_til_tekst(alder)
        adj1, adj2 = hent_adjektiver(alder)
        
        resp.status = falcon.HTTP_200  # This is the default status
        resp.content_type = falcon.MEDIA_TEXT  # Default is JSON, so override
        resp.text = f'{adj1}, {adj2} og {alder}'
        count += 1
        logging.info(f"Req from {req.remote_addr} got \"{resp.text}\"")




app = falcon.App()
app.add_route('/ord', WordResource())

if __name__ == '__main__':
    with make_server('', 23232, app) as httpd:
        print('Serving on port 23232...')

        # Serve until process is killed
        httpd.serve_forever()