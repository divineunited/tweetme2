import random
from django.conf import settings
from django.db import models

User = settings.AUTH_USER_MODEL


class TweetLike(models.Model):
    """
    This intermediary table defines the relationship between a user and the tweet it liked.
    It is a "through model" that adds a timestamp to the many to many field.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete=models.CASCADE) # if the model is defined below this, then need quotes
    timestamp = models.DateTimeField(auto_now_add=True)


class Tweet(models.Model):
    # Maps to SQL data
    # id = models.AutoField(primary_key=True) 
    # Parent is referencing itself "before it's defined" for retweeting
        # When the parent tweet is deleted, the retweet is just set to null
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.CASCADE) # one user can have many tweets
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike) # references above model
    content = models.TextField(blank=True, null=True)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-id']

    @property
    def is_retweet(self):
        return self.parent != None