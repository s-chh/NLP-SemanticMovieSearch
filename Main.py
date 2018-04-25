from ExtractionEngine import extractCharacters, extractEntities, extractNER, extractEvents, extractSemantics
from Match import Score
from Helper import AllfilesInFolder
from PreProcessing import PreProcessing
from stanfordcorenlp import StanfordCoreNLP

threshold = 0.9
topPicksCount = 20

corenlppath = r'E:\Documents\ASU\CSE_576_NLP\Project\stanford-corenlp-full-2015-12-09'


def buildDB(nlpServer_Port):
    print()
    extractCharacters.extractMovieCharacersfromDB(nlpServer_Port)
    print()
    extractEntities.extractEntitiesFromDB(nlpServer_Port)
    print()
    extractEvents.extractEventsFromDB(nlpServer_Port)
    print()
    extractNER.extractNEFromDB(nlpServer_Port)
    print()
    extractSemantics.extractSemanticFromDB()
    print()
    print("DB Rebuild Complete")


def character_score(q, nlpServer_Port):
    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    # Characters
    print()
    query_characters = extractCharacters.getCharacterNames(q, nlpServer_Port)
    if len(query_characters) > 0:
        print("Characters identified in query: " + str(query_characters))
        characters_score = Score.matchCharacters(allMovies, query_characters)
    else:
        print("No characters identitifed in query")
        characters_score = [0] * len(allMovies)
    if len(query_characters) > 0:
        characters_score = [round(x / len(query_characters), 5) for x in characters_score]

    return characters_score


def entity_score(q, nlpServer_Port):
    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    # Entities
    print()
    query_entites = extractEntities.getEntities(q, nlpServer_Port)
    if len(query_entites) > 0:
        print("Entities identified in query: " + str(query_entites))
        entitiy_score = Score.matchEntities(allMovies, query_entites, threshold)
    else:
        print("No entities identitifed in query")
        entitiy_score = [0] * len(allMovies)
    if len(query_entites) > 0:
        entitiy_score = [round(x / len(query_entites), 5) for x in entitiy_score]
    return entitiy_score


def event_score(q, nlpServer_Port):
    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    # Events
    print()
    query_events = list(set(extractEvents.getVerbs(q, nlpServer_Port)))
    if len(query_events) > 0:
        print("Events identified in query: " + str(query_events))
        event_score = Score.matchEvent(allMovies, query_events, threshold)
    else:
        print("No events identified in query")
        event_score = [0] * len(allMovies)
    if len(query_events) > 0:
        event_score = [round(x / len(query_events), 5) for x in event_score]
    return event_score


def ner_score(q, nlpServer_Port):
    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    # NE
    print()
    query_ne = extractNER.getNE(q, nlpServer_Port)
    if len(query_ne) > 0:
        print("NE identified in query: " + str(query_ne))
        ne_score = Score.matchNE(allMovies, query_ne)
    else:
        print("No NE identified in query")
        ne_score = [0] * len(allMovies)
    if len(query_ne) > 0:
        ne_score = [round(x / len(query_ne), 5) for x in ne_score]

    return ne_score


def semantic_score(q):
    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    # Semantics
    query_semantics = extractSemantics.extractSemanctic(q)
    if len(query_semantics) > 0:
        print("Semantics found in query:")
        for idx, query_semantic in enumerate(query_semantics):
            print(str(idx + 1) + ". " + query_semantic.toString())
        s_score = Score.matchSemantics(allMovies, query_semantics, allMovies, threshold)
    else:
        print("No Semantics found in query")
        s_score = [0] * len(allMovies)
    if len(query_semantics) > 0:
        s_score = [round(x, 5) for x in s_score]

    return s_score


def ranking(allMovies, prob, k):
    print()
    tempProb = prob
    topPicks = []

    for i in range(k):
        max_value = max(tempProb)
        max_index = tempProb.index(max_value)
        topPicks.append(allMovies[max_index])
        print("Pick" + str(i + 1) + ": " + str(allMovies[max_index]) + "      Probability: " + str(max_value))
        tempProb[max_index] = -1
    return topPicks


def predict(q, nlpServer_Port):
    print()
    print("Query = " + q)

    allMovies = AllfilesInFolder.getAllFilesInFolder("Data\Plots")

    c_score = character_score(q, nlpServer_Port)
    en_score = entity_score(q, nlpServer_Port)
    ev_score = event_score(q, nlpServer_Port)
    ne_score = ner_score(q, nlpServer_Port)
    s_score = semantic_score(q)

    total_score = [0] * len(allMovies)
    print()
    print("Final Score:")
    for i in range(len(allMovies)):
        total_score[i] = round((c_score[i] + en_score[i] + ev_score[i] + ne_score[i] + s_score[i]), 5)
        print(allMovies[i] + "  Character Score: " + str(c_score[i]) + "  Entity Score: " + str(
            en_score[i]) + "  Event Score: " + str(ev_score[i]) + "  NE score: " + str(ne_score[i]) +
              "  Semantic score: " + str(s_score[i]) + "   Total Score: " + str(total_score[i]))
    norm_factor = sum(total_score)
    prob = [round(x / norm_factor, 5) if (norm_factor > 0) else norm_factor for x in total_score]
    topPicks = ranking(allMovies, prob, topPicksCount)
    return topPicks


def evaluate(queries, nlpServer_Port):
    top1accuracy = 0
    top5accuracy = 0
    top10accuracy = 0
    top15accuracy = 0
    top20accuracy = 0

    for i, query in enumerate(queries):
        q = PreProcessing.cleanUp(query[0])
        top20picks = predict(q, nlpServer_Port)
        top15picks = top20picks[:15]
        top10picks = top20picks[:10]
        top5picks = top20picks[:5]
        top1pick = top20picks[:1]

        print()
        print("Actual Movie = " + query[1])
        print()

        if query[1] in top20picks:
            top20accuracy += 1
            print("Top20:     Prediction = Correct  ", end="")
        else:
            print("Top20:     Prediction = Incorrect", end="")
        print("        Current Top20Accuracy = " + str(top20accuracy) + "/" + str(i + 1))

        if query[1] in top15picks:
            top15accuracy += 1
            print("Top15:     Prediction = Correct  ", end="")
        else:
            print("Top15:     Prediction = Incorrect", end="")
        print("        Current Top15Accuracy = " + str(top15accuracy) + "/" + str(i + 1))

        if query[1] in top10picks:
            top10accuracy += 1
            print("Top10:     Prediction = Correct  ", end="")
        else:
            print("Top10:     Prediction = Incorrect", end="")
        print("        Current Top10Accuracy = " + str(top10accuracy) + "/" + str(i + 1))

        if query[1] in top5picks:
            top5accuracy += 1
            print("Top5:      Prediction = Correct  ", end="")
        else:
            print("Top5:      Prediction = Incorrect", end="")
        print("        Current Top5Accuracy  = " + str(top5accuracy) + "/" + str(i + 1))

        if query[1] in top1pick:
            top1accuracy += 1
            print("Top1:      Prediction = Correct  ", end="")
        else:
            print("Top1:      Prediction = Incorrect", end="")
        print("        Current Top1Accuracy  = " + str(top1accuracy) + "/" + str(i + 1))

    top1accuracy = top1accuracy / len(queries)
    top5accuracy = top5accuracy / len(queries)
    top10accuracy = top10accuracy / len(queries)
    top15accuracy = top15accuracy / len(queries)
    top20accuracy = top20accuracy / len(queries)

    print()
    print("Top1 Accuracy of the system  = " + str(top1accuracy))
    print("Top5 Accuracy of the system  = " + str(top5accuracy))
    print("Top10 Accuracy of the system = " + str(top10accuracy))
    print("Top15 Accuracy of the system = " + str(top15accuracy))
    print("Top20 Accuracy of the system = " + str(top20accuracy))
    print()


def main():
    try:
        nlpServer = StanfordCoreNLP(corenlppath)
        nlpServer_Port = nlpServer.port

        # PreProcessing.cleanUpDB()
        # buildDB(nlpServer_Port)

        q = []

        q.append(["Father of a man suffers from Alzheimer disease", "ASeparation(2011)-Synopsis.txt"])
        q.append(["A man loves his father very much", "ASeparation(2011)-Synopsis.txt"])
        q.append(["Two police officers go to a federal mental hospital.", "ShutterIsland(2010)-Synopsis.txt"])
        q.append(["Police officers interview mental hospital staff and patients", "ShutterIsland(2010)-Synopsis.txt"])
        q.append(["A mental patient escapes from a federal mental hospital", "ShutterIsland(2010)-Synopsis.txt"])
        q.append(["A man's car is caught in flash flood and left abandoned", "IntotheWild(2007)-Synopsis.txt"])
        q.append(["A man donates all his savings and goes on a cross-country drive", "IntotheWild(2007)-Synopsis.txt"])
        q.append(["A man camps in alaska in an abandoned bus", "IntotheWild(2007)-Synopsis.txt"])
        q.append(["A man travels from Mexico to United States on foot.", "IntotheWild(2007)-Synopsis.txt"])
        q.append(["A girl decides to pursue her dream of becoming a boxer", "MillionDollarBaby(2004)-Synopsis.txt"])
        q.append(["A boxer suffers spinal injury", "MillionDollarBaby(2004)-Synopsis.txt"])
        q.append(["The trainer ends boxer's life", "MillionDollarBaby(2004)-Synopsis.txt"])
        q.append(["The boxer bites her tongue to die.", "MillionDollarBaby(2004)-Synopsis.txt"])
        q.append(["A girl had her memories erased.", "EternalSunshineoftheSpotlessMind(2004)-Synopsis.txt"])
        q.append(["The movie takes place in a man's brain", "EternalSunshineoftheSpotlessMind(2004)-Synopsis.txt"])
        q.append(["A girl steals a company's records and gives them to clients","EternalSunshineoftheSpotlessMind(2004)-Synopsis.txt"])
        q.append(["A dog goes to train station with his master everyday", "hachi.txt"])
        q.append(["The master of a dog dies at work.", "hachi.txt"])
        q.append(["A mobster collects protection money from a convenience store owner", "departed.txt"])
        q.append(["A policeman dates a psychiatrist", "departed.txt"])
        q.append(["A policeman is a criminal's informant.", "departed.txt"])
        q.append(["Hero was a marine", "marine.txt"])
        q.append(["Hero's wife is kidnapped and hero rescues her.", "marine.txt"])
        q.append(["The kidnappers rest at a shack.", "marine.txt"])
        q.append(["The main criminal gets badly-burned.", "marine.txt"])
        q.append(["The movie occurs in early 1800", "amadeus.txt"])
        q.append(["A man cuts his throat.", "amadeus.txt"])
        q.append(["A prince is changed into a monstor.", "BeautyandtheBeast(1991)-Synopsis.txt"])
        q.append(["Household objects welcome a man in a castle", "BeautyandtheBeast(1991)-Synopsis.txt"])
        q.append(["A monster fell in love with a girl", "BeautyandtheBeast(1991)-Synopsis.txt"])
        q.append(["The monster is badly injured at the end. ", "BeautyandtheBeast(1991)-Synopsis.txt"])

        evaluate(q, nlpServer_Port)

    finally:
        nlpServer.close()


if __name__ == '__main__':
    main()
