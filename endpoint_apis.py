"""
API for the service using Cloud endpoints.




"""

import endpoints
import logging
import datetime

from protorpc import remote
from google.appengine.ext import ndb
from protorpc import message_types

import entities
from protos import *

package = "Words"

WEB_CLIENT_ID = "607994131901-if7as8ck330umlddcgmnmbhr05isalhm.apps.googleusercontent.com"


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
        entity = entities.Record.get_record(endpoints.get_current_user(),
                                            datetime.date.today())
        rec = entities.create_record_message(entity)
        return GetWordsResponse(records = [rec])

    @endpoints.method(PostWordsRequest, PostWordsResponse,
                      path = "postwords", http_method = "POST",
                      name = "postwords")
    def post_words(self, req):
        current_user = endpoints.get_current_user()

        user = entities.User.get_user(current_user)
        u_key = user.put()
        
        logger = logging.getLogger()
        logger.info("Update words for %s" % current_user.email())
                     
        rec = entities.update_record_entity(req, u_key)
        return PostWordsResponse(record = rec)

application = endpoints.api_server([WordsApi])
