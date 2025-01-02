import pandas as pd
from tqdm import tqdm
import numpy as np
import concurrent.futures
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed
from utils.inference_helpers import log_message, generate_gpt_response
from utils.prompt_helpers import gen_prompt_attr

split = 'train'

df = pd.read_pickle(f'outputs/neat/wikiqa_{split}_answers_paths20_relevantGPTpaths.pkl')


idx = df['idx'].tolist()
input_sentences = df['ip_sentences'].tolist()
relevant_triplets = df['relevant_triplets'].tolist()



def run_gpt_attribution(input_sentence, valid_triplets):   
    prompt = gen_prompt_attr(input_sentence, valid_triplets)
    generated_text = generate_gpt_response(prompt)
    return prompt, generated_text

max_threads = 5

inputDict = {}
outputDict = {}

with concurrent.futures.ThreadPoolExecutor(max_workers=max_threads) as executor:
    for i in tqdm(range(len(input_sentences))):
        input_sentence = input_sentences[i]
        valid_triplets = relevant_triplets[i]
        idx_value = idx[i]

        inputDict[idx_value] = (input_sentence, valid_triplets)
        future = executor.submit(run_gpt_attribution, input_sentence, valid_triplets)

        
        try:
            # Get result of future
            result = future.result()
            outputDict[idx_value] = result
        except Exception as exc:
            print(f'Generated an exception: {exc}')
            log_message(f'Generated an exception: {exc}')
        
        if (i+1) % 10 == 0:
            # np.save(f'outputs/parse_relevant_gpt_wikiqa_{split}_temp.npy', parse_relevant_gpt)
            np.save(f'outputs/neat/wikiqa_{split}_gpt4attr_inputDict.npy', inputDict)
            np.save(f'outputs/neat/wikiqa_{split}_gpt4attr_outputDict.npy', outputDict)
            # print("Saved temp file!")
            log_message(f"Saved temp file at index {i+1}/{len(df)}!")

np.save(f'outputs/neat/wikiqa_{split}_gpt4attr_inputDict.npy', inputDict)
np.save(f'outputs/neat/wikiqa_{split}_gpt4attr_outputDict.npy', outputDict)

print(f"Saved final file with size {len(df)}!")
log_message(f"Saved final file with size {len(df)}!")

