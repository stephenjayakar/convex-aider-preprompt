"""can you write a python program that
* reads input.md
* reads chatgpt-preprompt.md
* asks the user for an input
* concats them
* gets the openai key from .env
* sends them to model `gpt-4o` via the openai api
"""

import os
from dotenv import load_dotenv
import openai

# Load your OpenAI API key from the .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# Validate that the API key exists
if openai_api_key is None:
    raise ValueError("OpenAI API key not found in .env file")

# Read input.md
with open('input.md', 'r') as file:
    input_md_content = file.read()

# Read chatgpt-preprompt.md
with open('chatgpt-preprompt.md', 'r') as file:
    preprompt_content = file.read()

# Ask the user for an input
user_input = input("Please enter your input: ")

# Concatenate the contents
combined_content = input_md_content + "\n" + preprompt_content + "\n" + user_input

# Setup OpenAI API client
openai.api_key = openai_api_key

# Send the concatenated content to the model `gpt-4o`
response = openai.Completion.create(
    model="gpt-4o",
    prompt=combined_content,
    max_tokens=500  # Adjust the number of tokens as needed
)

# Print the model's response
print(response.choices[0].text.strip())
