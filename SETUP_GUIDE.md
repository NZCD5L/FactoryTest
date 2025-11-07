# FactoryTest - Complete Setup & Agent Initialization Guide

**Last Updated**: November 7, 2025  
**Status**: Week 1 Complete - Ready for Testing

---

## 🎯 What This Guide Covers

This is your **step-by-step guide** to:
1. Set up your local environment from scratch
2. Initialize the Python virtual environment
3. Configure the database
4. Run the LangChain SQL agent
5. Test with sample queries

**Time Required**: 20-30 minutes (first time setup)

---

## 📋 Prerequisites

Before starting, ensure you have:
- ✅ macOS 12.3+ or Linux
- ✅ Python 3.9 or higher
- ✅ Terminal access
- ✅ OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

---

## 🚀 Step-by-Step Setup

### Step 1: Install Homebrew (if not installed)

Check if Homebrew is installed:
```bash
brew --version
```

If not installed, run:
```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

---

### Step 2: Install PostgreSQL 16

```bash
# Install PostgreSQL
brew install postgresql@16

# Start PostgreSQL service
brew services start postgresql@16

# Verify installation
postgres --version
```

**Expected output**: `postgres (PostgreSQL) 16.x`

---

### Step 3: Create Database

```bash
# Create the database
createdb factorytest_local

# Verify database exists
psql -l | grep factorytest_local
```

**Expected output**: You should see `factorytest_local` in the list

---

### Step 4: Clone Repository (if not done)

```bash
# Clone from GitHub
git clone https://github.com/NZCD5L/FactoryTest.git

# Navigate to project directory
cd FactoryTest
```

---

### Step 5: Set Up Python Virtual Environment

This is **critical** - always use the virtual environment to avoid package conflicts.

#### Create Virtual Environment (first time only)

```bash
# Create virtual environment
python3 -m venv venv
```

This creates a `venv/` folder with an isolated Python environment.

#### Activate Virtual Environment

**Every time** you work on this project, activate the environment first:

```bash
# Activate (macOS/Linux)
source venv/bin/activate
```

**You'll know it worked when your terminal prompt shows `(venv)` at the beginning:**
```bash
(venv) dannazca@MacBook-Air FactoryTest %
```

#### Deactivate Virtual Environment (when done working)

```bash
deactivate
```

---

### Step 6: Install Python Dependencies

**Important**: Make sure your virtual environment is activated first!

```bash
# Verify venv is active (should see "venv" in prompt)
which python
# Should output: /Users/[your-username]/FactoryTest/venv/bin/python

# Install all required packages
pip install -r requirements.txt
```

**This installs 40+ packages including:**
- `langchain` - AI agent framework
- `langchain-openai` - OpenAI integration
- `sqlalchemy` - Database toolkit
- `psycopg2-binary` - PostgreSQL adapter
- `pandas` - Data manipulation

**Expected output**: All packages installed successfully (no errors)

---

### Step 7: Configure Environment Variables

Create your `.env` file with your OpenAI API key:

```bash
# Copy the template
cp .env.example .env

# Edit with your favorite editor (nano, vim, or VSCode)
nano .env
```

**Update this line with your actual API key:**
```bash
OPENAI_API_KEY=your_actual_api_key_here
```

**Save and close** (in nano: `Ctrl+O`, `Enter`, `Ctrl+X`)

#### Verify API Key is Set

```bash
# Check .env file exists and has your key
cat .env | grep OPENAI_API_KEY
```

**Expected output**: `OPENAI_API_KEY=sk-proj-...` (your key)

---

### Step 8: Load Data into PostgreSQL

Run the integration test script which automatically loads the CSV data:

```bash
# Make sure venv is active!
python test_integration.py
```

**What this does:**
1. Connects to PostgreSQL
2. Loads 3 CSV files into database:
   - `Companies.csv` → 2,175 rows
   - `KPIs_prueba.csv` → 21,514 rows
   - `dealflow_prueba.csv` → 4,676 rows
3. Tests basic SQL queries
4. Initializes LangChain agent

**Expected output:**
```
==================================================
STEP 1: Testing PostgreSQL Connection
==================================================
✅ Connected to PostgreSQL!

==================================================
STEP 2: Loading CSV Data into PostgreSQL
==================================================
✅ Loaded 2,175 rows into 'companies'
✅ Loaded 21,514 rows into 'kpis'
✅ Loaded 4,676 rows into 'dealflow'

==================================================
INTEGRATION TEST SUMMARY
==================================================
✅ PostgreSQL connection: Working
✅ CSV data loading: Working
✅ Basic SQL queries: Working
✅ LangChain SQL wrapper: Working
✅ LangChain SQL Agent: Ready to test

🎉 Integration workflow is functional!
```

---

## 🤖 Running the Agent

### Quick Demo (Simple Questions)

```bash
# Make sure venv is active!
python quick_demo.py
```

**What this tests:**
- "How many companies are in the database?"
- "Which company has raised the most funding?"
- "List the top 5 companies by total funding"

**Expected behavior:**
- Agent shows its reasoning process (verbose mode)
- Generates SQL queries
- Returns natural language answers
- Takes 30-60 seconds per query

---

### Advanced Testing (Complex Questions)

```bash
# Make sure venv is active!
python advanced_test.py
```

**What this tests:**
- Complex multi-table queries
- Date filtering and aggregations
- Multi-step reasoning
- Schema navigation (145+ columns)

**Example questions:**
- "What are the top 5 companies based on company valuation?"
- "What is the oldest deal in the portfolio?"
- "What is the average valuation per month of 2024?"

---

## 🔍 Verify Everything is Working

### Quick Health Check

Run these commands to verify your setup:

```bash
# 1. Check PostgreSQL is running
brew services list | grep postgresql
# Should show: postgresql@16  started

# 2. Check database exists and has data
psql factorytest_local -c "SELECT COUNT(*) FROM companies;"
# Should show: 2175

# 3. Check Python environment
which python
# Should show: /Users/.../FactoryTest/venv/bin/python

# 4. Check packages installed
pip list | grep langchain
# Should show multiple langchain packages

# 5. Check API key is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ API Key loaded' if os.getenv('OPENAI_API_KEY') else '❌ No API Key')"
# Should show: ✅ API Key loaded
```

---

## 💡 Usage Examples

### Example 1: Ask a Simple Question

```python
# In Python (with venv activated)
python quick_demo.py
```

**Output:**
```
Question 1: How many companies are in the database?
✅ ANSWER: There are 2,175 companies in the database.
```

---

### Example 2: Complex Query

```python
python advanced_test.py
```

**Output:**
```
Question: What are the top 5 companies based on company valuation?

🤖 Agent thinking process:
- Examining tables...
- Found 'companies' table with 'Funding Total' column
- Generating SQL query...
- Validating syntax...
- Executing query...

✅ ANSWER:
1. Plata Card - $635,000,000
2. MOMBAK - $428,395,124
3. Polkadot en Español - $202,700,000
4. Fairplay - $181,219,435
5. R2 - $180,025,000
```

---

## 🐛 Troubleshooting

### Issue: "OPENAI_API_KEY not found"

**Solution:**
```bash
# Check .env file exists
ls -la .env

# Verify API key is in the file
cat .env | grep OPENAI_API_KEY

# Make sure it starts with sk-proj- or sk-
# If missing, add: OPENAI_API_KEY=your_key_here
```

---

### Issue: "PostgreSQL connection failed"

**Solution:**
```bash
# Check if PostgreSQL is running
brew services list | grep postgresql

# If not running, start it
brew services start postgresql@16

# If database doesn't exist, create it
createdb factorytest_local
```

---

### Issue: "ModuleNotFoundError: No module named 'langchain'"

**Solution:**
```bash
# Make sure venv is activated (check for "(venv)" in prompt)
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

### Issue: "psql: command not found"

**Solution:**
```bash
# Add PostgreSQL to your PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc

# Reload shell configuration
source ~/.zshrc

# Verify
which psql
```

---

### Issue: Virtual Environment Not Activating

**Solution:**
```bash
# Delete and recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📁 Project Structure

```
FactoryTest/
├── .env                      # Your API key (DO NOT COMMIT)
├── .env.example              # Template for API key
├── .gitignore                # Git ignore rules
├── requirements.txt          # Python dependencies
│
├── README.md                 # Project overview
├── SETUP_GUIDE.md            # This file - setup instructions
├── SECURITY_ARCHITECTURE.md  # LP security design
├── FINAL_PDR_12WEEKS.md      # 12-week roadmap
│
├── test_integration.py       # Full integration test + data loading
├── quick_demo.py             # Quick agent test
├── advanced_test.py          # Complex query testing
├── test_setup.py             # Environment validation
│
├── venv/                     # Virtual environment (DO NOT COMMIT)
├── Companies.csv             # Company data (DO NOT COMMIT)
├── KPIs_prueba.csv          # KPI data (DO NOT COMMIT)
└── dealflow_prueba.csv      # Deal flow data (DO NOT COMMIT)
```

---

## 🔐 Security Checklist

Before committing any code, verify:

- ✅ `.env` file is in `.gitignore`
- ✅ CSV files are in `.gitignore`
- ✅ `venv/` folder is in `.gitignore`
- ✅ No API keys in code files
- ✅ Only use `.env.example` as template (no real keys)

**Check with:**
```bash
git status
# Should NOT show .env or CSV files
```

---

## 🔄 Daily Workflow

### Starting Your Work Session

```bash
# 1. Navigate to project
cd ~/FactoryTest

# 2. Activate virtual environment
source venv/bin/activate

# 3. Check PostgreSQL is running
brew services list | grep postgresql

# 4. Start working!
python quick_demo.py
```

### Ending Your Work Session

```bash
# Deactivate virtual environment
deactivate
```

---

## 📊 What Questions Can the Agent Answer?

### Portfolio Analysis
- "How many companies are in our portfolio?"
- "Which companies raised the most funding?"
- "Show me all fintech companies"
- "Companies founded after 2020"
- "List all companies in Brazil"

### Financial Queries
- "Total funding across all companies"
- "Average deal size by stage"
- "Companies with over $100M valuation"
- "Which investors have invested in the most companies?"

### Deal Flow
- "How many active deals?"
- "What is the oldest deal?"
- "Show me all rejected deals"
- "Deals by geography"
- "Average deal score by stage"

### KPI Tracking
- "Show revenue trends for [company]"
- "Companies with negative EBITDA"
- "Growth rates by sector"
- "Monthly KPI trends"

---

## 🎯 Next Steps After Setup

Once your setup is working:

1. **Run reasoning tests** (as per your request):
   ```bash
   python advanced_test.py
   ```

2. **Test UI** (if applicable):
   - Check if Streamlit or UI is set up
   - Or plan UI implementation

3. **Review security architecture**:
   - See `SECURITY_ARCHITECTURE.md`
   - Plan LP gatekeeping implementation

4. **Continue with Week 2**:
   - See `FINAL_PDR_12WEEKS.md` for roadmap
   - Set up automation (Google Drive integration)

---

## 💰 Costs

### Current Setup Costs
- PostgreSQL: **$0** (local installation)
- Python packages: **$0** (open source)
- Testing: **~$0.05** (OpenAI API)

### Ongoing Costs (Local Development)
- Per query: **~$0.01-0.02** (GPT-4o-mini)
- Weekly testing: **~$5-10**

### Production Costs (Week 6+)
- AWS RDS: **~$30/month**
- API usage: **~$20/month**
- Total: **~$50/month**

---

## 📞 Need Help?

### Common Questions

**Q: Do I need to activate venv every time?**  
A: Yes! Always activate before running Python scripts.

**Q: Can I delete the venv folder?**  
A: Yes, you can recreate it with `python3 -m venv venv`

**Q: Where is my API key stored?**  
A: In `.env` file (gitignored, safe)

**Q: Can I use this on Windows?**  
A: Yes, but activation command is `venv\Scripts\activate` (not `source venv/bin/activate`)

**Q: How do I update dependencies?**  
A: Run `pip install -r requirements.txt --upgrade`

---

## ✅ Setup Complete Checklist

Before moving forward, verify:

- [ ] PostgreSQL installed and running
- [ ] Database `factorytest_local` created
- [ ] Virtual environment created (`venv/` folder exists)
- [ ] Can activate venv (see `(venv)` in terminal)
- [ ] All packages installed (`pip list` shows langchain)
- [ ] `.env` file created with API key
- [ ] Data loaded (test_integration.py runs successfully)
- [ ] Agent responds to queries (quick_demo.py works)
- [ ] Advanced tests pass (advanced_test.py works)

**If all boxes are checked - you're ready for reasoning and UI tests!** 🎉

---

**Last Updated**: November 7, 2025  
**Version**: 1.0  
**Status**: ✅ Ready for Production Testing
