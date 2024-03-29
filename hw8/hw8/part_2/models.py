from mongoengine import Document, StringField, BooleanField


class Contacts(Document):
    full_name = StringField(required=True)
    email = StringField(required=True)
    sent = BooleanField(default=False)