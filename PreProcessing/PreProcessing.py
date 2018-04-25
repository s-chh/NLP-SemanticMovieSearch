import re, contractions
from Helper import AllfilesInFolder
import unidecode

TAG_RE = re.compile('<.*?>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def remove_specialChar(text):
    return unidecode.unidecode(text)


def remove_whitespaces(text):
    return ' '.join(text.split())


def spaceAfterPeriod(text):
    return text.replace('.', '. ').replace(' .', '.')


def fix_contractions(query):
    return (contractions.fix(query))


def cleanUp(text):
    return fix_contractions(remove_whitespaces(spaceAfterPeriod(remove_specialChar(remove_tags(text)))))


def cleanUpDB():
    readFolder = "Data\RawPlots"
    writeFolder = "Data\Plots"

    movies = AllfilesInFolder.getAllFilesInFolder(readFolder)

    for movie in (movies):
        f = open(readFolder + "/" + movie, 'r', encoding="utf8")
        plot = f.read()
        f.close()
        cleanPlot = cleanUp(plot)
        if len(cleanPlot) > 0:
            w = open(writeFolder + "//" + movie, 'w')
            w.write(cleanPlot)
            w.close()
        else:
            print(movie + " is empty")
    print("Movie plots cleaned up successfully")
