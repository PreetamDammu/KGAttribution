def gen_prompt_attr(input_sentence, valid_triplets):
    prompt = f'''
    Label the claims or statements in the following text as “Attributable”, “Contradictory”, or “Exploratory” by evaluating it against the provided triplets.
    Provide rationale for the prediction. 

    “Attributable” means that the sentence can be supported by the triplets
    “Contradictory” means that the sentence can be refuted by the triplets, and 
    “Exploratory” means that the triplets can neither support nor refute the sentence.

    Input sentence: {input_sentence}

    Valid triplets: {valid_triplets}

    Return only the relevant paths. If there are no relevant paths, return "No relevant paths". More than one path may be relevant.
    Generate an explanation for the selected relational path.


    Format your output as: *text_span* #prediction# [Triplet(s), rationale].
    '''

    return prompt.replace('    ', '')