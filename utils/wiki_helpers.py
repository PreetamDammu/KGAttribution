import spacy
from SPARQLWrapper import SPARQLWrapper, JSON
import pandas as pd
from itertools import combinations
from wikidata.client import Client
import numpy as np

# initialize language model
nlp = spacy.load("en_core_web_md")

# add wiki entity linker pipeline
nlp.add_pipe("entityLinker", last=True)

#Linking Wikidata SPARQL endpoint
sparql = SPARQLWrapper("https://query.wikidata.org/sparql")

#CHANGE BEFORE RUNNING ACCORDING TO SPLIT
# split = 'test' 
# split = 'validation' 
split = 'train' 

wiki_id_map = np.load(f'outputs/qid_to_label_map_{split}_wikiqa.npy', allow_pickle=True).item()

def getWikiInfo(textIp):
    '''
    Returns all relevant information from Wikidata KG for identified Wiki entities in a given sentence
    '''
    entInf = []
    doc = nlp(textIp)
    # returns all entities in the whole document
    all_linked_entities = doc._.linkedEntities

    for i in range(len(all_linked_entities)):
        ent = all_linked_entities[i]
        label = ent.get_label()
        wikiId = ent.get_id()
        desc = ent.get_description()
        text_span = str(ent.get_span())

        entInf.append([label, wikiId, desc, text_span])
    return entInf

def prepare_candidates(wikiEntList):
    '''
    Return the list of candidate tuples that may have links in the KG
    '''
    # QIDs = ['Q{}'.format(ent[1]) for ent in wikiEntList]
    QIDs = [ent[1] for ent in wikiEntList]

    directLinkCandidates = list(combinations(QIDs, 2))

    directLinkCandidates_reverse = []
    for candidate in directLinkCandidates:
        directLinkCandidates_reverse.append(candidate[::-1])
    directLinkCandidates = directLinkCandidates + directLinkCandidates_reverse

    return directLinkCandidates

def extractQID(uri):
    return uri.split('/')[-1]

def get_label_for_qid(qid):
    try:
        client = Client()
        entity = client.get(qid, load=True)
        label = str(entity.label)
        return label
    except Exception as e:
        # print(f"Error: {str(e)}")
        return None

def getLabelsForTripletNums(triplet):

    subjQID = f'Q{triplet[0]}'
    predicateQID = f'P{triplet[1]}'
    objQID = f'Q{triplet[2]}'

    try:
        subjLabel = get_label_for_qid(subjQID)
        predicateLabel = get_label_for_qid(predicateQID)
        objLabel = get_label_for_qid(objQID)
    except Exception as e:
        #print(f"Error: {str(e)}")
        return None

    tripletNames = (subjLabel, predicateLabel, objLabel)
    return tripletNames

def getLabelsForTripletNums_fromDictMap(triplet):

    subjQID = f'Q{triplet[0]}'
    predicateQID = f'P{triplet[1]}'
    objQID = f'Q{triplet[2]}'

    try:
        subjLabel = wiki_id_map[subjQID]
        predicateLabel = wiki_id_map[predicateQID]
        objLabel = wiki_id_map[objQID]
    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    tripletNames = (subjLabel, predicateLabel, objLabel)
    return tripletNames

def get_label_for_qid_fromDictMap(node):

    nodeQID = f'Q{node}'

    try:
        nodeLabel = wiki_id_map[nodeQID]

    except Exception as e:
        print(f"Error: {str(e)}")
        return None

    
    return nodeLabel

def format_relational_paths(nested_list):
    paths_desc_list = []
    formatted_string = ""
    relational_paths_dict = {}
    for i, path_list in enumerate(nested_list, start=1):
        path_key = f"Relational Path {i}"
        formatted_path = ", ".join([f"('{source}', '{relation}', '{target}')" for source, relation, target in path_list])
        formatted_string += f"Relational Path {i}: [{formatted_path}]"
        if i < len(nested_list):
            formatted_string += "\n "
        paths_desc_list.append(formatted_path)
        relational_paths_dict[path_key] = path_list
    return formatted_string, relational_paths_dict

    
def getLabelsForTriplets(tripletDict):
    listOfTriplets_qid = []
    listOfTriplets_label = []

    for i in range(len(tripletDict['subject.value'])):
        subjQID = extractQID(tripletDict['subject.value'][i])
        predicateQID = extractQID(tripletDict['predicate.value'][i])
        objQID = extractQID(tripletDict['object.value'][i])

        subjLabel = get_label_for_qid(subjQID)
        predicateLabel = get_label_for_qid(predicateQID)
        objLabel = get_label_for_qid(objQID)

        listOfTriplets_qid.append((subjQID, predicateQID, objQID))
        listOfTriplets_label.append((subjLabel, predicateLabel, objLabel))

    return listOfTriplets_qid, listOfTriplets_label

def retrieveTriplets(candidates):
    listOfTriplets_qids = []
    listOfTriplets_labels = []

    for i in range(len(candidates)):
        candidate = candidates[i]
        obj_qid = candidate[0]
        subj_qid = candidate[1]

        sparql_query = """
        SELECT ?subject ?predicate ?object
        WHERE {
            BIND(wd:OBJ_QID as ?subject)
            BIND(wd:SUBJ_QID as ?object)
            ?subject ?predicate ?object.
        }
        """

        sparql_query = sparql_query.replace('OBJ_QID', obj_qid)
        sparql_query = sparql_query.replace('SUBJ_QID', subj_qid)

        try:
            sparql.setQuery(sparql_query)
            sparql.setReturnFormat(JSON)
            results = sparql.query().convert()
        except Exception as e:
            print("SPARQL query error: {}".format(e))
            continue

        if len(results['results']['bindings'])<1:
            # print("nothing found")
            continue

        results_df = pd.json_normalize(results['results']['bindings'])
        tripletDict = results_df[['subject.value', 'object.value', 'predicate.value']].to_dict()

        listOfTriplets_qid, listOfTriplets_label = getLabelsForTriplets(tripletDict)

        listOfTriplets_qids = listOfTriplets_qids + listOfTriplets_qid
        listOfTriplets_labels = listOfTriplets_labels + listOfTriplets_label

    return listOfTriplets_qids, listOfTriplets_labels

