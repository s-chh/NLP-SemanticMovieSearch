import nltk


def PtoS(p):
    lines = nltk.tokenize.sent_tokenize(p)
    sentences = [item.strip() for item in lines]
    return (sentences)
