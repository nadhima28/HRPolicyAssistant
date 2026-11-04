from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

load_dotenv()

# --- Setup (runs once): split, embed, store ---
with open("policy.txt", "r") as file:
    policy = file.read()

# 1. Split: cut the policy into small chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=300, chunk_overlap=30)
chunks = splitter.split_text(policy)

# 2. Embed + 3. Store: turn chunks into vectors and keep them in memory
embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001")
vector_store = InMemoryVectorStore.from_texts(chunks, embeddings)

# Retriever: finds the 2 closest chunks for a question
retriever = vector_store.as_retriever(search_kwargs={"k": 2})

# --- The chain (same as before) ---
model = ChatAnthropic(model="claude-haiku-4-5", max_tokens=200)

prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an HR assistant. Answer ONLY using the policy below. "
               "If the answer is not in the policy, reply with exactly: I don't know.\n\n{policy}"),
    ("user", "{question}")
])

parser = StrOutputParser()
chain = prompt | model | parser

# --- Ask: retrieve first, then answer ---
def ask(question):
    docs = retriever.invoke(question)
    context = "\n\n".join(doc.page_content for doc in docs)
    print("Retrieved Chunks: \n", context, "\n")
    return chain.invoke({"policy": context, "question": question})
if __name__ == "__main__":
    print(ask("How many sick days do I get as a contractor?"))

