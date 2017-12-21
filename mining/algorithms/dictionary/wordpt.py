import requests, json, re
import unidecode as ud
import Stemmer

class ClientWNPT():
    def __init__(self, base_url="http://wordnet.pt/api/"):
        self.base_url = base_url
        self.regexp_pt = r'(por)(-)(\d+)(-)'

    def __make_request(self,request_url):
        res = requests.get(request_url)
        return json.loads(res.text)

    def __get_sysnsets_for_word(self,word):
        url = self.base_url + "por/search/" + word
        data = self.__make_request(url)
        return data

    def __get_words_from_synset(self,synset):
        url = self.base_url + "por/synset/" + re.sub(self.regexp_pt, '', str(synset))
        data = self.__make_request(url)
        return data

    def get_synonyms(self,word):
        synsets = self.__get_sysnsets_for_word(word)
        res = []
        for synset in synsets:
            words = self.__get_words_from_synset(synset)
            res.extend(words)
        return [ud._unidecode(el) for el in list(set(res))]

class StemmerPT():

    def __init__(self, lang='portuguese'):
        self.stemmer = Stemmer.Stemmer(lang)

    def stem_word(self, word):
        return self.stemmer.stemWord(word)

    def stem_word_list(self,word_list):
        return list(set(self.stemmer.stemWords(word_list)))