from django.test import TestCase
from django.contrib.auth import get_user_model

from rest_framework.test import APIClient

from .models import Tweet

User = get_user_model()


class TweetTestCase(TestCase):
    """
    Test suite for our Tweet API
    """
    def setUp(self):
        self.user = User.objects.create_user(username='cfe', password='somepassword')
        self.userb = User.objects.create_user(username='cfe2', password='somepassword2')
        Tweet.objects.create(content="my tweet 1", user=self.user)
        Tweet.objects.create(content="my tweet 2", user=self.user)
        Tweet.objects.create(content="my tweet 3", user=self.userb)


    def test_user_created(self):
        user = User.objects.get(username='cfe')
        self.assertEqual(user.username, 'cfe')


    def test_tweet_created(self):
        tweet = Tweet.objects.create(content="my tweet 4", user=self.user)
        self.assertEqual(tweet.id, 4)
        self.assertEqual(tweet.user, self.user)


    def get_client(self):
        client = APIClient()
        client.login(username=self.user.username, password='somepassword')
        return client


    def test_tweet_list(self):
        # we created these at the setup, test that they exist
        client = self.get_client()
        response = client.get("/api/tweets/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 3)


    def test_action_like(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 1, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)


    def test_action_unlike(self):
        client = self.get_client()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "like"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 1)

        response = client.post("/api/tweets/action/", {"id": 2, "action": "unlike"})
        self.assertEqual(response.status_code, 200)
        like_count = response.json().get('likes')
        self.assertEqual(like_count, 0)


    def test_action_retweet(self):
        client = self.get_client()
        current_count = Tweet.objects.all().count()
        response = client.post("/api/tweets/action/", {"id": 2, "action": "retweet"})
        self.assertEqual(response.status_code, 201)
        data = response.json()
        new_tweet_id = data.get("id")
        self.assertNotEqual(new_tweet_id, 2)
        self.assertEqual(current_count+1, Tweet.objects.all().count())

    def test_tweet_create_api_view(self):
        data = {'content': "this is my test tweet"}
        client = self.get_client()
        current_count = Tweet.objects.all().count()
        response = client.post("/api/tweets/create/", data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(current_count+1, Tweet.objects.all().count())
        
    def test_tweet_detail_api_view(self):
        client = self.get_client()
        response = client.get("/api/tweets/1/")
        self.assertEqual(response.status_code, 200)
        _id = response.json().get("id")
        self.assertEqual(_id, 1)
    
    def test_tweet_delete_api_view(self):
        client = self.get_client()
        response = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response.status_code, 200)
        client = self.get_client()
        response_after_deleted = client.delete("/api/tweets/1/delete/")
        self.assertEqual(response_after_deleted.status_code, 404)

        # the userb was the one that created tweet # 3
            # this client is logged in as the original user
        response_incorrect_owner = client.delete("/api/tweets/3/delete/")
        self.assertEqual(response_incorrect_owner.status_code, 401)


