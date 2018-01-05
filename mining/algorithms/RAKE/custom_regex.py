from settings import *
import re

from utils.timeouts import exit_after

@exit_after(TIMEOUT_RAKE)
def custom_regex(filename=REGEX_FILE):
    regext = []
    for line in open(filename):
        if line.strip()[0:1] != "#": # comment character
            for word in line.split():  # in case more than one per line
                regext.append(word)
    return regext

@exit_after(TIMEOUT_RAKE)
def remove_regex(text):
    try:
        tmp = text
        for regex in custom_regex():
            tmp = re.sub(re.compile(regex), '', tmp)
        return tmp
    except Exception as e:
        logm.info("Exception in remove_regex: " + str(e))
        return None