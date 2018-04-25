import json, numpy
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from Helper import AllfilesInFolder
from textblob import TextBlob as tb
from stanfordcorenlp import StanfordCoreNLP
from tqdm import tqdm

def tf(word, blob):
    return blob.words.count(word) / len(blob.words)

def n_containing(word, bloblist):
    return sum(1 for blob in bloblist if word in blob.words)

def idf(word, bloblist):
    return numpy.log(len(bloblist) / (1 + n_containing(word, bloblist)))

def tfidf(word, blob, bloblist):
    return tf(word, blob) * idf(word, bloblist)

lem = WordNetLemmatizer()
sw = set(stopwords.words('english'))

def getVerbs(q,nlpServer_Port):
    verbs = []
    nlp = StanfordCoreNLP('http://localhost', port=nlpServer_Port)
    result = nlp.annotate(q, properties={'annotators': 'pos,lemma', 'outputFormat': 'json', "ner.useSUTime": "0"})
    json_data = json.loads(result)
    json_data = json_data['sentences']
    for sentence in json_data:
        tokens = sentence['tokens']
        for token in tokens:
            if str(token['pos']).startswith("V"):
                verbs.append(token['lemma'])
    return verbs

def extractVerbsFromDB(nlpServer_Port):
    movies = AllfilesInFolder.getAllFilesInFolder('Data\Plots\\')
    print ("Extracting events from plots")
    for movie in tqdm(movies):
        r = open('Data\Plots\\'+movie,'r')
        plot = r.read()
        r.close()
        verbs = getVerbs(plot,nlpServer_Port)
        w = open('Data\Event\AllVerbs\\'+movie,'w')
        w.writelines(["%s " % vb for vb in verbs])
        w.close()

def extractTfidFromDB():
    movies = AllfilesInFolder.getAllFilesInFolder('Data\Event\AllVerbs\\')
    rawDocs = []
    print ("Building TF-IDF for the events")
    for movie in movies:
        r = open('Data\Event\AllVerbs\\' + movie, 'r')
        q = r.read()
        rawDocs.append(tb(q))
        r.close()
    i = 0
    for doc in tqdm(rawDocs):
        scores = {word: tfidf(word, doc, rawDocs) for word in doc.words}
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        Tf_Score = []
        for word, score in sorted_words[:]:
            if score>0.00001:
                Tf_Score.append({"Event": word, "Score": round(score, 5)})
        w = open('Data\Event\TFIDF\\' + movies[i], 'w')
        Tf_json = json.dumps(Tf_Score)
        w.write(Tf_json)
        w.close()
        i += 1
    print ("Event files successfully created")

def extractEventsFromDB(nlpServer_Port):
    extractVerbsFromDB(nlpServer_Port)
    extractTfidFromDB()
