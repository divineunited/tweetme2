from django.conf import settings
from rest_framework import serializers

from .models import Tweet

MAX_TWEET_LENGTH = settings.MAX_TWEET_LENGTH
TWEET_ACTION_OPTIONS = settings.TWEET_ACTION_OPTIONS

class TweetActionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    action = serializers.CharField()
    content = serializers.CharField(allow_blank=True, required=False)

    def validate__action(self, value):
        value = value.lower().strip()
        if not value in TWEET_ACTION_OPTIONS:
            raise serializers.ValidationError("This is not a valid action for tweets.")
        return value


class TweetCreateSerializer(serializers.ModelSerializer):
    """
    Serializer used to serialize created tweets
    """
    likes = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes']
    
    def get_likes(self, obj):
        return obj.likes.count()
    
    def validate_content(self, value):
        if len(value) > MAX_TWEET_LENGTH:
            raise serializers.ValidationError("This tweet is too long.")
        return value


class TweetSerializer(serializers.ModelSerializer):
    """
    Serializer used to serialize tweets for read only purposes. 
    To serialize the data coming back to the client
    """
    likes = serializers.SerializerMethodField(read_only=True)

    # using another version of the TweetCreateSerializer to pass the serialized parent 
    parent = TweetCreateSerializer(read_only=True)

    class Meta:
        model = Tweet
        fields = ['id', 'content', 'likes', 'is_retweet', 'parent']
    
    # to use the above serializer method fields, we define them as follows:
    def get_likes(self, obj):
        return obj.likes.count()
