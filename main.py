from data.utils.parserUtil import ResultsParser

resultsParser = ResultsParser(filenameResults='files/autarquicas17-resultados.csv', filenameConfig='files/parties-config/parties-config-1.json')

for result in resultsParser.results:
    print("Partido: " + result.camaras + " Votos: " + str(round(result.votosRecalc*100, 3)) + "%")