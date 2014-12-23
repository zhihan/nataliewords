""" 
The entities defined in this app 

This simple app uses two entities. 

 - User: a user is of the default user type provided by
  the platform. The id of a user is the email. 

 - Record: a record is the collection of words for a specific
  day. A record entity always has a parent user and the date 
  is used as the key to the records. 

"""


import datetime
from google.appengine.ext import ndb

import protos 

class User(ndb.Model):
    user = ndb.UserProperty(required = True)

    @classmethod
    def find(cls, u):
        return cls.query(cls.user == u)

    @staticmethod
    def get_user(u):
        return User(user = u,
                    id = u.email())

class Record(ndb.Model):
    date = ndb.DateProperty(required = True)
    words = ndb.StringProperty(repeated = True)

    @staticmethod
    def get_record(user, date):
        key = ndb.Key('User', user.email(),
                      'Record', date.strftime('%Y%m%d'))
        return key.get()


"""
Create a record message from a record entity
"""
def create_record_message(entity):
    return protos.Record(date = entity.date.strftime('%Y%m%d'),
                         words = entity.words)


"""
Update the entity date using the msg
"""
def update_record_entity(msg, parent_key):
    if not msg.date:
        msg_date = datetime.date.today()
    else:
        msg_date = datetime.datetime.strptime(msg.date,
                                              '%Y%m%d').date()
    dstr = msg_date.strftime('%Y%m%d')
    entity = Record(date = msg_date, 
                    words = msg.words,
                    id = dstr,
                    parent = parent_key)
    entity.put()
    return protos.Record(date = dstr,
                         words = msg.words)

"""
Create a record entity from a record message
"""
def create_record_entity(msg):
    if msg.date:
        dt = datetime.datetime.strptime(msg.date, '%Y%m%d')
        d = dt.date()
    else:
        d = datetime.date.today()
    return Record(date = d, 
                  words = msg.words)
