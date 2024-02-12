import spacy_universal_sentence_encoder


# load one of the models: ['en_use_md', 'en_use_lg', 'xx_use_md', 'xx_use_lg']
nlp = spacy_universal_sentence_encoder.load_model('en_use_lg')

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
