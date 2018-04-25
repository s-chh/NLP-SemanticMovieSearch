from Helper import AllfilesInFolder
import json
from stanfordcorenlp import StanfordCoreNLP
from tqdm import tqdm

def getNE(plot,nlpServer_Port):
    nlp = StanfordCoreNLP('http://localhost', port=nlpServer_Port)
    NE = []
    result = nlp.annotate(plot, properties={'annotators': 'ner', 'outputFormat': 'json', "ner.useSUTime": "0"})
    json_data = json.loads(result)
    json_data = json_data['sentences']
    tagType = ''
    NE_Chunk = ""
    for sentence in json_data:
        tokens = sentence['tokens']
        for token in tokens:
            if token['ner']==tagType:
                NE_Chunk = NE_Chunk + " " + token['word']
            else:
                if (len(NE_Chunk)):
                    NE.append(NE_Chunk.strip().lower().replace(","," "))
                    tagType = ""
                    NE_Chunk = ""

                if (token['ner'] != 'O'):
                    NE_Chunk = token['word']
                    tagType = token['ner']
        if (len(NE_Chunk)):
            NE.append(NE_Chunk.strip().lower().replace(",", " "))
    return list(set(NE))


def extractNEFromDB(nlpServer_Port):
    dataFolder = "Data\Plots"

    plotFiles = AllfilesInFolder.getAllFilesInFolder(dataFolder)

    all_NE = []
    print ("Extracting NE from plots")
    for movie in tqdm(plotFiles):
        f = open(dataFolder+"/"+movie, 'r')
        plot = f.read()
        allNE = getNE(plot,nlpServer_Port)
        trunc_NE = []
        for NE in allNE:
            if not (NE in trunc_NE):
                trunc_NE.append(NE)
        NE = {"movieTitle": movie,"NE": ",".join(trunc_NE)}
        all_NE.append(NE)
        f.close()
    r = json.dumps(all_NE)
    f = open("Data\\NE\MovieNE.txt", "w")
    f.write(r)
    f.close()
    print ("NE file successfully created")