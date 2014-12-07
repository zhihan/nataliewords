import webapp2
from google.appengine.api import users
from entities import User
from google.appengine.ext import ndb


class HomeHandler(webapp2.RequestHandler):
    """ 
    Handle the home page sign-in actions 
    """
    def get(self):
        cur_user = users.get_current_user()
        if cur_user:
            existing_user = User.find(cur_user)
            if not existing_user.get():
                # New user
                user_entity = User(user = cur_user)
                user_entity.put()
                greeting = ('Welcome! %s (<a href = "%s">sign out</a>)' %
                            (cur_user.nickname(), users.create_logout_url('/login')))
            else:
                greeting = ('Welcome back, %s (<a href = "%s">sign out</a>)' %
                            (cur_user.nickname(), users.create_logout_url('/login')))
        else:
            greeting = ('<a href="%s">Sign in</a>' % users.create_login_url("/login"))
        self.response.out.write("<html><body>%s</body></html>" % greeting)

application = webapp2.WSGIApplication([('/login', HomeHandler),], debug=True)
