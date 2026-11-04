# HR Policy Assistant

A small AI agent that answers employee leave questions from a company policy document.

## What it does
- Answers policy questions (vacation, sick leave, parental leave, holidays) using RAG over policy.txt
- Looks up an employee's remaining vacation balance using a tool (sample data)
- The agent decides which tool to use based on the question
- Says when something is not covered in the policy instead of guessing

## How it works
1. The policy is split into chunks (size 300, overlap 30)
2. Chunks are embedded with Gemini embeddings and stored in an in-memory vector store
3. A retriever returns the top 2 chunks for each question
4. A LangChain agent (Claude Haiku 4.5) has two tools: search_policy and get_leave_balance

## Files
- main.py: first version using the Anthropic SDK directly
- main_langchain.py: same idea as a LangChain chain
- main_rag.py: RAG pipeline (splitter, embeddings, vector store, retriever)
- main_agent.py: the agent with two tools
- test_main.py: pytest evals

## Setup
python -m venv .venv
source .venv/bin/activate
pip install anthropic python-dotenv langchain langchain-anthropic langchain-google-genai langchain-text-splitters pytest

Create a .env file with:
ANTHROPIC_API_KEY=your_key
GOOGLE_API_KEY=your_key

## Run
python main_agent.py
pytest test_main.py

## What I learned
- Exact string checks in evals are fragile (apostrophes broke a test), so I normalize text before checking
- When an answer was wrong, I printed the retrieved chunks to tell retrieval problems apart from generation problems
- The agent once claimed contractors aren't eligible for sick leave, which the policy never says. I fixed it by tightening the system prompt to state only what the policy says

## Next steps
- Connect the balance tool to a real HR API
- Add evals for the agent's tool choice
- Use a persistent vector store