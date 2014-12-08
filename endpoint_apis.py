"""
API for the service using Cloud endpoints.
"""

import endpoints
import logging

from protorpc import remote
from protorpc import messages
from protorpc import message_types
from words import *
from google.appengine.ext import ndb

package = "Words"

WEB_CLIENT_ID = "607994131901-h6364c6afomr1s72m74m3v36uiiksufn.apps.googleusercontent.com"

"""
Protocol buffers for this API 
"""
class GetUserResponse(messages.Message):
    email = messages.StringField(1, required=True)

class Record(messages.Message):
    date = messages.StringField(1, required=True)
    words = messages.StringField(2, repeated=True)

class GetWordsResponse(messages.Message):
    records = messages.MessageField(Record, 1, repeated=True)

class PostWordsRequest(messages.Message):
    words = messages.StringField(1, repeated=True)

class PostWordsResponse(messages.Message):
    record = messages.MessageField(Record, 1)


def date_to_string(d):
    return "%d/%d/%d" % (d.year, d.month, d.day)

def string_to_date(s):
    parts = s.split('/')
    d = datetime.date(year = int(parts[0]),
                      month = int(parts[1]),
                      day = int(parts[2]))
    return d

"""
End points
"""
@endpoints.api(name = 'wordsapi', version = 'v1',
               allowed_client_ids = [WEB_CLIENT_ID, 
                                     endpoints.API_EXPLORER_CLIENT_ID],
               description = "Natalie words API",
               scopes = [endpoints.EMAIL_SCOPE])
class WordsApi(remote.Service):
    @endpoints.method(message_types.VoidMessage, GetUserResponse,
                     path = "getuser", http_method = "GET",
                     name = "users.getuser")
    def get_user(self, void_request):
        current_user = endpoints.get_current_user()
        return GetUserResponse(email = current_user.email())


    @endpoints.method(message_types.VoidMessage, GetWordsResponse,
                      path = "getmywords", http_method = "GET",
                      name = "getmywords")
    def get_my_words(self, void_request):
        d = datetime.date.today()
        current_user = endpoints.get_current_user()
        key = ndb.Key('User', current_user.email(),
                      'Words', d.strftime('%Y%m%d'))
        entity = key.get()
        w = Words.load(entity)

        logger = logging.getLogger()
        logger.info("Get words for %s" % current_user.email())

        rec = Record(date = date_to_string(w.date),
                     words = w.words)
        return GetWordsResponse(records = [rec])

    @endpoints.method(PostWordsRequest, PostWordsResponse,
                      path = "postwords", http_method = "POST",
                      name = "postwords")
    def post_words(self, req):
        current_user = endpoints.get_current_user()

        user = entities.User(user = current_user, 
                            id = current_user.email())
        u_key = user.put()
        
        logger = logging.getLogger()
        logger.info("Update words for %s" % current_user.email())

        # TODO (check if data exists)
        w = Words()
        w.user = current_user
        w.words = req.words
        entity = w.save(u_key)
        entity.put()

        rec = Record(date = date_to_string(w.date),
                     words = w.words)
                     
        return PostWordsResponse(record = rec)

application = endpoints.api_server([WordsApi])
