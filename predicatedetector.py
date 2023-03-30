import spacy
import json 
from antecedents import antecedents
from predicates import predicates
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_md")

antMatcher = PhraseMatcher(nlp.vocab)
predMatcher = PhraseMatcher(nlp.vocab)
antPatterns = [nlp.make_doc(term) for term in antecedents]
predPatterns = [nlp.make_doc(term) for term in predicates]
antMatcher.add("prelist", antPatterns)
predMatcher.add("predlist", predPatterns)

#doc = nlp("Greenhouse gasses have been thought to cause climate change")
#doc = nlp("Climate change has been thought to have been caused by greenhouse gasses")
# doc = nlp("Scientists believe  that co2 causes climate change")
#doc = nlp("Scientists believe that climate change is caused by  carbon dioxide")
doc = nlp("Scientists have been thought to believe that climate change is caused by  carbon dioxide")
antMatches = antMatcher(doc)
predMatches = predMatcher(doc)

data = []
ants = []
jsn = {}

for mid, start, end in antMatches:
  jsn['strt'] = start
  jsn['enx'] = end
  foo = doc[start:end]
  jsn['txt'] = str(foo)
  ants.append(jsn)
  jsn = {}
data.append(ants)

preds = []
jsn = {}
for mid, start, end in predMatches:
  jsn['strt'] = start
  jsn['enx'] = end
  foo = doc[start:end]
  jsn['txt'] = str(foo)
  preds.append(jsn)
  jsn = {}
data.append(preds)

print("DID: ",data)
