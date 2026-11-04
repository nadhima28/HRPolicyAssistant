from langchain_core.tools import tool
from dotenv import load_dotenv
from langchain.agents import create_agent
from main_rag import retriever

load_dotenv()

@tool
def get_leave_balance(employee_name: str) -> str:
    """Get the remaining vacation days for an employee."""
    balances = {"nadhiya": 12, "ravi": 5}
    days = balances.get(employee_name.lower())
    if days is None:
        return "Employee not found."
    return f"{employee_name} has {days} vacation days left."

@tool
def search_policy(question: str) -> str:
    """Search the company leave policy document to answer questions about leave rules."""
    docs = retriever.invoke(question)
    #print(docs)
    return "\n\n".join(doc.page_content for doc in docs)

agent = create_agent(
    model="anthropic:claude-haiku-4-5",
    tools=[get_leave_balance, search_policy],
    system_prompt="You are a helpful HR assistant. Use tools when needed. Only state what the policy explicitly says. If the policy does not mention something, say it is not covered in the policy and suggest contacting HR.",
)

'''result = agent.invoke(
    {"messages": [{"role": "user", "content": "How many sick days do full time employees get"}]}
    print(result["messages"][-1].content)
)'''
while True:
    question = input("Ask a question (or type quit): ")
    if question.lower() == "quit":
        break
    result = agent.invoke(
        {"messages": [{"role": "user", "content": question}]}
    )
    print(result["messages"][-1].content)

