from peewee import *

mysql_db = MySQLDatabase('wildhacks', user='hacker', password='h4ckingILLini')

class BaseModel(Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = mysql_db

# Hilariously insecure user model #fuckitshipit
class User(BaseModel):
    username = CharField(unique=True, max_length=64)
    password = CharField(max_length=64)
    imageUrl = CharField(max_length=256)
    language = CharField(max_length=16)
"""
def create_tables():
    mysql_db.connect()
    mysql_db.create_tables([User])

create_tables()
"""
