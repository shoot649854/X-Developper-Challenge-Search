
import os
import datetime
from openai import OpenAI
from dotenv import load_dotenv
import os
import re


load_dotenv()

openai_client = OpenAI(
    organization="org-1EDbnzjdGhFGeAAiDIyKSyc6",
)
pplx_client = OpenAI(api_key=os.getenv('PPLX'), base_url="https://api.perplexity.ai")

def remove_leading_number(text):
    # Find the index of the first space character
    index_of_space = text.find(' ')
    if index_of_space != -1:
        # Remove the leading number by slicing the string from the character after the space
        return text[index_of_space+1:].strip()
    else:
        # If no space is found, return the original text
        return text.strip()
    
def clean_keywords(keywords, search_term):
    intent_instructions = """
    **ONLY RETURN A PYTHON LIST**
    So you've been given a search term {search_term} and you already have data on some of the latest events, companies, teams, individuals, etc involved directly with this.
    Your job is to fill the given information into a python list. Even if the keyword is a phrase, it should be a single string in the list, so break it up into relevant parts. I need names on the latest events, companies, teams, individuals, etc involved directly with this.
    Do not include long summaries or descriptions.
    
    {keywords}
    
    Remember you're only supposed to return a python list""" 
    
    sys_prompt = intent_instructions.format(
        keywords=str(keywords),
        search_term=search_term
    )
    chat_completion = openai_client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": sys_prompt,
            }],
        model="gpt-4",
    )
    return chat_completion.choices[0].message.content

def clean_results(string):
    results = string.split('results:')[1]
    keywords = results.split('\n')
    return [remove_leading_number(key.strip()) for key in keywords if key != '']



def get_subqueries(query):
    messages = [
    {
        "role": "system",
        "content": (
            "Your goal is to return real-time/latest information/description on the user's query, today's date is" + str(datetime.datetime.now()).split()[0]
        )
    },
    {
        "role": "user",
        "content":f"""Generate me 5-7 context-based keywords in a list for the search_term:'{query}'
        
        I need names on the latest events, companies, teams, individuals, etc involved directly with this, every term in a new line
        
        Here's example:
        'search_term':Lok Sabha Elections
        results:
        BJP vs Congress
        Congress Party India
        Bhartiya Janta Party
        Narendra Modi
        """,
    },
    ]
    # chat completion without streaming
    response = pplx_client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
        
    return eval(clean_keywords(response.choices[0].message.content, query))
    # try:
    #     return clean_results(response.choices[0].message.content)
    # except:
    #     return eval(clean_keywords(response.choices[0].message.content))
    

def get_description(query):
    messages = [
    {
        "role": "system",
        "content": (
            "Your goal is to return a 3-4 line real-time/latest information/description on the user's query, for context, today's date is" + str(datetime.datetime.now()).split()[0]
        )
    },
    {
        "role": "user",
        "content":query,
    },
    ]
    # chat completion without streaming
    response = pplx_client.chat.completions.create(
        model="mistral-7b-instruct",
        messages=messages,
    )
    return response.choices[0].message.content