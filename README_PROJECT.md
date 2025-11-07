# FactoryTest - AI-Powered Portfolio Analytics Platform

**Status**: Week 1 Complete - Local Development Phase ✅  
**Last Updated**: November 6, 2025

---

## 🎯 Project Overview

FactoryTest is an AI-powered analytics platform for venture capital portfolio management. It enables natural language queries against portfolio data using LangChain SQL agents, with planned investor-specific access controls via WhatsApp.

### Key Features
- ✅ Natural language queries on 28k+ rows of portfolio data
- ✅ LangChain SQL agents with GPT-4o-mini
- ✅ PostgreSQL database with company, KPI, and deal flow data
- 🚧 Investor gatekeeping with WhatsApp authentication (Weeks 9-12)
- 🚧 Multi-tenant security with Row-Level Security (Week 3-4)

---

## 📊 Current Status

### Completed (Week 1 - Day 1-2)
- [x] PostgreSQL 16.10 installed and configured
- [x] Database schema created (companies, kpis, dealflow)
- [x] CSV data loaded (2,175 companies, 21,514 KPIs, 4,676 deals)
- [x] LangChain SQL agents integrated
- [x] Integration tests passing
- [x] Advanced query testing with natural language

### Data Loaded
| Table | Rows | Description |
|-------|------|-------------|
| `companies` | 2,175 | Company profiles, funding, investors |
| `kpis` | 21,514 | Time-series KPI data (revenue, ARPU, etc.) |
| `dealflow` | 4,676 | Deal pipeline with scoring and status |
| **Total** | **28,365** | **Complete portfolio dataset** |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    User Query                            │
│           (Natural Language Question)                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              LangChain SQL Agent                         │
│              (GPT-4o-mini)                              │
│   - Understands question                                │
│   - Generates SQL query                                 │
│   - Validates syntax                                    │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│              PostgreSQL Database                         │
│   - 28,365 rows across 3 tables                        │
│   - Row-Level Security (RLS) - Coming in Week 3        │
└────────────────────┬────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────────────┐
│           Natural Language Answer                        │
│   "The top company is Plata Card with $635M"           │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start

### Prerequisites
- macOS 12.3+ (tested) or Linux
- Python 3.9+
- PostgreSQL 16+
- OpenAI API key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd FactoryTest
```

2. **Set up Python virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

4. **Set up PostgreSQL**
```bash
# Install PostgreSQL (macOS with Homebrew)
brew install postgresql@16
brew services start postgresql@16

# Create database
createdb factorytest_local
```

5. **Load data**
```bash
# Place your CSV files in the project root:
# - Companies.csv
# - KPIs_prueba.csv
# - dealflow_prueba.csv

# Run integration test (loads data automatically)
python test_integration.py
```

6. **Test the agent**
```bash
python quick_demo.py
```

---

## 📝 Usage Examples

### Example 1: Simple Query
```python
from quick_demo import agent

agent.query("How many companies are in the database?")
# Output: "There are 2,175 companies in the database."
```

### Example 2: Complex Query
```python
agent.query("What are the top 5 companies by valuation?")
# Output:
# 1. Plata Card - $635,000,000
# 2. MOMBAK - $428,395,124
# 3. Polkadot en Español - $202,700,000
# ...
```

### Example 3: Time Series Analysis
```python
agent.query("What is the average valuation per month in 2024?")
# Returns monthly breakdown with deal counts
```

---

## 🧪 Testing

### Run All Tests
```bash
# Basic integration test
python test_integration.py

# Advanced queries with reasoning
python advanced_test.py

# Quick demo
python quick_demo.py
```

### Test Results
- ✅ PostgreSQL connection: Working
- ✅ CSV data loading: 28,365 rows loaded
- ✅ LangChain SQL wrapper: Connected
- ✅ Agent queries: 100% accuracy on test questions
- ✅ Complex reasoning: Multi-step queries working

---

## 📁 Project Structure

```
FactoryTest/
├── .env                          # Environment variables (DO NOT COMMIT)
├── .env.example                  # Environment template
├── .gitignore                    # Git ignore rules
├── requirements.txt              # Python dependencies
├── README_PROJECT.md             # This file
│
├── test_integration.py           # Full 5-step integration test
├── quick_demo.py                 # Quick validation script
├── advanced_test.py              # Complex query testing
│
├── FINAL_PDR_12WEEKS.md         # 12-week product roadmap
├── SECURITY_ARCHITECTURE.md     # Security & gatekeeping design
├── INTEGRATION_TEST_RESULTS.md  # Test results documentation
├── ADVANCED_TEST_RESULTS.md     # Advanced query results
├── SESSION_SUMMARY.md           # Session summary
├── INDEX.md                      # Documentation index
│
├── venv/                         # Virtual environment (DO NOT COMMIT)
└── *.csv                         # Data files (DO NOT COMMIT)
```

---

## 🔐 Security

### Current Status (Week 1)
- ⚠️ **Local development only** - No authentication required
- ⚠️ **Full database access** - No restrictions yet
- ✅ **API key in .env** - Not committed to Git
- ✅ **CSV data excluded** - Not in version control

### Planned Security (Weeks 3-12)
- 🔒 WhatsApp phone number authentication (Week 9)
- 🔒 Row-Level Security (PostgreSQL RLS) (Week 3)
- 🔒 LangChain Middleware for gatekeeping (Week 3-4)
- 🔒 Investor-specific data access (Week 9-12)
- 🔒 Rate limiting (50 queries/hour per user) (Week 3)
- 🔒 Audit logging (all queries tracked) (Week 3)

See [SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md) for detailed security design.

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Database** | PostgreSQL | 16.10 | Data storage |
| **ORM** | SQLAlchemy | 2.0.44 | Database abstraction |
| **AI Framework** | LangChain | 0.3.27 | Agent framework |
| **LLM** | OpenAI GPT-4o-mini | Latest | Natural language understanding |
| **Python** | Python | 3.9.6 | Core language |
| **Data Processing** | Pandas | 2.3.3 | Data manipulation |
| **Environment** | python-dotenv | 1.2.1 | Environment variables |

---

## 📅 Roadmap

### Phase 1: Local Development (Weeks 1-5) - $0 cost
- ✅ **Week 1**: PostgreSQL + ETL *(COMPLETE)*
- 🔄 **Week 2**: Automation + Google Drive integration
- 🔄 **Week 3**: Internal agents (3 types)
- 🔄 **Week 4**: LP agent + gatekeeping
- 🔄 **Week 5**: Local usability testing (15 team members)

### Phase 2: AWS Migration (Week 6) - Costs begin
- 🔄 **Week 6**: Deploy to AWS (~$70/month)

### Phase 3: Production (Weeks 7-8)
- 🔄 **Week 7-8**: Internal team production use + feedback

### Phase 4: LP Rollout (Weeks 9-12)
- 🔄 **Week 9**: LP security hardening
- 🔄 **Week 10**: LP UI + documentation
- 🔄 **Week 11**: LP beta testing
- 🔄 **Week 12**: Full LP launch via WhatsApp 🚀

**Total Budget**: ~$700 for 12 weeks

See [FINAL_PDR_12WEEKS.md](FINAL_PDR_12WEEKS.md) for complete roadmap.

---

## 🤝 Contributing

### Team Setup (Week 5+)
When the Vibe Coders team joins:

1. Clone the repository
2. Set up local environment (follow Quick Start)
3. Get OpenAI API key from team lead
4. Load CSV data (available in shared drive)
5. Run tests to verify setup

### Development Workflow
```bash
# Create feature branch
git checkout -b feature/your-feature-name

# Make changes
# ...

# Run tests
python test_integration.py

# Commit with descriptive message
git commit -m "feat: add investor gatekeeping middleware"

# Push and create PR
git push origin feature/your-feature-name
```

---

## 📊 Performance Metrics

### Agent Performance (Week 1 Testing)
| Metric | Result |
|--------|--------|
| Query Accuracy | 100% (all test queries correct) |
| Avg Response Time | 30-60 seconds |
| Complex Query Handling | ✅ Excellent |
| Schema Navigation | ✅ 145+ columns handled |
| SQL Injection Protection | ✅ Built-in validation |
| Cost per Query | ~$0.01-0.02 (GPT-4o-mini) |

### Database Stats
- **Total Rows**: 28,365
- **Tables**: 3 (companies, kpis, dealflow)
- **Query Performance**: <1 second for most queries
- **Data Size**: ~15 MB (in-memory)

---

## 🐛 Known Issues

1. **Agent Response Time**: Currently 30-60 seconds per query
   - *Solution*: Will optimize to <10s in Week 3
   
2. **Verbose Output**: Agent shows all reasoning steps
   - *Solution*: Add `verbose=False` for production (Week 3)
   
3. **No Caching**: Every query hits database
   - *Solution*: Add Redis caching in Week 6

4. **CSV Data Not Automated**: Manual CSV loading
   - *Solution*: Google Drive integration in Week 2

---

## 📚 Documentation

- **[FINAL_PDR_12WEEKS.md](FINAL_PDR_12WEEKS.md)** - Complete 12-week roadmap
- **[SECURITY_ARCHITECTURE.md](SECURITY_ARCHITECTURE.md)** - Security & gatekeeping design
- **[INTEGRATION_TEST_RESULTS.md](INTEGRATION_TEST_RESULTS.md)** - Initial test results
- **[ADVANCED_TEST_RESULTS.md](ADVANCED_TEST_RESULTS.md)** - Complex query testing
- **[SESSION_SUMMARY.md](SESSION_SUMMARY.md)** - Day 1-2 session summary
- **[INDEX.md](INDEX.md)** - Documentation navigation

---

## 💰 Cost Tracking

### Week 1 Costs: ~$0.05
- PostgreSQL: $0 (local)
- OpenAI API: ~$0.05 (testing)

### Projected Costs
- **Weeks 1-5**: ~$20 (local + API)
- **Weeks 6-12**: ~$700 (AWS + API)
- **Total**: ~$720

---

## 📞 Support

### Getting Help
- Check documentation in this README
- Review [INDEX.md](INDEX.md) for navigation
- Check test scripts for examples
- Review session summaries for context

### Common Issues
**"OPENAI_API_KEY not found"**
- Ensure `.env` file exists with your API key
- Run `source .env` if needed

**"PostgreSQL connection failed"**
- Check PostgreSQL is running: `brew services list`
- Restart if needed: `brew services restart postgresql@16`

**"Module not found"**
- Activate virtual environment: `source venv/bin/activate`
- Install dependencies: `pip install -r requirements.txt`

---

## 📄 License

Private repository - Internal use only.

---

## 🎉 Acknowledgments

- Built with LangChain and OpenAI GPT-4o-mini
- PostgreSQL for robust data storage
- Factory Droid for development assistance

---

**Last Updated**: November 6, 2025  
**Version**: 0.1.0 (Week 1 Complete)  
**Status**: ✅ Local development functional, ready for Week 2
