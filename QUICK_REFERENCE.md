# Quick Reference - FactoryTest Agent

**One-page cheat sheet for daily use**

---

## 🚀 Starting Your Session

```bash
# 1. Navigate to project
cd ~/FactoryTest

# 2. Activate virtual environment (CRITICAL - do this first!)
source venv/bin/activate

# 3. Verify venv is active (should see "(venv)" in prompt)
# (venv) dannazca@MacBook-Air FactoryTest %

# 4. Check PostgreSQL is running
brew services list | grep postgresql
# Should show: postgresql@16  started

# If not running:
brew services start postgresql@16
```

---

## 🤖 Running the Agent

### Quick Test (Simple Questions)
```bash
python quick_demo.py
```
- Tests 3 simple questions
- Takes ~2-3 minutes
- Good for quick validation

### Advanced Test (Complex Reasoning)
```bash
python advanced_test.py
```
- Tests 3 complex questions
- Shows agent reasoning process
- Takes ~5-10 minutes
- Best for comprehensive testing

### Integration Test (Data Loading)
```bash
python test_integration.py
```
- Loads CSV data into PostgreSQL
- Tests full stack
- Run this first time only (or to reload data)

---

## 🔍 Health Checks

```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Check database exists
psql -l | grep factorytest_local

# Count records in database
psql factorytest_local -c "SELECT COUNT(*) FROM companies;"
# Should return: 2175

# Check Python environment
which python
# Should show: .../FactoryTest/venv/bin/python

# Check if venv is active
echo $VIRTUAL_ENV
# Should show: /Users/.../FactoryTest/venv

# Check API key is loaded
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✅ OK' if os.getenv('OPENAI_API_KEY') else '❌ MISSING')"
```

---

## 🐛 Common Issues & Quick Fixes

### "OPENAI_API_KEY not found"
```bash
# Check .env file exists
cat .env | grep OPENAI_API_KEY
# If missing, add: OPENAI_API_KEY=sk-proj-...
```

### "PostgreSQL connection failed"
```bash
brew services restart postgresql@16
```

### "Module not found"
```bash
# Make sure venv is active
source venv/bin/activate
pip install -r requirements.txt
```

### "Command not found: psql"
```bash
# Add PostgreSQL to PATH
echo 'export PATH="/opt/homebrew/opt/postgresql@16/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

### Virtual Environment Not Working
```bash
# Deactivate first
deactivate

# Recreate venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

## 💬 Example Questions to Test

### Simple Questions
- "How many companies are in the database?"
- "Which company raised the most funding?"
- "Show me the top 5 companies by valuation"

### Complex Questions
- "What are the top 5 fintech companies in Brazil?"
- "Show me all deals from Q4 2024 with status = closed"
- "What is the average deal size by stage?"
- "Which investors have invested in the most companies?"
- "Show me companies founded after 2020 with negative EBITDA"

### Data Exploration
- "What columns are in the companies table?"
- "Show me a sample row from the dealflow table"
- "What are the unique values in the 'stage' column?"

---

## 📁 Project Structure

```
FactoryTest/
├── README.md                 # Project overview (start here)
├── SETUP_GUIDE.md           # Complete setup instructions
├── QUICK_REFERENCE.md       # This file - daily cheat sheet
│
├── docs/private/            # Private docs (gitignored)
│   ├── FINAL_PDR_12WEEKS.md          # 12-week roadmap
│   └── SECURITY_ARCHITECTURE.md       # LP security design
│
├── .env                     # Your API key (gitignored)
├── .env.example             # Template
├── requirements.txt         # Python packages
│
├── test_integration.py      # Load data + full test
├── quick_demo.py           # Quick 3-question test
├── advanced_test.py        # Complex reasoning test
│
├── venv/                   # Virtual environment (gitignored)
├── Companies.csv           # 2,175 companies (gitignored)
├── KPIs_prueba.csv        # 21,514 KPI records (gitignored)
└── dealflow_prueba.csv    # 4,676 deals (gitignored)
```

---

## 🔐 Security Checklist

Before committing:
```bash
# Check what's staged
git status

# Verify .env is NOT listed (should be gitignored)
# Verify CSV files are NOT listed (should be gitignored)

# If .env or CSV files appear, DO NOT COMMIT
# Check .gitignore file
```

---

## 📊 Quick Stats

| Metric | Value |
|--------|-------|
| Companies | 2,175 |
| KPI Records | 21,514 |
| Deals | 4,676 |
| **Total Rows** | **28,365** |
| Tables | 3 |
| Cost per Query | ~$0.01-0.02 |
| Response Time | 30-60 seconds |

---

## 🔄 Daily Workflow

### Starting Work
1. `cd ~/FactoryTest`
2. `source venv/bin/activate`
3. Check PostgreSQL: `brew services list | grep postgresql`
4. Run tests: `python quick_demo.py`

### During Work
- Make changes to code
- Test frequently
- Keep venv activated

### Ending Work
1. `deactivate`
2. Commit changes: `git add . && git commit -m "..."`
3. Push to GitHub: `git push origin main`

---

## 📞 When You Need Help

| Issue | See Document | Section |
|-------|-------------|---------|
| First-time setup | SETUP_GUIDE.md | Full guide |
| Venv not working | SETUP_GUIDE.md | Step 5 + Troubleshooting |
| PostgreSQL issues | SETUP_GUIDE.md | Troubleshooting |
| API key problems | SETUP_GUIDE.md | Step 7 |
| Understanding security | SECURITY_ARCHITECTURE.md | All sections |
| Project roadmap | FINAL_PDR_12WEEKS.md | Week-by-week |
| Quick reference | QUICK_REFERENCE.md | This file |

---

## ✅ Before Running Tests Checklist

- [ ] Virtual environment activated (`(venv)` in prompt)
- [ ] PostgreSQL running (`brew services list`)
- [ ] Database exists (`psql -l | grep factorytest_local`)
- [ ] API key in `.env` file
- [ ] CSV files in project root
- [ ] Dependencies installed (`pip list | grep langchain`)

**If all checked - run `python quick_demo.py` to start!**

---

## 💡 Pro Tips

1. **Always activate venv first** - This is the #1 cause of errors
2. **Check PostgreSQL status** before running tests
3. **Use quick_demo.py** for fast validation
4. **Use advanced_test.py** to see agent reasoning
5. **Deactivate venv** when done to avoid confusion later

---

## 🎯 Next Steps After Setup

1. ✅ Run reasoning tests: `python advanced_test.py`
2. ✅ Test UI (if applicable)
3. ✅ Review SECURITY_ARCHITECTURE.md for LP planning
4. ✅ Check FINAL_PDR_12WEEKS.md for Week 2 tasks

---

**Last Updated**: November 7, 2025  
**Purpose**: Daily reference for common tasks  
**Print This**: Keep handy while working
