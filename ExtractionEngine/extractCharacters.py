from Helper import AllfilesInFolder
import json
from stanfordcorenlp import StanfordCoreNLP
from tqdm import tqdm

def getCharacterNames(plot,nlpServer_Port):
    nlp = StanfordCoreNLP('http://localhost', port=nlpServer_Port)
    characters = []
    result = nlp.annotate(plot, properties={'annotators': 'ner', 'outputFormat': 'json', "ner.useSUTime": "0"})
    json_data = json.loads(result)
    json_data = json_data['sentences']
    for sentence in json_data:
            tokens = sentence['tokens']
            full_Name = ""
            for token in tokens:
                if token['ner'] == 'PERSON':
                    full_Name+=" "+ (token['word'])
                else:
                    if (len(full_Name)):
                        characters.append(full_Name.strip().lower())
                        full_Name = ""
            if (len(full_Name)):
                characters.append(full_Name.strip().lower())
    return (list(set(characters)))

def extractMovieCharacersfromDB(nlpServer_Port):
    dataFolder = "Data\Plots"
    plotFiles = AllfilesInFolder.getAllFilesInFolder(dataFolder)
    characters = []
    print ("Extracting characters from plots")
    for movie in tqdm(plotFiles):
        f = open(dataFolder+"/"+movie, 'r')
        plot = f.read()
        allCharacters = getCharacterNames(plot,nlpServer_Port)
        movieChar = {"movieTitle": movie,"characters": ",".join(allCharacters)}
        characters.append(movieChar)
        f.close()
    r = json.dumps(characters)
    f = open('Data\Characters\Characters.txt', 'w')
    f.write(r)
    f.close()
    print ("Characters file successfully created")