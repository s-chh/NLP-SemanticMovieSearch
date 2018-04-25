from Helper import  ParagraphToSentences, AllfilesInFolder, MongoDB, SemanticClass
import jpype as jp
from tqdm import tqdm

kparser_path = "E:\Documents\ASU\CSE_576_NLP\Project\KParser\kparser.jar"

try:
    x = jp.startJVM(jp.get_default_jvm_path(), "-ea",
                "-Djava.class.path=%s" % kparser_path)
except:
    pass
classLoader = jp.java.lang.ClassLoader.getSystemClassLoader()
mgClass = jp.JClass("module.graph.MakeGraph")


def splitNodevalue(value):
    currentNodeValueTokens = value.split("-")
    return currentNodeValueTokens[0]

def classExits(srTemp, semanticRoles):
    for semanticRole in semanticRoles:
        if srTemp.root == semanticRole.root and srTemp.properties == semanticRole.properties:
            return True
    return False

def sematic_extraction(nd, semanticRoles):
    edgeList = nd.getEdgeList()
    children = nd.getChildren()
    properties = {}
    root = splitNodevalue(nd.getValue())
    if (nd.isAnEntity() or nd.isAnEvent()) and len(children)>1:
        for i in range(len(children)):
            if edgeList.get(i) == "instance_of":
                root = children.get(i).getValue().lower()
            else:
                value = splitNodevalue(children.get(i).getValue()).lower()
                if edgeList.get(i) == "semantic_role":
                    value = value[1:]
                if edgeList.get(i) in properties.keys():
                    properties[edgeList.get(i)].append(value)
                else:
                    properties[edgeList.get(i)] = [value]
        srTemp = SemanticClass.SemanticData(root=root, isEntity=nd.isAnEntity(), isEvent=nd.isAnEvent(),
                                               properties=properties)
        if not classExits(srTemp,semanticRoles):
            semanticRoles.append(srTemp)
    for i in range(children.size()):
        if (children.get(i).isAnEntity() or children.get(i).isAnEvent()):
            sematic_extraction(children.get(i),semanticRoles)
    return semanticRoles


def semanticRoleSimilarity(lines):
    semanticRoles = []

    for line in lines:
        try:
            mg = mgClass()
            graphs = mg.createGraphUsingSentence(line, False, True, False)
            it = graphs.iterator()
            while (it.hasNext()):
                nd = it.next().getGraphNode()
                semanticRoles = sematic_extraction(nd, semanticRoles)
        except:
             print("Error in line " + str(line))
    for semanticRole in semanticRoles:
        semanticRole.setWeight()
    return semanticRoles


def extractSemanticFromDB():
    dataFolder = "Data\Plots"

    plotFiles = AllfilesInFolder.getAllFilesInFolder(dataFolder)
    MongoDB.delete_all()
    print("Extracting semantics roles from plots")
    for movie in tqdm(plotFiles):
        f = open(dataFolder + "/" + movie, 'r')
        plot = f.read()
        f.close()
        sentences = ParagraphToSentences.PtoS(plot)
        semantics = semanticRoleSimilarity(sentences)
        semanticsMongo = []
        for semantic in semantics:
            r = semantic.root
            p = semantic.properties
            w = semantic.weight
            semanticsMongo.append([r,p,w, movie])
        MongoDB.bulk_insert(semanticsMongo)
        print(str(MongoDB.recordCount()) + " semantic roles present in DB")

def extractSemanctic(query):
    sentences = ParagraphToSentences.PtoS(query)
    semantics = semanticRoleSimilarity(sentences)
    for semantic in semantics:
        semantic.setWeight()
    return semantics