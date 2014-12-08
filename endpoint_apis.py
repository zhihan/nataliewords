"""
API for the service using Cloud endpoints.
"""

import endpoints
import datetime

from protorpc import remote
from protorpc import messages
from protorpc import message_types


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
    date = messages.StringField(2)

class PostWordsResponse(messages.Message):
    record = messages.MessageField(Record, 1)

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
        # TODO (Get the data from the database)
        fake_record = Record(date = "2014/1/1",
                             words = ["a", "b"]);
        return GetWordsResponse(records = [fake_record])

    @endpoints.method(PostWordsRequest, PostWordsResponse,
                      path = "postwords", http_method = "POST",
                      name = "postwords")
    def post_words(self, req):
        # TODO (Use real data)
        if not req.date:
            d = "2014/1/1"
        else:
            d = req.date
            
        rec = Record(date = d,
                     words = req.words)
        return PostWordsResponse(record = rec)

application = endpoints.api_server([WordsApi])
