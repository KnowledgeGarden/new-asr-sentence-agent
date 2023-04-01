import spacy
import json 
from antecedents import antecedents
from predicates import predicates
from spacy.matcher import PhraseMatcher
nlp = spacy.load("en_core_web_md")
import spacy_dbpedia_spotlight
nlp.add_pipe('dbpedia_spotlight')
# Note: opentapioca is not all that accurate
# plus which the repo uses the wrong api URL
#nlx = spacy.blank('en')
#nlx.add_pipe('opentapioca')

antMatcher = PhraseMatcher(nlp.vocab)
predMatcher = PhraseMatcher(nlp.vocab)
antPatterns = [nlp.make_doc(term) for term in antecedents]
predPatterns = [nlp.make_doc(term) for term in predicates]
antMatcher.add("prelist", antPatterns)
predMatcher.add("predlist", predPatterns)

def handleGet(json):
  txt = json['text']
  print(txt)
  doc = nlp(txt)
  #DBpedia
  dbps = []
  for ent in doc.ents:
    txt = ent.text 
    kid = ent.kb_id_
    dbp = ent._.dbpedia_raw_result['@similarityScore']
    dbps.append((txt, kid, dbp))
  #Wikidata
  
  #wdx = nlx(txt)
  wkds = []
  
  #for edx in wdx.ents:
  #  txt = edx.text
  #  kid = edx.kb_id_
  #  lbl = edx.label_
  #  dsc = edx._.description
  #  wkds.append((txt, kid, lbl,dsc))

  #Predicates
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
  
  return {'data':data, 'dbp':dbps, 'wkd':wkds}