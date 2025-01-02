from openai import AzureOpenAI
from dotenv import dotenv_values
import datetime
import time


secrets = dotenv_values(".env")
personal_api_key = secrets['AZURE_OPENAI_KEY']
azure_endpoint = secrets['AZURE_OPENAI_ENDPOINT']

client = AzureOpenAI(
  azure_endpoint = azure_endpoint, 
  api_key=personal_api_key,  
  api_version="2023-05-15"
)

def log_message(message, log_file=f'logs/distillGPT_log.txt'):
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