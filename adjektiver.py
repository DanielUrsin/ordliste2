
import os, sys, time, re



class Adjektiver:
    '''
    Translates numericial strings to worded numbers in Norwegian.
    Only numbers 1-100 are supported.
    '''
    
    def __init__(self) -> None:
        self.hovedliste = None
        self.list_path = 'resources/fullformsliste.txt'
        self.populate()


    def tall_til_tekst(self, tall):
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

    def populate(self):
        print("Populating ... ", end="")
        module_dir = os.path.dirname(__file__)  # get current directory
        file_path = os.path.join(module_dir, self.list_path)
        input = open(file_path, "r", encoding="iso-8859-1", errors='ignore')
        self.hovedliste = []
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
            self.hovedliste.append(ord)
        self.hovedliste = list(set(self.hovedliste))
        self.hovedliste.sort(key=str.casefold)
        print("Done!")

    def hent_adjektiver(self, alder):
        '''Returns two adjectives with the same first letter as the input string.'''

        if alder.isnumeric():
            alder = self.tall_til_tekst(alder)
        ordliste = []
        for line in self.hovedliste:
            if line[0] == alder[0]:
                ordliste.append(line)

        if not len(ordliste):
            return "nope", "nope"
        rand1 = int.from_bytes(os.urandom(4), byteorder='big')%len(ordliste)
        rand2 = int.from_bytes(os.urandom(4), byteorder='big')%len(ordliste)
        return ordliste[rand1], ordliste[rand2]

