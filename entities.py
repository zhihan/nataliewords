import datetime

from google.appengine.ext import ndb

""" 
The entities defined in this app 
"""

class User(ndb.Model):
    user = ndb.UserProperty(required = True)

    @classmethod
    def find(cls, u):
        return cls.query(cls.user == u)

class Words(ndb.Model):
    date = ndb.DateProperty(required = True)
    words = ndb.StringProperty(required = True)
    notes = ndb.StringProperty()
    

    
