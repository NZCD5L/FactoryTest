# FactoryTest - AI-Powered Portfolio Analytics

**Status**: Week 1 Complete ✅ | Ready for Testing  
**Repository**: https://github.com/NZCD5L/FactoryTest

---

## 🎯 What is FactoryTest?

An AI-powered analytics platform that lets you ask **natural language questions** about your venture capital portfolio data.

**Example questions:**
- "What are the top 5 companies by valuation?"
- "Which deals were closed in Q4 2024?"
- "Show me all fintech companies in Brazil"
- "What is the average funding round size?"

**The agent understands your question, generates SQL queries, and returns answers in plain English.**

---

## 📊 Current Data

| Dataset | Records | Description |
|---------|---------|-------------|
| Companies | 2,175 | Company profiles, funding, investors |
| KPIs | 21,514 | Financial & operational metrics |
| Deal Flow | 4,676 | Deal pipeline, scoring, status |
| **Total** | **28,365** | Complete portfolio dataset |

---

## 🚀 Quick Start

### First Time Setup (20-30 minutes)

**See complete instructions in: [`SETUP_GUIDE.md`](SETUP_GUIDE.md)**

Quick summary:
1. Install PostgreSQL 16
2. Create database: `createdb factorytest_local`
3. Activate virtual environment: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Configure `.env` with your OpenAI API key
6. Load data: `python test_integration.py`
7. Test agent: `python quick_demo.py`

---

## 🤖 Running the Agent

```bash
# Always activate virtual environment first
source venv/bin/activate

# Quick test (simple questions)
python quick_demo.py

# Advanced test (complex reasoning)
python advanced_test.py
```

**Example output:**
```
Question: What are the top 5 companies by valuation?

✅ ANSWER:
1. Plata Card - $635,000,000
2. MOMBAK - $428,395,124
3. Polkadot en Español - $202,700,000
4. Fairplay - $181,219,435
5. R2 - $180,025,000
```

---

## 📚 Documentation

| Document | Purpose |
|----------|---------|
| **[SETUP_GUIDE.md](SETUP_GUIDE.md)** | Complete setup & initialization (START HERE) |
| **[FINAL_PDR_12WEEKS.md](FINAL_PDR_12WEEKS.md)** | 12-week product roadmap |
| **[SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md)** | LP security & gatekeeping design |
| **README.md** | This file - project overview |

---

## 🛠️ Technology Stack

- **Database**: PostgreSQL 16 (local development)
- **AI Framework**: LangChain + OpenAI GPT-4o-mini
- **Language**: Python 3.9+
- **Data Processing**: Pandas, SQLAlchemy
- **Cost**: ~$0.01-0.02 per query

---

## 🔐 Security

- ✅ API keys in `.env` (gitignored)
- ✅ CSV data files excluded from Git
- ✅ SQL injection protection built-in
- ✅ No sensitive data in version control

---

## 📅 Project Roadmap

**Week 1** (✅ Complete): Local PostgreSQL + LangChain integration  
**Week 2**: Automation + Google Drive sync  
**Week 3-4**: Specialized agents + LP gatekeeping  
**Week 5**: Internal team testing (15 users)  
**Week 6**: AWS deployment  
**Weeks 7-12**: Production rollout + LP access

See [FINAL_PDR_12WEEKS.md](FINAL_PDR_12WEEKS.md) for details.

---

## 💡 Sample Questions the Agent Can Answer

### Portfolio Analysis
- "How many companies are in our portfolio?"
- "Which companies raised the most funding?"
- "Show me all companies founded after 2020"

### Financial Analysis
- "Total funding across all companies"
- "Companies with over $100M valuation"
- "Average deal size by stage"

### Deal Flow
- "What is the oldest deal in the portfolio?"
- "How many active deals do we have?"
- "Show me all rejected deals and why"

### KPI Tracking
- "Show revenue trends for [company]"
- "Companies with negative EBITDA"
- "Monthly growth rates by sector"

---

## 🐛 Troubleshooting

**"OPENAI_API_KEY not found"**  
→ Create `.env` file with your API key (see SETUP_GUIDE.md)

**"PostgreSQL connection failed"**  
→ Start PostgreSQL: `brew services start postgresql@16`

**"Module not found"**  
→ Activate venv: `source venv/bin/activate`

**Full troubleshooting guide**: See [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🤝 Team Setup

When new team members join:
1. Clone this repository
2. Follow [SETUP_GUIDE.md](SETUP_GUIDE.md) step-by-step
3. Get OpenAI API key from team lead
4. Place CSV files in project root
5. Run tests to verify setup

---

## 💰 Cost Summary

**Local Development (Weeks 1-5)**: ~$20  
**AWS Production (Weeks 6-12)**: ~$700  
**Total Budget**: ~$720

Per-query cost: ~$0.01-0.02 (GPT-4o-mini)

---

## ✅ Current Status

- ✅ PostgreSQL installed and configured
- ✅ 28,365 rows loaded across 3 tables
- ✅ LangChain SQL agent functional
- ✅ Complex natural language queries working
- ✅ 100% query accuracy in testing
- ✅ Security best practices implemented

**Ready for reasoning tests and UI development!**

---

**Last Updated**: November 7, 2025  
**Version**: 1.0 (Week 1 Complete)  
**License**: Private - Internal Use Only
