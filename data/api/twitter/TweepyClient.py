import tweepy

consumer_key = "uEIEwhUCqELdY1vd7lxBTdglE"
consumer_secret = "obLlVTjKYEU9cRcyEw6otgJyUJGqn2nJXsKdLO0uvi7WYFDJvs"
access_token = "910185708928761856-uBqFLLKn0EXLm0pWzpxbzb7CqBXR4Ih"
access_token_secret = "71KXRZtO8oTDFhh4jxTLwLeM1C2yjMsAUlNcGxzovTDS8"

class TweepyClient():

    locations = [
        {'Name': 'Lisbon', 'lat': '39.004245', 'lon': '-9.405670', 'radius':'46'},
        {'Name': 'Leiria', 'lat': '39.747850', 'lon': '-8.809662', 'radius':'19'},
        {'Name': 'Santarem', 'lat': '39.283294', 'lon': '-8.497925', 'radius':'50'},
        {'Name': 'Setubal', 'lat': '38.186387', 'lon': '-8.918152', 'radius':'64'},
        {'Name': 'Beja', 'lat': '37.779399', 'lon': '-7.816772', 'radius':'64'},
        {'Name': 'Faro', 'lat': '36.677231', 'lon': '-8.096924', 'radius':'100'},
        {'Name': 'Evora', 'lat': '38.561053', 'lon': '-7.866211', 'radius':'55'},
        {'Name': 'Portalegre', 'lat': '39.215231', 'lon': '-7.701416', 'radius':'55'},
        {'Name': 'Castelo Branco', 'lat': '39.922376', 'lon': '-7.514648', 'radius':'49'},
        {'Name': 'Guarda', 'lat': '40.663973', 'lon': '-7.218018', 'radius':'49'},
        {'Name': 'Coimbra', 'lat': '40.164182', 'lon': '-8.371582', 'radius':'44'},
        {'Name': 'Aveiro', 'lat': '40.726446', 'lon': '-8.585815', 'radius':'44'},
        {'Name': 'Viseu', 'lat': '40.755580', 'lon': '-7.877197', 'radius':'49'},
        {'Name': 'Braganca', 'lat': '41.475660', 'lon': '-6.844482', 'radius':'46'},
        {'Name': 'Vila Real', 'lat': '41.553811', 'lon': '-7.591553', 'radius':'40'},
        {'Name': 'Porto', 'lat': '41.205523', 'lon': '-8.426514', 'radius':'34'},
        {'Name': 'Braga', 'lat': '41.553811', 'lon': '-8.338623', 'radius':'34'},
        {'Name': 'Viana do Castelo', 'lat': '41.904321', 'lon': '-8.627014', 'radius':'36'},
    ]

    def __init__(self):
        self.auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = tweepy.API(self.auth)

    def get_user_names(self): #remove duplicates list(set(t))
        user_ids = []
        for dist in self.locations:
            print("District: " + dist['Name'])
            i=0
            while True:
                try:
                    users = self.api.search_users(q="geocode:"+dist['lat']+","+dist['lon']+","+dist['radius']+"km AND lang:pt", page=i)
                except Exception:
                    print("Exception caught.")
                    break
                if not len(users)>0:
                    break
                for user in users:
                    user_ids.append(user.screen_name)
                i+=1
        total_users = list(set(user_ids))
        print("Total users: " + str(len(total_users)))
        return total_users

if __name__ == "__main__":
    client = TweepyClient()
    client.get_user_names()
