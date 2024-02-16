
from openai import AzureOpenAI
import pandas as pd
from dotenv import dotenv_values
from tqdm import tqdm
import numpy as np
import time
import concurrent.futures
import datetime
import pandas as pd
from concurrent.futures import ThreadPoolExecutor, as_completed

secrets = dotenv_values(".env")
personal_api_key = secrets['AZURE_OPENAI_KEY']
azure_endpoint = secrets['AZURE_OPENAI_ENDPOINT']

client = AzureOpenAI(
  azure_endpoint = azure_endpoint, 
  api_key=personal_api_key,  
  api_version="2023-05-15"
)

split = 'train'

df = pd.read_pickle(f'outputs/neat/wikiqa_{split}_answers_paths20_relevantGPTpaths.pkl')


idx = df['idx'].tolist()
input_sentences = df['ip_sentences'].tolist()
relevant_triplets = df['relevant_triplets'].tolist()

def log_message(message, log_file=f'logs/distillGPT_{split}_log.txt'):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_message = f"[{timestamp}] {message}\n"
    
    with open(log_file, 'a') as file:
        file.write(formatted_message)
    return

def generate_gpt_response(prompt, retries=5, wait_time=2):
    attempt = 0
    while attempt < retries:
        try:
            response = client.chat.completions.create(
                model="gpt4_preview",  # model = "deployment_name".
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": f"{prompt}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Attempt {attempt + 1} failed with error: {e}")
            if attempt < retries - 1:
                print(f"Retrying in {wait_time * attempt} seconds...")
                time.sleep(wait_time * attempt)
            else:
                print("All attempts failed. Returning None.")
                log_message(f"Failed to generate GPT response for prompt: {prompt}, due to error: {e}")
                return None
        finally:
            attempt += 1

def gen_prompt(input_sentence, valid_triplets):
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


# Define a function that will be executed in parallel
def run_gpt_attribution(input_sentence, valid_triplets):   
    prompt = gen_prompt(input_sentence, valid_triplets)
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

