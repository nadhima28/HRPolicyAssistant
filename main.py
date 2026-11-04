import os
from dotenv import load_dotenv
from anthropic import Anthropic

load_dotenv()

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

with open("Policy.txt", "r") as file:
    policy = file.read()

system_prompt = f"""You are an HR assistant.
Answer ONLY using the policy below.
If the answer is not in the policy, say "I don't know."

{policy}"""
def ask(question):
    response = client.messages.create(
        model="claude-haiku-4-5",
        max_tokens=200,
        system=system_prompt,
        messages=[{"role": "user", "content": question}]
)
    return response.content[0].text
