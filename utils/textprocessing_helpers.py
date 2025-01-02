import spacy_universal_sentence_encoder
import spacy
import neuralcoref
from utils.woolnet_pipe import get_woolnet_paths
from wiki_helpers import getWikiInfo, prepare_candidates, retrieveTriplets


nlp = spacy.load('en_core_web_sm')
# Add neural coref to SpaCy's pipe
neuralcoref.add_to_pipe(nlp)


def resolve_coreference(ip_text):
    doc = nlp(ip_text)
    op_text = str(doc._.coref_resolved)
    return op_text

def get_rel_paths(ip_text):
    wikient = getWikiInfo(ip_text)
    candidates = prepare_candidates(wikient)
    paths_all = []
    for i in range(len(candidates)):
        cand = candidates[i]
        paths = get_woolnet_paths(cand[0], cand[1])
        paths_all.append(paths)
    return paths_all, wikient

def preprocess(ip_text):
    ip_coref = resolve_coreference(ip_text)
    paths, wikients = get_rel_paths(ip_coref)
    return paths, wikients

def semantic_similarity(sentence1, sentence2):
    # Load the medium English model

    # Process the sentences
    doc1 = nlp(sentence1)
    doc2 = nlp(sentence2)

    # Compute and return the similarity
    return doc1.similarity(doc2)

def filter_relevant_entities(ipSentence, wikient):
    relevant_wikient = []
    for i in range(len(wikient)):
        sentence1 = ipSentence
        sentence2 = wikient[i][2]
        similarity_score = semantic_similarity(sentence1, sentence2)
        if similarity_score > 0:    
            relevant_wikient.append(wikient[i])

    return relevant_wikient

