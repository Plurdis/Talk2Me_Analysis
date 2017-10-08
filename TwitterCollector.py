import tweepy
twitter_consumer_key = '9raJaaJY9eY9qXcLomZLfHrNa'
twitter_consumer_secret = 'teVkhJrBrIOWRSfMMSq54a6GcXYuhRZgIyVRv4354TB8UNnwtu'
twitter_access_token = '907903860408172544-qIroyTkGvqW3wQrIO1rmuFaT1qDnHCf'
twitter_access_token_secret = 'D28j2o7hWx4vA7SRC3Fhj2vql7YAr455i03PqMdX71CXe'


class TwitterCollector:

    def test(self):
        auth = tweepy.OAuthHandler(twitter_consumer_key,
                                   twitter_consumer_secret)
        auth.set_access_token(twitter_access_token,
                              twitter_access_token_secret)

        # try:
        #     redirect_url = auth.get_authorization_url()
        #     print(redirect_url)
        # except tweepy.TweepError:
        #     print('Error! Failed to get request token.')

        api = tweepy.API(auth)

        # user = api.get_user('uutak2000')

        # print(user.screen_name)
        # print(user.followers_count)

        public_tweets = api.home_timeline()

        for tweet in public_tweets:
            print(type(tweet))
            print(tweet.text)
            # twitter.com/anyuser/status/915715643990790145
            print(tweet.id_str)
            print(tweet.created_at)

if __name__ == '__main__':
    tc = TwitterCollector()

    tc.test()

