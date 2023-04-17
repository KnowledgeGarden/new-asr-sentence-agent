import spacy
import json 
from antecedents import antecedents
from predicates import predicates
from spacy.matcher import PhraseMatcher
from spacy.matcher import Matcher
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
conjMatcher = Matcher(nlp.vocab)
conjMatcher.add("ConJ", [[{"POS": "CCONJ","TEXT":"and" }],
                         [{"POS": "PUNCT", "TEXT":","}]])
disjMatcher = Matcher(nlp.vocab)

def handleGet(json):
  txt = json['text']
  print(txt)
  doc = nlp(txt)
  jsn = {}

  #DBpedia
  dbps = []
  for ent in doc.ents:
    jsn = {}
    jsn['strt'] = ent.text 
    jsn['kid'] = ent.kb_id_
    jsn['dbp'] = ent._.dbpedia_raw_result['@similarityScore']
    dbps.append(jsn)

  print('DBP', dbps)
  #Wikidata
  # ignoring for now
  
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
 
  for mid, start, end in antMatches:
    jsn = {}
    jsn['strt'] = start
    jsn['enx'] = end
    tok = doc[start:end]
    jsn['txt'] = tok.text 
    ants.append(jsn)
  print('ANTECENTS', ants)
  data.append(ants)

  preds = []
  jsn = {}
  for mid, start, end in predMatches:
    jsn = {}
    jsn['strt'] = start
    jsn['enx'] = end
    tok = doc[start:end]
    jsn['txt'] = tok.text
    preds.append(jsn)
  print('PREDICATES', preds)
  data.append(preds)

  #Nouns and verbs
  nmatcher = Matcher(nlp.vocab)
  nmatcher.add("Nouns", [[{"POS": "NOUN"}]])
  nns = nmatcher(doc)
  #print('FOO', nns)
  nnx = []
  pnmatcher = Matcher(nlp.vocab)
  pnmatcher.add("ProperNouns", [[{"POS": "PROPN"}]])
  pnns = pnmatcher(doc)
  #print('BAR', pnns)
  pnnx = []
  vmatcher = Matcher(nlp.vocab)
  vmatcher.add("Verbs", [[{"POS": "VERB"}]])
  vbs = vmatcher(doc)
  vbx = []
  #print('BAH', vbs)
  for mid, start, end in nns:
    tok = doc[start]
    jsn = {}
    jsn['strt'] = start
    jsn['txt'] = tok.text
    nnx.append(jsn)
 # print('NNN', nnx)
  for mid, start, end in pnns:
    tok = doc[start]
    jsn = {}
    jsn['strt'] = start
    jsn['txt'] = tok.text
    pnnx.append(jsn)
  #print('PNN', pnnx)
  for mid, start, end in vbs:
    tok = doc[start]
    jsn = {}
    jsn['strt'] = start
    jsn['txt'] = tok.text
    vbx.append(jsn)
  #print('VRB', vbx)
  #conjunctions
  conjX = conjMatcher(doc)
  conjM = []


  for mid, start, end in conjX:
    tok = doc[start]
    jsn = {}
    jsn['strt'] = start
    jsn['txt'] = tok.text
    conjM.append(jsn)
  #disjunctions
  disjX = disjMatcher(doc)
  disjM = []
  for mid, start, end in disjX:
    tok = doc[start]
    jsn = {}
    jsn['strt'] = start
    jsn['txt'] = tok.text
    disjM.append(jsn)
  return {'data':data, 'dbp':dbps, 'wkd':wkds, 
    'nns':nnx, 'pnns':pnnx, 'vrbs':vbx, 'conj':conjM, 'disj':disjM}