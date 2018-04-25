import pymongo

db = pymongo.MongoClient().MovieDB


def bulk_insert(movieSemantics):
    var = db.movie.insert_many(
        [{'root': movieSemantics[i][0], 'properties': movieSemantics[i][1], 'weight': movieSemantics[i][2],
          'movie': movieSemantics[i][3]}
         for i in range(len(movieSemantics))])


def delete_all():
    # db.movie.bulk_write([pymongo.DeleteMany({})])
    return


def find(v, movies):
    filtered = []
    result = db.movie.find({"verbs": v, "movie": {"$in": movies}})
    for document in result:
        filtered.append(document)
    return filtered


def find2(r, movies):
    filtered = []
    result = db.movie.find({"root": r, "movie": {"$in": movies}})
    for document in result:
        filtered.append(document)
    return filtered


def recordCount():
    return db.movie.count()


def getAll():
    filtered = []
    result = db.movie.find({})
    for document in result:
        filtered.append(document)
    return filtered


def printAll():
    semantics = getAll()
    for semantic in semantics:
        print(semantic)

# printAll()
