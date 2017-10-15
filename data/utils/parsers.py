import csv

class ParserCSV():
    def __init__(self, file):
        self.file = file

    def setFile(self, file):
        self.file=file

    def getRow(self,colname, colvalue, index=-1):
        with open(self.file,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for i,row in enumerate(reader):
                if row[colname] == colvalue and index<0:
                    #print("found at index: " + str(i))
                    return row
                elif i==index:
                    return row

    def getRowEntry(self,colname,colvalue,fetchcol=''):
        row = self.getRow(colname, colvalue)
        value = lambda x: fetchcol if x!='' else colname
        return row[value(fetchcol)]

    def getRows(self):
        with open(self.file,'r') as csvfile:
            reader = csv.DictReader(csvfile)
            list = []
            for row in reader:
                list.append(row)
            return list

    def prettyPrint(self,data):
        pprint(data)

import json
from pprint import pprint

class ParserJSON():
    def __init__(self, file):
        self.file = file

    def setFile(self, file):
        self.file=file

    def getJsonData(self):
        with open(self.file) as data_file:
            data = json.load(data_file)
            return data

    def prettyPrint(self,data):
        pprint(data)