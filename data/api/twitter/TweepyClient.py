import tweepy

consumer_key = "uEIEwhUCqELdY1vd7lxBTdglE"
consumer_secret = "obLlVTjKYEU9cRcyEw6otgJyUJGqn2nJXsKdLO0uvi7WYFDJvs"
access_token = "910185708928761856-uBqFLLKn0EXLm0pWzpxbzb7CqBXR4Ih"
access_token_secret = "71KXRZtO8oTDFhh4jxTLwLeM1C2yjMsAUlNcGxzovTDS8"

class TweepyClient():

    locations = [
        {'Name': 'Lisbon', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Leiria', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Santarem', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Setubal', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Beja', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Faro', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Evora', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Portalegre', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Castelo Branco', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Guarda', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Coimbra', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Aveiro', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Viseu', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Braganca', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Vila Real', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Porto', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Braga', 'lat': '', 'lon': '', 'area':''},
        {'Name': 'Viana do Castelo', 'lat': '', 'lon': '', 'area':''},
    ]

    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(self.auth)



if __name__ == "__main__":
    client = TweepyClient()
    users = client.api.search_users(q="geocode:39.673370,-8.283691,306km AND lang:pt", page=2)
    print(len(users))
    for user in users:
        print(user.id)