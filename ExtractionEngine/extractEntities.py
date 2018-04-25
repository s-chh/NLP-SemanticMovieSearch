from Helper import AllfilesInFolder
import json
from stanfordcorenlp import StanfordCoreNLP
from tqdm import tqdm

def getEntities(query,nlpServer_Port):
    nlp = StanfordCoreNLP('http://localhost', port=nlpServer_Port)
    result = nlp.annotate(query, properties={'annotators': 'ner', 'outputFormat': 'json', "ner.useSUTime": "0"})
    json_data = json.loads(result)
    json_data = json_data['sentences']
    entities = []
    for sentence in json_data:
        tokens = sentence['tokens']
        for token in tokens:
            if token['ner']=='O' and str(token['pos']).startswith("N"):
                entities.append(token['lemma'])
    return (list(set(entities)))

def extractEntitiesFromDB(nlpServer_Port):
    dataFolder = "Data\Plots"
    plotFiles = AllfilesInFolder.getAllFilesInFolder(dataFolder)
    movieEntities = []
    print ("Extracting Entites from plots")
    for movie in tqdm(plotFiles):
        f = open(dataFolder + "/" + movie, 'r')
        plot = f.read()
        Entities_list=getEntities(plot,nlpServer_Port)
        Entities_list = Entities_list
        Entities = {"movieTitle": movie, "Entities": ",".join(Entities_list)}
        movieEntities.append(Entities)
        f.close()
    r = json.dumps(movieEntities)
    f = open("Data\Entities\Entities.txt", "w")
    f.write(str(r))
    f.close
    print("Entity file successfully created")