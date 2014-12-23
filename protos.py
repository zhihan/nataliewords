"""
Protocol buffers for the app 
"""

from protorpc import messages

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


