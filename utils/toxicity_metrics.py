from detoxify import Detoxify

with open('utils/nsfw_wordslist.txt', 'r', encoding='utf-8') as file:
    bad_words_set =  [line.strip() for line in file if line.strip()]

def compute_social_metrics(utterance):
    """
    Compute the social metrics for an utterance using the detoxify package
    Returns the toxicity score
    """
    res = Detoxify('original').predict(utterance)
    return res



def contains_bad_words(input_sentence):
    """
    Check if the input sentence contains any bad words.
    
    Parameters:
    - bad_words_set: a set of bad words for efficient search.
    - input_sentence: the sentence to check.
    
    Returns:
    - True if the input sentence contains any bad words, False otherwise.
    """
    # Normalize the sentence: lowercase and split into words
    words_in_sentence = input_sentence.lower().split()
    
    # Check each word in the sentence against the set of bad words
    for word in words_in_sentence:
        if word in bad_words_set:
            print(input_sentence)
            return True  # Found a bad word
        
    return False  # No bad words found

