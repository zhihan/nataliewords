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

class Record(ndb.Model):
    date = ndb.DateProperty(required = True)
    words = ndb.StringProperty(repeated = True)

    
# A record key is a child of a user key
# A record uses the date as the id    
