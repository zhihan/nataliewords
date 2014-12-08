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
        self.notes = ""
        self.user = None
    
    def save(self, parent_key):
        dstr = self.date.strftime('%Y%m%d')
        return entities.Words(date = self.date, 
                              words = self.words,
                              id = dstr,
                              parent = parent_key)
    @staticmethod
    def load(entity):
        w = Words()
        w.date = entity.date
        w.words = entity.words
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
