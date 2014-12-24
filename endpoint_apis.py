"""
API for the service using Cloud endpoints.

 - getuser: get the current user.
 - getmywords: get the words for a specific day (default to today)
 - getallmywords: get all the words for a specific user
 - postwords: update the words for a speicific day

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
        user = endpoints.get_current_user()
        if entities.User.get_by_user(user):
            entity = entities.Record.get_record(endpoints.get_current_user(),
                                                datetime.date.today())
            if entity:
                rec = entities.create_record_message(entity)
                return GetWordsResponse(records = [rec])
            else:
                return GetWordsResponse(records = [])
        else:
            return GetWordsResponse(records = [])

    @endpoints.method(message_types.VoidMessage, GetWordsResponse,
                      path = "getallmywords", http_method = "GET",
                      name = "getallmywords")
    def get_all_my_words(self, void_request):
        user = entities.User.get_by_user(endpoints.get_current_user())
        if user:
            l = entities.Record.get_all_records(user)
            return GetWordsResponse(records = entities.create_records(l))
        else:
            return GetWordsResponse(records = [])
    
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
