import re, os

from utils.timeouts import exit_after

dir_path = os.path.dirname(os.path.realpath(__file__))
regexFile = str(dir_path) + '\/regex.txt'

regexs = [
    r"^\\s+[A-Za-z,;'\"\\s]+[.?!]$",
    r"http \S+|https \S+|http\S+",
    r"pic.twitter\S+|youtube.com\S+|twitter.com\S+|bit.ly\S+|goo.gl\S+|youtu.be\S+"
]

def custom_regex(filename=regexFile):
    regext = []
    for line in open(filename):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                regext.append(word)
    return regext

@exit_after(10)
def remove_regex(text):
    try:
        tmp = text
        for regex in custom_regex():
            tmp = re.sub(re.compile(regex), '', tmp)
    except Exception as e:
        print("Exception in remove_regex: " + str(e))
        tmp = None
    return tmp