import os
from dotenv import load_dotenv
import openai

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

openai_client = openai.OpenAI(
    api_key=openai_api_key,
)

if openai_api_key is None:
    raise ValueError("OpenAI API key not found in .env file")

with open("input.md", "r") as file:
    input_md_content = file.read()

with open("chatgpt-preprompt.md", "r") as file:
    preprompt_content = file.read()

with open("system.txt", "r") as system_file:
    system_prompt = system_file.read()

with open("prompt.md", "r") as prompt_file:
    user_input = prompt_file.read()

# Concatenate the contents
combined_content = input_md_content + "\n" + preprompt_content + "\n" + user_input


messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": combined_content},
]
# Send the concatenated content to the model `gpt-4o`
response = openai_client.chat.completions.create(model="gpt-4o", messages=messages)

# Print the model's response
txt = response.choices[0].message.content
print(txt.strip())
with open("output.md", "w") as output_file:
    output_file.write(txt)
