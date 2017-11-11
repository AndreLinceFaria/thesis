import re, os

from utils.timeouts import exit_after

dir_path = os.path.dirname(os.path.realpath(__file__))
regexFile = str(dir_path) + '\/regex.txt'


def custom_regex(filename=regexFile):
    regext = []
    for line in open(filename):
        if line.strip()[0:1] != "#":
            for word in line.split():  # in case more than one per line
                regext.append(word)
    return regext

@exit_after(10)
def remove_regex(text):
    tmp = text
    for regex in custom_regex():
        tmp = re.sub(str(regex), '', tmp)
    return tmp