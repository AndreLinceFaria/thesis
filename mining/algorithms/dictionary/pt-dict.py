import requests, json

class ClientWNPT():
    def __init__(self, base_url="http://wordnet.pt/api/"):
        self.base_url = base_url

    def __make_request(self,request_url):
        res = requests.get(request_url)
        print(res)
        return json.loads(res.text)

    def get_sysnsets_for_word(self,word):
        url = self.base_url + "por/search/" + word
        data = self.__make_request(url)
        print(str(data))
        return data

    def get_word_from_synset(self,synset_id):
        url = self.base_url + "por/synset/" + str(synset_id)
        print(str(url))
        #data = self.__make_request(url)
        #print(str(data))

if __name__ == "__main__":
    client = ClientWNPT()
    synsets = client.get_sysnsets_for_word("comida")

    print(len(synsets))

    for syn in synsets:
        print(syn)
        client.get_word_from_synset(str(syn))