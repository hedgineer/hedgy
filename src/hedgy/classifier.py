import openai
import os
import json

from dotenv import load_dotenv
from functools import lru_cache


load_dotenv()
open_api = os.getenv("OPENAI_API_KEY")

def classify(text: str, model="gpt-3.5-turbo"):
    
    classifier_prompts = generate_classifier_prompts()
    user_message = [
        {
            'role': 'user', 
            "content": f"Classify this prompt:\n{text}"
        }
    ]
    # return classifier_prompts + user_message
    response = openai.ChatCompletion.create(
        model=model,
        messages=classifier_prompts + user_message,
        temperature=0
    )
    
    return response.choices[0]['message']['content']

# @lru_cache(maxsize=None)
def load_prompt_data(prompt_file: str) -> dict:
    '''
    Reads the promts from the data files and returns a dictionary
    '''

    current_dir = os.path.dirname(os.path.realpath(__file__))
    grand_parent_dir = os.path.dirname(os.path.dirname(current_dir))
    prompts_path = os.path.join(grand_parent_dir, "data", prompt_file)

    with open(prompts_path) as f:
        return json.load(f)['prompts']
    
def generate_classifier_prompts(classifier_prompts="classifier_prompts.json") -> list:
    '''
    Generates the classifier prompts and returns a list of messages
    '''

    prompt_data = load_prompt_data(prompt_file=classifier_prompts)
    prompts = []

    system_promt = """
    You are a classification engine that classifies prompts into the {category_count} categories as follows:

    {model_list}

    Follow these rules for each category defintion:

    {rules}
    """.format(
        category_count = (len(prompt_data) + 1),
        model_list="\n".join(i['name'] for i in prompt_data),
        rules="\n".join(i['instructions'] for i in prompt_data)
    )

    prompts.append({"role": "system", "content": system_promt})
    for i in prompt_data:
        for e in i['examples']:
            prompts.append({
                'role': 'user',
                'content': f"Classify this prompt:\n{e}"
                
            })
            prompts.append({
                'role': 'assistant',
                'content': i['name']
            })   

    return prompts
