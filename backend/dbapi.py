from peewee import *
import json

db = SqliteDatabase('tweets.db', threadlocals=True)


class Tweet(Model):
    content = CharField()
    order = IntegerField()

    class Meta():
        database = db

    @classmethod
    def add(cls, content=""):
        return cls.insert_at_index(content, cls.count())

    @classmethod
    def insert_at_index(cls, content, index):
        if not content:
            return None
        if index > cls.count():
            return None

        update_query = (cls.update(order=(cls.order + 1))
                       .where(cls.order >= index))
        update_query.execute()

        tweet = Tweet.create(content=content, order=index)
        if not tweet:
            return None

        return tweet

    @classmethod
    def all_query(cls):
        return Tweet.select().order_by(cls.order)

    @classmethod
    def all(cls):
        return [tweet for tweet in cls.all_query()]

    @classmethod
    def all_dicts(cls):
        return [tweet.json_object() for tweet in cls.all_query()]

    def json_object(self):
        return vars(self)["_data"]

    @classmethod
    def count(cls):
        return Tweet.select().count()

    @classmethod
    def top(cls):
        tweets = (cls.select().order_by(Tweet.order).limit(1))
        if not tweets:
            return None
        return tweets.first()

    @classmethod
    def pop(cls):
        tweet = cls.top()
        if not tweet:
            return None
        tweet.remove()
        return tweet

    @classmethod
    def move(cls, from_index, to_index):
        if from_index == to_index:
            return None

        count = cls.count()
        if from_index > count or to_index > count:
            return None

        tweet = (cls.select()
                 .where(cls.order == from_index)
                 .limit(1)
                 .first())
        if not tweet:
            return None

        is_moving_down = from_index > to_index

        if is_moving_down:
            first_index_selection_query = cls.order < from_index
            second_index_selectionquery = cls.order >= to_index
        else:
            first_index_selection_query = cls.order > from_index
            second_index_selectionquery = cls.order <= to_index

        increment = 1 if is_moving_down else -1

        update_query = (cls.update(order=(Tweet.order + increment))
                        .where(first_index_selection_query)
                        .where(second_index_selectionquery))
        update_query.execute()

        tweet.order = to_index
        tweet.save()
        return tweet

    def remove(self):
        number_deleted = self.delete_instance()
        if number_deleted == 0:
            return None
        update_query = (self.update(order=(Tweet.order - 1))
                        .where(Tweet.order > self.order))
        update_query.execute()
        return self

    @classmethod
    def for_id(cls, id):
        try:
            return cls.get(id=id)
        except Tweet.DoesNotExist:
            return None

    @classmethod
    def remove_with_id(cls, id):
        tweet = cls.for_id(id)
        if not tweet:
            return None
        return tweet.remove()


Tweet.create_table(True)
