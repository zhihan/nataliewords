import datetime
import re
import random
import entities

"""
Basic support for words. Listing, merging and serializing
"""

class Words:
    def __init__(self):
        self.date = datetime.date.today()
        self.words = []
    
    def save(self):
        return entities.Words(date = self.date, \
                              words = self.words)
    @staticmethod
    def load(entity):
        w = Words()
        w.date = entity.date
        w.words = entity.words
        if entity.notes:
            w.notes = entity.notes
        return w

def get_words(s):
    """
    Parse a list of words and return as set.
    """
    w = re.split("\W+", s)
    w = [x for x in w if x]
    return set(w)


def random_pick(l, n):
    """
    Given a list of words, randomly pick n unique ones from them
    """ 
    ll = list(l)
    x = random.sample(ll, n)
    return x
