# FactoryTest - Agent & Workflow Platform

## 🎯 Project Overview
AI-powered agent system for analyzing venture capital data across Companies, KPIs, and Deal Flow.

## 📊 Data Sources
- **Companies.csv** (2,175 companies, 6.34 MB)
- **KPIs_prueba.csv** (21,514 records, 8.15 MB) - Financial & operational metrics
- **dealflow_prueba.csv** (4,676 deals, 19.08 MB) - Deal pipeline & scoring

## 🛠️ Setup Instructions

### Activate Virtual Environment
```bash
source venv/bin/activate
```

### Install Dependencies
```bash
pip install pandas numpy
```

### Test Setup
```bash
python test_setup.py
```

### Deactivate Virtual Environment
```bash
deactivate
```

## 📅 Update Schedule
- **Weekly**: KPIs_prueba.csv (Mondays)
- **Monthly**: Companies.csv + dealflow_prueba.csv (1st of month)

## 🚀 Recommended Tech Stack
- **Backend**: Python + pandas for data processing
- **UI**: Streamlit (low-code, free) or Retool (paid, polished)
- **Agents**: LangChain + OpenAI API
- **Automation**: n8n or Make.com for scheduled updates
- **Database**: SQLite (local) or Supabase (cloud)

## 📋 Next Steps
1. Choose UI framework (Streamlit vs Retool)
2. Set up automation workflows
3. Build first agent (Portfolio Analyzer)
4. Connect to OpenAI API

---
**Environment**: Python 3.9.6 | Pandas 2.3.3
