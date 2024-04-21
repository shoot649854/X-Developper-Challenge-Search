import asyncio
import xai_sdk
import os
import json
from dotenv import load_dotenv
load_dotenv()
os.environ['XAI_API_KEY'] = os.getenv('XAI_API_KEY')

async def datatype_decision():
    client = xai_sdk.Client()
    sampler = client.sampler
    output = ""

    PREAMBLE = """\
This is a conversation between a human user and a highly intelligent AI. The AI's name is Grok and it makes every effort to truthfully answer a user's questions. It always responds politely but is not shy to use its vast knowledge in order to solve even the most difficult problems. The conversation begins.

Human: Based on the input, return what data type it would be. You can only return text, video/image, and number

Assistant: Understood! Please provide the input."""

    text = input("Write a message ")

    prompt = PREAMBLE + f"<|separator|>\n\nHuman: {text}<|separator|>\n\nAssistant: " + "{\n"
    # print(prompt)
    async for token in  sampler.sample(
        prompt=prompt,
        max_len=1024,
        stop_tokens=["<|separator|>"],
        temperature=0.5,
        nucleus_p=0.95):
        output += token.token_str
        # print(token.token_str, end="\n")
    print()
    return output

def format(input):
    if(input is None):
        return ""
    elif("text" in input):
        return "text"
    elif("video" in input):
        return "video"

if __name__ == '__main__':
    token_str = asyncio.run(datatype_decision())
    data_type = token_str.strip()
    print(format(data_type))
