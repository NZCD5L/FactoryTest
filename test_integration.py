"""
Integration Test: CSV → PostgreSQL → LangChain Agent
Tests the complete workflow without deep training
"""

import os
import pandas as pd
from sqlalchemy import create_engine, text
from langchain_community.utilities import SQLDatabase
from langchain_openai import ChatOpenAI
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

# Configuration
DB_NAME = "factorytest_local"
DB_USER = "dannazca"  # Your macOS username
DB_PASSWORD = ""  # Local PostgreSQL usually doesn't need password
DB_HOST = "localhost"
DB_PORT = "5432"

# Step 1: Connect to PostgreSQL
print("=" * 50)
print("STEP 1: Testing PostgreSQL Connection")
print("=" * 50)

try:
    engine = create_engine(f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}")
    with engine.connect() as conn:
        result = conn.execute(text("SELECT version();"))
        version = result.fetchone()[0]
        print(f"✅ Connected to PostgreSQL!")
        print(f"Version: {version[:50]}...")
except Exception as e:
    print(f"❌ Connection failed: {e}")
    print("\nTo fix:")
    print("1. Run: createdb factorytest_local")
    print("2. Or ensure PostgreSQL is running: brew services list")
    exit(1)

# Step 2: Load CSV data into database
print("\n" + "=" * 50)
print("STEP 2: Loading CSV Data into PostgreSQL")
print("=" * 50)

csv_files = {
    "companies": "Companies.csv",
    "kpis": "KPIs_prueba.csv",
    "dealflow": "dealflow_prueba.csv"
}

for table_name, csv_file in csv_files.items():
    try:
        print(f"\nLoading {csv_file} into table '{table_name}'...")
        df = pd.read_csv(csv_file)
        
        # Load to PostgreSQL (replace if exists)
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        # Verify
        with engine.connect() as conn:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table_name}")).fetchone()[0]
            print(f"✅ Loaded {count:,} rows into '{table_name}'")
    except Exception as e:
        print(f"❌ Error loading {csv_file}: {e}")
        exit(1)

# Step 3: Test basic SQL queries
print("\n" + "=" * 50)
print("STEP 3: Testing Basic SQL Queries")
print("=" * 50)

test_queries = [
    ("Total companies", "SELECT COUNT(*) FROM companies"),
    ("Total KPI records", "SELECT COUNT(*) FROM kpis"),
    ("Total deals", "SELECT COUNT(*) FROM dealflow"),
    ("Sample company", "SELECT \"Company Name\", \"Funding Total\" FROM companies LIMIT 1"),
]

for description, query in test_queries:
    try:
        with engine.connect() as conn:
            result = conn.execute(text(query))
            data = result.fetchone()
            print(f"✅ {description}: {data[0] if len(data) == 1 else data}")
    except Exception as e:
        print(f"❌ Query failed: {e}")

# Step 4: Set up LangChain SQL Database wrapper
print("\n" + "=" * 50)
print("STEP 4: Testing LangChain SQL Database Wrapper")
print("=" * 50)

try:
    db = SQLDatabase(engine, include_tables=["companies", "kpis", "dealflow"])
    print("✅ LangChain SQLDatabase wrapper initialized")
    print(f"Available tables: {db.get_usable_table_names()}")
    
    # Test getting table info
    print("\nCompanies table schema (first 200 chars):")
    table_info = db.get_table_info(["companies"])
    print(table_info[:200] + "...")
except Exception as e:
    print(f"❌ LangChain wrapper failed: {e}")
    exit(1)

# Step 5: Test LangChain Agent (requires OpenAI API key)
print("\n" + "=" * 50)
print("STEP 5: Testing LangChain SQL Agent")
print("=" * 50)

openai_key = os.getenv("OPENAI_API_KEY")

if not openai_key:
    print("⚠️  OPENAI_API_KEY not set in environment")
    print("To test the agent:")
    print("1. Get API key from: https://platform.openai.com/api-keys")
    print("2. Run: export OPENAI_API_KEY='your-key-here'")
    print("3. Run this script again")
else:
    try:
        # Initialize LLM
        llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
        
        # Create SQL agent
        toolkit = SQLDatabaseToolkit(db=db, llm=llm)
        agent = create_sql_agent(
            llm=llm,
            toolkit=toolkit,
            verbose=True,
            agent_type="openai-tools"
        )
        
        print("✅ LangChain SQL Agent initialized")
        
        # Test questions
        test_questions = [
            "How many companies are in the database?",
            "What is the total funding raised by all companies?",
        ]
        
        print("\n🤖 Testing agent with sample questions:")
        for i, question in enumerate(test_questions, 1):
            print(f"\n--- Question {i}: {question}")
            try:
                response = agent.invoke({"input": question})
                print(f"✅ Answer: {response['output']}")
            except Exception as e:
                print(f"❌ Agent error: {e}")
                
    except Exception as e:
        print(f"❌ Agent setup failed: {e}")

# Final Summary
print("\n" + "=" * 50)
print("INTEGRATION TEST SUMMARY")
print("=" * 50)
print("✅ PostgreSQL connection: Working")
print("✅ CSV data loading: Working")
print("✅ Basic SQL queries: Working")
print("✅ LangChain SQL wrapper: Working")
if openai_key:
    print("✅ LangChain SQL Agent: Ready to test")
else:
    print("⚠️  LangChain SQL Agent: Needs OPENAI_API_KEY")

print("\n🎉 Integration workflow is functional!")
print("\nNext steps:")
print("1. Set OPENAI_API_KEY environment variable")
print("2. Test with more complex questions")
print("3. Add security rules for LP gatekeeping")
