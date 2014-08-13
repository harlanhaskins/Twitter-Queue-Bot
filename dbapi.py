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

        updateQuery = (cls.update(order=(cls.order + 1))
                            .where(cls.order >= index))
        updateQuery.execute()

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
        tweets = (cls
                .select()
                .order_by(Tweet.order)
                .limit(1))
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
    def move(cls, fromIndex, toIndex):
        if fromIndex == toIndex:
            return None

        count = cls.count()
        if fromIndex > count or toIndex > count:
            return None

        tweet = (cls.select()
                    .where(cls.order == fromIndex)
                    .limit(1)
                    .first())
        if not tweet:
            return None

        movingDown = fromIndex > toIndex

        if (movingDown):
            firstIndexSelectionQuery = cls.order < fromIndex
            secondIndexSelectionQuery = cls.order >= toIndex
        else:
            firstIndexSelectionQuery = cls.order > fromIndex
            secondIndexSelectionQuery = cls.order <= toIndex

        increment = 1 if movingDown else -1

        updateQuery = (cls.update(order=(Tweet.order + increment))
                          .where(firstIndexSelectionQuery)
                          .where(secondIndexSelectionQuery))
        updateQuery.execute()

        tweet.order = toIndex
        tweet.save()
        return tweet

    def remove(self):
        numberDeleted = self.delete_instance()
        if numberDeleted == 0:
            print("None deleted")
            return None
        updateQuery = (self.update(order=(Tweet.order - 1))
                           .where(Tweet.order > self.order))
        updateQuery.execute()
        return self

    @classmethod
    def remove_with_id(cls, id):
        tweet = cls.select().where(cls.id == id).first()
        print(tweet)
        if not tweet:
            return None
        return tweet.remove()

Tweet.create_table(True)
