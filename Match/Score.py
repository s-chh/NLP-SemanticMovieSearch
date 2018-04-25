import json
from Helper import AllfilesInFolder, MongoDB
from nltk.corpus import wordnet as wn


def matchCharacters(allMovies, query_characters):
    mFolder = "Data\Characters"
    mFile = str(AllfilesInFolder.getAllFilesInFolder(mFolder)[0])
    f = open(mFolder + '/' + mFile, 'r')
    allMovieCharacters = json.loads(f.read())

    score = [0] * len(allMovies)
    if len(query_characters) == 0:
        return score
    for movie in allMovieCharacters:
        movie_chars = movie["characters"]
        movie_chars = movie_chars.split(",")
        for query_char in query_characters:
            for movie_char in movie_chars:
                if (query_char in movie_char):
                    score[allMovies.index(movie["movieTitle"])] += 1
                    print("Character '" + query_char + "' found in " + movie["movieTitle"])
                    break
    return (score)


def matchEntities(allMovies, query_entities, threshold):
    mFolder = "Data\Entities"
    mFile = str(AllfilesInFolder.getAllFilesInFolder(mFolder)[0])
    f = open(mFolder + '/' + mFile, 'r')
    allMovieEntities = json.loads(f.read())

    score = [0] * len(allMovies)
    if len(query_entities) == 0:
        return score

    for query_entity in query_entities:
        for movie in allMovieEntities:
            movie_entities = movie["Entities"]
            movie_entities = movie_entities.split(",")
            en_score = 0
            for movie_entity in movie_entities:
                a1 = wn.synsets(movie_entity)
                a2 = wn.synsets(query_entity)
                try:
                    sim = a1[0].wup_similarity(a2[0])
                    if sim > en_score:
                        en_score = sim
                except:
                    pass
            if en_score >= threshold:
                score[allMovies.index(movie["movieTitle"])] += en_score
                print("Entity '" + query_entity + "' found in " + movie["movieTitle"])

    return (score)


def matchNE(allMovies, query_NEs):
    mFolder = "Data\\NE"
    mFile = str(AllfilesInFolder.getAllFilesInFolder(mFolder)[0])
    f = open(mFolder + '/' + mFile, 'r')
    allMovieNE = json.loads(f.read())

    score = [0] * len(allMovies)
    if len(query_NEs) == 0:
        return score
    for movie in allMovieNE:
        movie_NEs = movie["NE"]
        movie_NEs = movie_NEs.split(",")
        for query_NE in query_NEs:
            for movie_NE in movie_NEs:
                if (query_NE in movie_NE):
                    score[allMovies.index(movie["movieTitle"])] += 1
                    print("NE '" + query_NE + "' found in " + movie["movieTitle"])
                    break
    return (score)


def matchEvent(allMovies, queryEvents, threshold):
    score = [0] * len(allMovies)
    mFolder = "Data\Event\TFIDF"
    mFiles = AllfilesInFolder.getAllFilesInFolder(mFolder)
    for idx, mFile in enumerate(mFiles):
        print("Movie: " + mFile)
        f = open(mFolder + '/' + mFile, 'r')
        allMovieEvents = json.loads(f.read())
        for queryEvent in queryEvents:
            eScore = []
            for movieEvent in allMovieEvents:
                mEvent = movieEvent["Event"]
                a1 = wn.synsets(mEvent)
                a2 = wn.synsets(queryEvent)
                try:
                    sim = a1[0].wup_similarity(a2[0])
                    if sim >= threshold:
                        eScore.append(round(sim, 5))
                    else:
                        eScore.append(0)
                except:
                    eScore.append(0)

            if len(eScore) > 0:
                max_value = max(eScore)
                if max_value > 0:
                    max_index = eScore.index(max_value)
                    print("       Event = '" + queryEvent + "' matched with '" + allMovieEvents[max_index][
                        'Event'] + "'. " + "Similarity Score:" + str(max_value) + "     Tf-Idf Score:" + str(
                        allMovieEvents[max_index]['Score']))
                    score[idx] += allMovieEvents[max_index]['Score'] * max_value
                else:
                    print("       No matches found for Event = '" + queryEvent + "'")
            else:
                print("       No Events were found in the movie")
    return score


def matchSemantics(allMovies, query_semantics, filtered_movies, threshold):
    movie_score = [0.0] * len(allMovies)
    for idx, query_semantic in enumerate(query_semantics):
        semantic_score = [0.0] * len(allMovies)
        matching_semantics = MongoDB.find2(query_semantic.root.lower(), allMovies)
        q_properties = query_semantic.properties
        # print ()
        # print (query_semantic.toString())
        for matching_semantic in matching_semantics:
            # print (matching_semantic)
            m_properties = matching_semantic['properties']
            m_score = 0
            for q_property in q_properties.keys():
                if q_property in m_properties.keys():
                    property_score = 0
                    for q_attribute in q_properties[q_property]:
                        for m_attribute in m_properties[q_property]:
                            a1 = wn.synsets(q_attribute)
                            a2 = wn.synsets(m_attribute)
                        try:
                            sim = a1[0].wup_similarity(a2[0])
                            if sim >= threshold:
                                property_score = max(sim, property_score)
                        except:
                            pass
                    m_score += property_score
            m_score = m_score / query_semantic.weight
            if m_score > 0:
                print("Semantic " + str(idx + 1) + " found in " + matching_semantic["movie"] + " score = " + str(m_score))
                semantic_score[allMovies.index(matching_semantic["movie"])] = max(semantic_score[allMovies.index(matching_semantic["movie"])], m_score)
        for i in range(len(allMovies)):
            movie_score[i] += semantic_score[i]

    return (movie_score)
