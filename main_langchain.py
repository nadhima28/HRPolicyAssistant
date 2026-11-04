from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

with open("policy.txt", "r") as file:
    policy = file.read()

# 1. Chat model
model = ChatAnthropic(model="claude-haiku-4-5", max_tokens=200)

# 2. Prompt template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an HR assistant. Answer ONLY using the policy below. "
               "If the answer is not in the policy, reply with exactly: I don't know.\n\n{policy}"),
    ("user", "{question}")
])

# 3. Output parser
parser = StrOutputParser()

# The chain
chain = prompt | model | parser

def ask(question):
    return chain.invoke({"policy": policy, "question": question})

print(ask("how are you?"))