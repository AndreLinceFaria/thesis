import itertools,operator

def accumulate(l):
    it = itertools.groupby(sorted(l), operator.itemgetter(0))
    for key, subiter in it:
       yield key, sum(item[1] for item in subiter)

def get_max(l):
    mx = max(l, key=operator.itemgetter(1))
    return mx