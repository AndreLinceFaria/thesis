from parsers import ParserCSV, ParserJSON

results = '././files/autarquicas17-resultados.csv'
config = '././files/parties-config/parties-config-1.json'


class ResultsParser():

    def __init__(self, filenameResults = results, filenameConfig = config):
        self.pconfig = PartiesConfig(filenameConfig)
        self.parser = ParserCSV(results)
        self.results = []
        self.setup()

    def setup(self):
        for config in self.pconfig.configs:
            camaras = config.labelname
            listParties = []
            votos, votantes, presidentes, maiorias, concelhos, mandatos = 0,0,0,0,0,0
            for party in config.parties:
                row = self.parser.getRow(colname='CAMARAS', colvalue=party)
                #print("Party: " + row['CAMARAS'] + " Votos: " + row['VOTOS'])
                votos += float(row['VOTOS'].strip("%"))
                votantes += int(row['VOTANTES'])
                presidentes += int(row['PRESIDENTES'])
                maiorias += int(row['MAIORIAS ABSOLUTAS'])
                concelhos += int(row['CONCELHOS CONCORREU'])
                mandatos += int(row['MANDATOS'])
                listParties.append(party)
            self.results.append(
                Result(camaras,votos,votantes,presidentes,maiorias,concelhos,mandatos, listParties)
            )

        totalVotos = 0
        for result in self.results:
            totalVotos+=result.votos

        for result in  self.results:
            result.votosRecalc = result.votos / float(totalVotos)


class Result():
    def __init__(self,camaras,votos, votantes, presidentes,maiorias, concelhos, mandatos, listParties):
        self.camaras = camaras #label
        self.votos = votos
        self.votantes = votantes
        self.presidentes = presidentes
        self.maiorias = maiorias
        self.concelhos = concelhos
        self.mandatos = mandatos
        self.listParties = listParties
        self.votosRecalc = -1

class PartiesConfig():

    def __init__(self, filename=config):
        self.parser = ParserJSON(filename)
        self.configs = []
        self.setup()

    def setup(self):
        conf = self.parser.getJsonData()
        for obj in conf:
            label = obj['label']
            parties = []
            for party in obj['parties']:
                parties.append(party)
            self.configs.append(
                Config(label, parties)
            )

class Config():
    def __init__(self, labelname, parties):
        self.labelname = labelname
        self.parties = parties

    def hasParty(self, party):
        if party in self.parties:
            return True
        return False

    def getLabel(self):
        return self.labelname

    def getParties(self):
        return self.parties



