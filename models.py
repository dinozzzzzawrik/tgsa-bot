from peewee import *

db = SqliteDatabase('database.db')


class WhiteList(Model):
    id = IntegerField(primary_key=True)
    name = CharField(null=False)
    tg_id = IntegerField(null=False, unique=True)

    class Meta:
        db_table = 'WhiteList'
        database = db


class Accounts(Model):
    id = IntegerField(primary_key=True)
    name = CharField(unique=True)
    key = CharField(unique=True)

    class Meta:
        db_table = 'Accounts'
        database = db
