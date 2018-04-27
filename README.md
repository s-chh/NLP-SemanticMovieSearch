# NLP-SemanticMovieSearch

Dependencies:
Requires Knowledge Parser, StanfordCoreNLP and MongoDB


1. Knowledge Parser: Download Link for KnowledgeParser: https://github.com/arpit7123/K-Parser-JAR

Absolute path needs to be configured in extractSemantics.py, line 5

Check the readme file for properly configuring KnowledgeParser

2. StanfordCoreNLP:Download Link for Knowledge Parser: https://stanfordnlp.github.io/CoreNLP/

Absolute path needs to be configured in Main.py, line 10

3. Running MongoDB Server

Run buildDB function on the first run to extract Entity-Mention relationships from the data and store it in MongoDB
