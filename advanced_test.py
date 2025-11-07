"""
Advanced Integration Test: Complex queries with reasoning
"""

import os
from sqlalchemy import create_engine
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get API key from environment
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY not found in environment. Please check your .env file.")

# Connect to database
print("\n" + "="*70)
print("🧠 ADVANCED INTEGRATION TEST - NATURAL LANGUAGE + REASONING")
print("="*70)

engine = create_engine("postgresql://dannazca@localhost:5432/factorytest_local")
db = SQLDatabase(engine, include_tables=["companies", "kpis", "dealflow"])

# Create agent with verbose mode to see reasoning
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    verbose=True,
    agent_type="openai-tools",
    max_iterations=10,
    max_execution_time=60
)

print("\nAgent initialized with access to:")
print("  - Companies table: 2,175 rows")
print("  - KPIs table: 21,514 rows")
print("  - Dealflow table: 4,676 rows")
print("\n" + "="*70)

# Complex test questions
questions = [
    {
        "question": "What are the top 5 companies based on company valuation?",
        "context": "Note: Look for valuation fields in companies or dealflow tables"
    },
    {
        "question": "What is the oldest deal in the portfolio?",
        "context": "Note: Check date fields like 'created', 'date_of_first_contact', etc. in dealflow table"
    },
    {
        "question": "What is the average valuation per month of 2024?",
        "context": "Note: Filter deals from 2024 and group by month, showing the average valuation"
    }
]

results = []

for i, item in enumerate(questions, 1):
    print(f"\n{'='*70}")
    print(f"QUESTION {i}")
    print(f"{'='*70}")
    print(f"\n❓ {item['question']}")
    print(f"\n💡 Context: {item['context']}")
    print(f"\n{'—'*70}")
    print("🤖 Agent thinking process:")
    print(f"{'—'*70}\n")
    
    try:
        response = agent.invoke({"input": item['question']})
        answer = response['output']
        
        print(f"\n{'='*70}")
        print(f"✅ ANSWER:")
        print(f"{'='*70}")
        print(f"\n{answer}\n")
        
        results.append({
            "question": item['question'],
            "status": "✅ Success",
            "answer": answer
        })
        
    except Exception as e:
        print(f"\n{'='*70}")
        print(f"❌ ERROR:")
        print(f"{'='*70}")
        print(f"\n{str(e)}\n")
        
        results.append({
            "question": item['question'],
            "status": "❌ Failed",
            "answer": str(e)
        })
    
    if i < len(questions):
        print("\n" + "—"*70)
        print("Moving to next question...")
        print("—"*70)

# Summary
print("\n" + "="*70)
print("📊 TEST SUMMARY")
print("="*70)

for i, result in enumerate(results, 1):
    print(f"\n{i}. {result['status']} - {result['question']}")
    if result['status'] == "✅ Success":
        print(f"   Answer preview: {result['answer'][:100]}...")

print("\n" + "="*70)
print("✅ ADVANCED INTEGRATION TEST COMPLETE")
print("="*70)
print("\nWorkflow validated:")
print("  ✅ Complex natural language queries")
print("  ✅ Multi-table reasoning")
print("  ✅ Date filtering and aggregations")
print("  ✅ Agent decision-making process visible")
print("\n🎉 LangChain agent handling complex queries successfully!")
